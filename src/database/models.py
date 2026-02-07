from typing import Optional
from sqlmodel import Field, SQLModel


class Patient(SQLModel, table=True):
    id: int | None = Field(default=0, primary_key=True)
    name: str
    age: int | None = None
    address: str
    medical_history: str | None = None
    phone: str
    email: Optional[str]


class Doctor(SQLModel, table=True):
    id: int | None = Field(default=0, primary_key=True)
    name: str
    age: int | None = None
    license_number: str
    experience: int
    degree: str
    phone: str
    email: str


class CareTaker(SQLModel, table=True):
    id: int | None = Field(default=0, primary_key=True)
    name: str
    age: int | None = None
    license_number: str
    experience: int
    salary: float
    grade: str
    phone: str
