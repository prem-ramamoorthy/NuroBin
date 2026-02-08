from typing import Optional
from sqlmodel import SQLModel

from src.database.models import UserRole


class UserCreate(SQLModel):
    username: str
    email: str
    password: str
    role: UserRole | None = None


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool


class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    role: UserRole | None = None


class PatientCreate(SQLModel):
    name: str
    user_id: int | None = None
    age: int
    address: str
    medical_history: Optional[str]
    phone: str


class PatientRead(SQLModel):
    id: int
    name: str
    address: str
    age: int
    medical_history: Optional[str]
    phone: str


class PatientUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    address: str | None = None
    medical_history: str | None = None
    phone: str | None = None


class DoctorCreate(SQLModel):
    name: str
    user_id: int | None = None
    age: int | None = None
    license_number: str
    experience: int
    degree: str
    phone: str


class DoctorRead(SQLModel):
    id: int
    name: str
    age: int | None = None
    license_number: str
    experience: int
    degree: str
    phone: str


class DoctorUpdate(SQLModel):
    id: int | None = None
    name: str | None = None
    age: int | None = None
    license_number: str | None = None
    experience: int | None = None
    degree: str | None = None
    phone: str | None = None


class CareTakerCreate(SQLModel):
    name: str
    user_id: int | None = None
    age: int | None = None
    license_number: str
    experience: int
    salary: float
    grade: str
    phone: str


class CareTakerRead(SQLModel):
    id: int
    name: str
    age: int | None = None
    license_number: str
    experience: int
    salary: float
    grade: str
    phone: str


class CareTakerUpdate(SQLModel):
    id: int | None = None
    name: str | None = None
    age: int | None = None
    license_number: str | None = None
    experience: int | None = None
    salary: float | None = None
    grade: str | None = None
    phone: str | None = None
