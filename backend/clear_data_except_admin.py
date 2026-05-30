from sqlmodel import Session, select, SQLModel
from backend.database import engine
from backend.models import User, Tool, Inspection, Alert, MovementHistory

def clear_data():
    print("Connecting to the database...")
    with Session(engine) as session:
        # 1. Backup all admin users
        print("Backing up admin users...")
        admins = session.exec(select(User).where(User.role == "admin")).all()
        
        # Detach from session so we can re-add them to the new tables
        for admin in admins:
            session.expunge(admin)
            
    # 2. Drop and Recreate all tables (Guarantees auto-increment reset on ANY database: MySQL, Postgres, SQLite)
    print("Dropping all tables to reset auto-increment counters...")
    SQLModel.metadata.drop_all(engine)
    
    print("Recreating clean tables...")
    SQLModel.metadata.create_all(engine)
    
    # 3. Restore admin users
    with Session(engine) as session:
        print(f"Restoring {len(admins)} admin user(s)...")
        for admin in admins:
            session.add(admin)
            
        session.commit()
        print("Database completely wiped and auto-increment reset successfully! Only admin users remain.")

if __name__ == "__main__":
    clear_data()
