from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from src.api.models import UserApi, RegisterPatient
from src.auth.util import get_current_active_user
from src.database.create_tables import get_session
from src.database.crud import (
    create_caretaker_patient_link,
    create_patient,
    create_user,
    delete_patient,
    get_patient,
    get_patients,
    update_patient,
)
from src.database.models import CaretakerPatientLink, CareTaker, UserRole
from src.database.schemas import (
    CaretakerPatientLinkCreate,
    PatientCreate,
    PatientRead,
    PatientUpdate,
    UserCreate,
)
from typing import Annotated

patient_router = APIRouter(prefix="/patients", tags=["patients"])


@patient_router.post("/", response_model=PatientRead)
async def add_patient(
    patient: RegisterPatient,
    current_user: Annotated[UserApi, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    user_in = UserCreate.model_validate_json(patient.model_dump_json(), extra="ignore")
    patient_in = PatientCreate.model_validate_json(
        patient.model_dump_json(), extra="ignore"
    )
    user_in.sqlmodel_update({"role": UserRole.patient})
    
    # Create the user (crud.create_user now handles hashing)
    user = create_user(session, user_in)
    
    # Associate user with patient
    patient_in.sqlmodel_update({"user_id": user.id})
    new_patient = create_patient(session, patient_in)
    
    # If the registrant is a caretaker, automatically link them
    if current_user.role == UserRole.caretaker:
        # We need the caretaker record's ID (not the user ID)
        caretaker_stmt = select(CareTaker).where(CareTaker.user_id == current_user.id)
        caretaker = session.exec(caretaker_stmt).first()
        if caretaker:
            link_in = CaretakerPatientLinkCreate(
                caretaker_id=caretaker.id,
                patient_id=new_patient.id,
                is_primary=True
            )
            create_caretaker_patient_link(session, link_in)
            
    return new_patient


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
