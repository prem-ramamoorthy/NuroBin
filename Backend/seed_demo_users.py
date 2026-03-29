import sys
import os

# Add the Backend directory to sys.path to allow imports from src
sys.path.append(os.getcwd())

from sqlmodel import Session, select
from src.database.create_tables import engine, create_db_table
from src.database.models import User, UserRole, Doctor, CareTaker, Patient
from src.auth.hashing import get_password_hash

def seed():
    # Ensure tables exist
    create_db_table()
    
    with Session(engine) as session:
        # 1. ADMIN
        admin_data = {
            "username": "admin@neurobin.com",
            "email": "admin@neurobin.com",
            "password": "admin123",
            "role": UserRole.admin
        }
        
        # 2. DOCTOR
        doctor_data = {
            "username": "doctor@neurobin.com",
            "email": "doctor@neurobin.com",
            "password": "neurobin123",
            "role": UserRole.doctor,
            "profile": {
                "name": "Dr. Sarah Smith",
                "age": 45,
                "license_number": "DOC12345",
                "experience": 15,
                "degree": "MD Neurology",
                "phone": "+1-555-0101"
            }
        }
        
        # 3. CARETAKER
        caretaker_data = {
            "username": "caregiver@neurobin.com",
            "email": "caregiver@neurobin.com",
            "password": "neurobin123",
            "role": UserRole.caretaker,
            "profile": {
                "name": "James Wilson",
                "age": 32,
                "license_number": "CT998877",
                "experience": 5,
                "salary": 3500.0,
                "grade": "Senior",
                "phone": "+1-555-0202"
            }
        }
        
        # 4. PATIENTS
        patients_to_seed = [
            {
                "username": "patient@neurobin.com",
                "email": "patient@neurobin.com",
                "password": "neurobin123",
                "role": UserRole.patient,
                "profile": {
                    "name": "John Doe",
                    "age": 72,
                    "address": "123 Elm St, Springfield",
                    "medical_history": "Early stage Alzheimer's",
                    "phone": "+1-555-0303"
                }
            },
            {
                "username": "jane.doe@neurobin.com",
                "email": "jane.doe@neurobin.com",
                "password": "neurobin123",
                "role": UserRole.patient,
                "profile": {
                    "name": "Jane Doe",
                    "age": 68,
                    "address": "456 Oak Ave, Riverside",
                    "medical_history": "Mild cognitive impairment",
                    "phone": "+1-555-0404"
                }
            }
        ]

        all_creds = []

        def create_user_and_profile(data):
            statement = select(User).where(User.username == data["username"])
            existing_user = session.exec(statement).first()
            if not existing_user:
                print(f"Creating user: {data['username']} ({data['role']})")
                user = User(
                    username=data["username"],
                    email=data["email"],
                    password=get_password_hash(data["password"]),
                    role=data["role"]
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                
                # Create profile if exists
                if "profile" in data:
                    if data["role"] == UserRole.doctor:
                        profile = Doctor(user_id=user.id, **data["profile"])
                    elif data["role"] == UserRole.caretaker:
                        profile = CareTaker(user_id=user.id, **data["profile"])
                    elif data["role"] == UserRole.patient:
                        profile = Patient(user_id=user.id, **data["profile"])
                    session.add(profile)
                
                all_creds.append(f"Email: {data['email']} | Pass: {data['password']} | Role: {data['role']}")
            else:
                print(f"User {data['username']} already exists.")

        create_user_and_profile(admin_data)
        create_user_and_profile(doctor_data)
        create_user_and_profile(caretaker_data)
        for p in patients_to_seed:
            create_user_and_profile(p)
        
        session.commit()
        
        # Write to pass.txt
        pass_path = "/home/gopal/Documents/NuroBin/pass.txt"
        with open(pass_path, "w") as f:
            f.write("\n".join(all_creds))
        print(f"Credentials written to {pass_path}")

if __name__ == "__main__":
    seed()
