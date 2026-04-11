from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil
import os
import uuid
import io
import re
import pandas as pd
from datetime import datetime
from pathlib import Path
from sqlmodel import Session, select
from ..database import get_session
from ..models import Tool, User, Alert
from ..auth import get_current_user
router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

@router.post("/certificate")
async def upload_certificate(file: UploadFile = File(...)):
    ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: PDF, JPG, PNG")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    # Return URL (relative path)
    return {"url": f"/uploads/{unique_filename}"}

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: JPG, PNG, GIF")
    
    unique_filename = f"img_{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"url": f"/uploads/{unique_filename}"}

def generate_qr_code(description, date_of_supply, purchaser_name, supplier_code, index):
    name_part = "XX"
    if description:
        val = re.sub(r'[^A-Z]', 'X', str(description).upper())
        name_part = val[:2].ljust(2, 'X')

    date_part = "0000"
    if date_of_supply:
        try:
            dt = pd.to_datetime(date_of_supply)
            date_part = dt.strftime("%m%y")
        except:
            pass

    supplier_part = "XX"
    if purchaser_name:
        val = re.sub(r'[^A-Z]', 'X', str(purchaser_name).upper())
        supplier_part = val[:2].ljust(2, 'X')

    code_part = "000"
    if supplier_code:
        code_part = str(supplier_code).zfill(3)[:3].upper()
    else:
        code_part = str(index).zfill(3)[:3]

    return f"{name_part}{date_part}{supplier_part}{code_part}"

@router.post("/tools", response_model=dict)
async def upload_tools(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(('.xlsx', '.xls', '.pdf')):
        raise HTTPException(status_code=400, detail="Only Excel (.xlsx, .xls) and PDF files are supported.")
    
    contents = await file.read()
    
    if file.filename.endswith(('.xlsx', '.xls')):
        try:
            df = pd.read_excel(io.BytesIO(contents))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading Excel file: {str(e)}")
            
    elif file.filename.endswith('.pdf'):
        try:
            import pdfplumber
            tables = []
            with pdfplumber.open(io.BytesIO(contents)) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_table()
                    if extracted:
                        tables.extend(extracted)
            if not tables:
                raise HTTPException(status_code=400, detail="No readable tables found in the PDF.")
            
            headers = tables[0]
            df = pd.DataFrame(tables[1:], columns=headers)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading PDF file: {str(e)}")

    df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')
    required_cols = ['description', 'make', 'capacity', 'safe_working_load', 'purchaser_name']
    
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required columns in uploaded file: {', '.join(missing)}")

    success_count = 0
    errors = []
    existing_qrs = {t.qr_code for t in session.exec(select(Tool)).all()}

    for index, row in df.iterrows():
        try:
            row = row.where(pd.notnull(row), None)
            
            description = str(row.get('description', ''))
            make = str(row.get('make', datetime.now().year))
            capacity = str(row.get('capacity', ''))
            swl = str(row.get('safe_working_load', ''))
            purchaser = str(row.get('purchaser_name', ''))
            
            supplier_code = str(row.get('supplier_code', index + 1))
            date_val = row.get('date_of_supply', None)
            
            if pd.notnull(date_val):
                date_of_supply = pd.to_datetime(date_val).to_pydatetime()
            else:
                date_of_supply = datetime.now()
            
            qr_code = generate_qr_code(description, date_of_supply, purchaser, supplier_code, index)
            
            original_qr = qr_code
            counter = 1
            while qr_code in existing_qrs:
                qr_code = f"{original_qr}-{counter}"
                counter += 1
                
            existing_qrs.add(qr_code)
            
            expiry_date = None
            if date_of_supply:
                try:
                    expiry_date = datetime(date_of_supply.year + 3, date_of_supply.month, date_of_supply.day)
                except ValueError: 
                    expiry_date = datetime(date_of_supply.year + 3, date_of_supply.month, 28)
            
            db_tool = Tool(
                description=description,
                make=make,
                capacity=capacity,
                safe_working_load=swl,
                tool_type=str(row.get('tool_type', 'Erection Tools')),
                purchaser_name=purchaser,
                purchaser_contact=str(row.get('purchaser_contact', None)) if row.get('purchaser_contact') else None,
                supplier_code=supplier_code,
                job_code=str(row.get('job_code', None)) if row.get('job_code') else None,
                job_description=str(row.get('job_description', None)) if row.get('job_description') else None,
                date_of_supply=date_of_supply,
                expiry_date=expiry_date,
                validity_period=3,
                qr_code=qr_code,
                status="usable",
                inspection_result="usable"
            )
            session.add(db_tool)
            success_count += 1
        except Exception as e:
            errors.append(f"Row {index+2}: {str(e)}")

    if success_count > 0:
        session.commit()
        
        bulk_alert = Alert(
            type="new-tool",
            severity="info",
            title="Bulk Tools Uploaded",
            message=f"{success_count} tools have been mass-uploaded from {file.filename}.",
            site=None
        )
        session.add(bulk_alert)
        session.commit()

    return {
        "success": True,
        "message": f"Successfully imported {success_count} tools.",
        "errors": errors
    }
