from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.api.models import RegisterDoctor
from src.database.create_tables import get_session
from src.database.crud import (
    create_doctor,
    create_user,
    delete_doctor,
    get_doctor,
    get_doctors,
    update_doctor,
)
from src.database.models import UserRole
from src.database.schemas import DoctorCreate, DoctorRead, DoctorUpdate, UserCreate

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
