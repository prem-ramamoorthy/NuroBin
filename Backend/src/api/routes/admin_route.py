from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database.create_tables import get_session
from src.database.crud import (
    create_user,
    create_doctor,
    create_caretaker,
    create_patient,
    delete_user,
    get_users,
)
from src.database.models import UserRole
from src.database.schemas import (
    UserCreate,
    DoctorCreate,
    CareTakerCreate,
    PatientCreate,
    UserRead,
)
from src.api.models import RegisterDoctor, RegisterCareTaker, RegisterPatient, UserApi
from src.auth.util import get_current_active_user, require_role
from typing import Annotated

admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Dependency to ensure the user is an admin
admin_only = Depends(require_role(UserRole.admin))

@admin_router.get("/users", response_model=list[UserRead])
async def list_all_users(
    current_user: Annotated[UserApi, admin_only],
    session: Session = Depends(get_session)
):
    return get_users(session)

@admin_router.post("/register/doctor", status_code=status.HTTP_201_CREATED)
async def admin_register_doctor(
    doctor_in: RegisterDoctor,
    current_user: Annotated[UserApi, admin_only],
    session: Session = Depends(get_session)
):
    u_in = UserCreate.model_validate(doctor_in.model_dump(), update={"role": UserRole.doctor})
    user = create_user(session, u_in)
    
    d_in = DoctorCreate.model_validate(doctor_in.model_dump(), update={"user_id": user.id})
    return create_doctor(session, d_in)

@admin_router.post("/register/caretaker", status_code=status.HTTP_201_CREATED)
async def admin_register_caretaker(
    caretaker_in: RegisterCareTaker,
    current_user: Annotated[UserApi, admin_only],
    session: Session = Depends(get_session)
):
    u_in = UserCreate.model_validate(caretaker_in.model_dump(), update={"role": UserRole.caretaker})
    user = create_user(session, u_in)
    
    c_in = CareTakerCreate.model_validate(caretaker_in.model_dump(), update={"user_id": user.id})
    return create_caretaker(session, c_in)

@admin_router.post("/register/patient", status_code=status.HTTP_201_CREATED)
async def admin_register_patient(
    patient_in: RegisterPatient,
    current_user: Annotated[UserApi, admin_only],
    session: Session = Depends(get_session)
):
    u_in = UserCreate.model_validate(patient_in.model_dump(), update={"role": UserRole.patient})
    user = create_user(session, u_in)
    
    p_in = PatientCreate.model_validate(patient_in.model_dump(), update={"user_id": user.id})
    return create_patient(session, p_in)

@admin_router.delete("/user/{user_id}")
async def admin_delete_user(
    user_id: int,
    current_user: Annotated[UserApi, admin_only],
    session: Session = Depends(get_session)
):
    deleted = delete_user(session, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully", "user": deleted}
