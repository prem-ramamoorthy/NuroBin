from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.api.models import RegisterDoctor, UserApi
from src.auth.util import get_current_active_user, require_role
from src.database.create_tables import get_session
from src.database.crud import (
    create_caretaker_patient_link,
    create_doctor,
    create_user,
    delete_caretaker,
    delete_patient,
    delete_user,
    get_caretaker,
    get_caretakers,
    get_doctor,
    get_doctors,
    get_patient,
    get_patients,
    update_doctor,
)
from src.database.models import CaretakerPatientLink, UserRole
from src.database.schemas import (
    CaretakerPatientLinkCreate,
    DoctorCreate,
    DoctorRead,
    DoctorUpdate,
    UserCreate,
)
from typing import Annotated

doctor_router = APIRouter(prefix="/doctors", tags=["doctors"])


@doctor_router.post("/", response_model=DoctorRead)
async def add_doctor(doctor: RegisterDoctor, session: Session = Depends(get_session)):
    user_in = UserCreate.model_validate_json(doctor.model_dump_json(), extra="ignore")
    doctor_in = DoctorCreate.model_validate_json(
        doctor.model_dump_json(), extra="ignore"
    )
    user_in.sqlmodel_update({"role": UserRole.doctor})
    user = create_user(session, user_in)
    doctor_in.sqlmodel_update({"user_id": user.id})
    return create_doctor(session, doctor_in)


@doctor_router.get("/{doctor_id}", response_model=DoctorRead)
async def read_doctor(doctor_id, session: Session = Depends(get_session)):
    return get_doctor(session, doctor_id=doctor_id)


@doctor_router.get("/", response_model=list[DoctorRead])
async def read_all_doctors(session: Session = Depends(get_session)):
    return get_doctors(session)


@doctor_router.patch("/{doctor_id}", response_model=DoctorRead)
async def patch_doctor(
    doctor_id: int, doctor: DoctorUpdate, session: Session = Depends(get_session)
):
    return update_doctor(session, doctor_id, doctor)


@doctor_router.delete("/{doctor_id}", response_model=DoctorRead)
async def remove_doctor(doctor_id: int, session: Session = Depends(get_session)):
    return delete_doctor(session, doctor_id)

# Doctor authority to manage other accounts
doctor_only = Depends(require_role(UserRole.doctor))

@doctor_router.delete("/manage/patient/{patient_id}")
async def doctor_delete_patient(
    patient_id: int,
    current_user: Annotated[UserApi, doctor_only],
    session: Session = Depends(get_session)
):
    # Need to delete the user record associated with the patient
    patient = get_patient(session, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    delete_user(session, patient.user_id) # cascade or manual
    return {"message": "Patient account removed"}

@doctor_router.delete("/manage/caretaker/{caretaker_id}")
async def doctor_delete_caretaker(
    caretaker_id: int,
    current_user: Annotated[UserApi, doctor_only],
    session: Session = Depends(get_session)
):
    caretaker = get_caretaker(session, caretaker_id)
    if not caretaker:
        raise HTTPException(status_code=404, detail="Caretaker not found")
    delete_user(session, caretaker.user_id)
    return {"message": "Caretaker account removed"}

@doctor_router.post("/manage/link-caretaker")
async def doctor_link_caretaker(
    link_in: CaretakerPatientLinkCreate,
    current_user: Annotated[UserApi, doctor_only],
    session: Session = Depends(get_session)
):
    return create_caretaker_patient_link(session, link_in)

@doctor_router.delete("/manage/unlink-caretaker/{patient_id}/{caretaker_id}")
async def doctor_unlink_caretaker(
    patient_id: int,
    caretaker_id: int,
    current_user: Annotated[UserApi, doctor_only],
    session: Session = Depends(get_session)
):
    statement = select(CaretakerPatientLink).where(
        CaretakerPatientLink.patient_id == patient_id,
        CaretakerPatientLink.caretaker_id == caretaker_id
    )
    link = session.exec(statement).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    session.delete(link)
    session.commit()
    return {"message": "Caretaker unlinked from patient"}
