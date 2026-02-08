from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    caretaker = "caretaker"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str
    password: str
    role: UserRole
    is_active: bool = True


class Patient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    name: str
    age: int | None = None
    address: str
    medical_history: str | None = None
    phone: str


class Doctor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    name: str
    age: int | None = None
    license_number: str
    experience: int
    degree: str
    phone: str


class CareTaker(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    name: str
    age: int | None = None
    license_number: str
    experience: int
    salary: float
    grade: str
    phone: str
