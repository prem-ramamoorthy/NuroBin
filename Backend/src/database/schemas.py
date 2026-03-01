from typing import Optional, Union
import numpy
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


class FamilyMemberCreate(SQLModel):
    patient_id: int
    name: str | None
    relation: str | None
    phone: str | None = None


class FamilyMemberRead(SQLModel):
    id: int
    patient_id: int
    name: str
    relation: str
    phone: str | None


class FamilyMemberUpdate(SQLModel):
    name: str | None = None
    relation: str | None = None
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


class LocationCreate(SQLModel):
    name: str
    latitude: float
    longitude: float


class LocationRead(SQLModel):
    id: int
    name: str
    latitude: float
    longitude: float


class LocationUpdate(SQLModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class PlaceCreate(SQLModel):
    name: str
    user_id: int
    lat: float
    lng: float
    place_type: str | None = None
    geofence_radius_m: int = 150
    created_at: float | None = None


class PlaceRead(SQLModel):
    id: int
    name: str
    user_id: int
    lat: float
    lng: float
    place_type: str | None = None
    geofence_radius_m: int
    created_at: float | None = None


class PlaceUpdate(SQLModel):
    name: str | None = None
    user_id: int | None = None
    lat: float | None = None
    lng: float | None = None
    place_type: str | None = None
    geofence_radius_m: int | None = None
    created_at: float | None = None


class FaceEmbeddingCreate(SQLModel):
    family_member: int
    embedding: Union[list[float], numpy.typing.NDArray]


class FaceEmbeddingRead(SQLModel):
    id: int
    family_member: int
