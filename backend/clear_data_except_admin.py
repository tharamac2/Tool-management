from sqlmodel import Session, select, SQLModel
from backend.database import engine
from backend.models import User
from backend.auth import get_password_hash

def clear_data():
    print("Connecting to the database...")
    
    # Drop and Recreate all tables
    print("Dropping all tables to wipe everything...")
    SQLModel.metadata.drop_all(engine)
    
    print("Recreating clean tables...")
    SQLModel.metadata.create_all(engine)
    
    # Create the brand new Admin User
    print("Creating fresh Admin user with password: Admin@1234")
    with Session(engine) as session:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            role="admin",
            status="active",
            hashed_password=get_password_hash("Admin@1234")
        )
        session.add(admin_user)
        session.commit()
        
        print("Database completely wiped and brand new Admin user created successfully!")

if __name__ == "__main__":
    clear_data()
