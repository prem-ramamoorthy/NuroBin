from typing import Optional
from sqlmodel import SQLModel


class PatientCreate(SQLModel):
    name: str
    age: int
    address: str
    medical_history: Optional[str]
    phone: str
    email: Optional[str]


class PatientRead(SQLModel):
    id: int
    name: str
    address: str
    age: int
    medical_history: Optional[str]
    phone: str
    email: Optional[str]


class PatientUpdate(SQLModel):
    name: str | None
    age: int | None
    address: str | None
    medical_history: Optional[str]
    phone: str | None
    email: Optional[str]


class DoctorCreate(SQLModel):
    name: str
    age: int | None = None
    license_number: str
    experience: int
    degree: str
    phone: str
    email: str


class DoctorRead(SQLModel):
    id: int
    name: str
    age: int | None = None
    license_number: str
    experience: int
    degree: str
    phone: str
    email: str


class DoctorUpdate(SQLModel):
    id: int | None
    name: str | None
    age: int | None = None
    license_number: str | None
    experience: int | None
    degree: str | None
    phone: str | None
    email: str | None


class CareTakerCreate(SQLModel):
    name: str
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
    id: int | None
    name: str | None
    age: int | None = None
    license_number: str | None
    experience: int | None
    salary: float | None
    grade: str | None
    phone: str | None
