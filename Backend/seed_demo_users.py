import sys
import os

# Add the Backend directory to sys.path to allow imports from src
sys.path.append(os.getcwd())

from sqlmodel import Session, select
from src.database.create_tables import engine, create_db_table
from src.database.models import User, UserRole
from src.auth.util import get_password_hash

def seed():
    # Ensure tables exist
    create_db_table()
    
    with Session(engine) as session:
        demo_users = [
            {
                "username": "caregiver@neurobin.com",
                "email": "caregiver@neurobin.com",
                "password": "neurobin123",
                "role": UserRole.caretaker
            },
            {
                "username": "doctor@neurobin.com",
                "email": "doctor@neurobin.com",
                "password": "neurobin123",
                "role": UserRole.doctor
            },
            {
                "username": "patient@neurobin.com",
                "email": "patient@neurobin.com",
                "password": "neurobin123",
                "role": UserRole.patient
            }
        ]
        
        for user_data in demo_users:
            # Check if user already exists
            statement = select(User).where(User.username == user_data["username"])
            existing_user = session.exec(statement).first()
            
            if not existing_user:
                print(f"Creating demo user: {user_data['username']}")
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=get_password_hash(user_data["password"]),
                    role=user_data["role"],
                    is_active=True
                )
                session.add(user)
            else:
                print(f"User {user_data['username']} already exists.")
        
        session.commit()
        print("Seeding completed successfully.")

if __name__ == "__main__":
    seed()
