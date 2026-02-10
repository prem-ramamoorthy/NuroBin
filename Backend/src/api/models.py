from pydantic import BaseModel

from src.database.models import UserRole


class UserApi(BaseModel):
    username: str
    email: str
    role: UserRole
    is_active: bool


class RegisterPatient(BaseModel):
    username: str
    email: str
    password: str
    name: str
    age: int
    address: str
    medical_history: str | None
    phone: str


class RegisterDoctor(BaseModel):
    username: str
    email: str
    password: str
    name: str
    age: int
    license_number: str
    experience: int
    degree: str
    phone: str


class RegisterCareTaker(BaseModel):
    username: str
    email: str
    password: str
    name: str
    age: int
    license_number: str
    experience: int
    salary: float
    grade: str
    phone: str
