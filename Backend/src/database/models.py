from enum import Enum
from typing import Any, cast
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from pgvector.sqlalchemy import VECTOR


class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    caretaker = "caretaker"
    admin = "admin"


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
    name: str | None
    relation: str | None
    phone: str | None = None
    notes: str | None = None  # Specifically for Memory Triggers
    photo_url: str | None = None


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
    embedding: Any = Field(sa_type=cast(type[Any], VECTOR(128)))


class MeetingStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class Meeting(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    doctor_id: int = Field(foreign_key="doctor.id")
    caretaker_id: int | None = Field(default=None, foreign_key="caretaker.id")
    scheduled_time: datetime
    duration_minutes: int | None = 30
    status: MeetingStatus = MeetingStatus.scheduled
    notes: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DoctorPatientLink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key="doctor.id")
    patient_id: int = Field(foreign_key="patient.id")
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_primary: bool = False


class CaretakerPatientLink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    caretaker_id: int = Field(foreign_key="caretaker.id")
    patient_id: int = Field(foreign_key="patient.id")
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    shift: str | None = None
    is_primary: bool = False
