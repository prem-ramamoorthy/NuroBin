from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.api.models import RegisterPatient
from src.database.create_tables import get_session
from src.database.crud import (
    create_patient,
    create_user,
    delete_patient,
    get_patient,
    get_patients,
    update_patient,
)
from src.database.models import UserRole
from src.database.schemas import PatientCreate, PatientRead, PatientUpdate, UserCreate

patient_router = APIRouter(prefix="/patients", tags=["patients"])


@patient_router.post("/", response_model=PatientRead)
async def add_patient(
    patient: RegisterPatient, session: Session = Depends(get_session)
):
    user_in = UserCreate.model_validate_json(patient.model_dump_json(), extra="ignore")
    patient_in = PatientCreate.model_validate_json(
        patient.model_dump_json(), extra="ignore"
    )
    user_in.sqlmodel_update({"role": UserRole.patient})
    user = create_user(session, user_in)
    patient_in.sqlmodel_update({"user_id": user.id})
    return create_patient(session, patient_in)


@patient_router.get("/{patient_id}", response_model=PatientRead)
async def read_patient(patient_id: int, session: Session = Depends(get_session)):
    return get_patient(session, patient_id)


@patient_router.get("/", response_model=list[PatientRead])
async def read_all_patient(session: Session = Depends(get_session)):
    return get_patients(session)


@patient_router.patch("/{patient_id}", response_model=PatientRead)
async def patch_patient(
    patient_id: int, patient: PatientUpdate, session: Session = Depends(get_session)
):
    return update_patient(session, patient_id, patient)


@patient_router.delete("/{patient_id}", response_model=PatientRead)
async def remove_patient(patient_id, session: Session = Depends(get_session)):
    return delete_patient(session, patient_id)
