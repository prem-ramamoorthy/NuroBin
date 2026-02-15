from enum import Enum
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
    place_type: str | None = None # hospital, pharmacy, etc.
    geofence_radius_m: int = 150
    created_at: float | None = None
