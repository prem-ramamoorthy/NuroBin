from enum import Enum
from sqlmodel import Column, Field, SQLModel
from pgvector.sqlalchemy import Vector


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


class FamilyMember(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    name: str
    relation: str
    phone: str | None = None


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


class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    latitude: float
    longitude: float
    timestamp: float
    created_at: float | None = None


class Place(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(index=True, unique=True)
    lat: float
    lng: float
    place_type: str | None = None  # hospital, pharmacy, etc.
    geofence_radius_m: int = 150
    created_at: float | None = None


class FaceEmbedding(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    family_member: int = Field(foreign_key="familymember.id")
    embedding: list[float] = Field(sa_column=Column(Vector(512)))
