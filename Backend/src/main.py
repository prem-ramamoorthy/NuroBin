from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import (
    OAuth2PasswordRequestFormStrict,
)
from sqlmodel.orm.session import Session
from fastapi.middleware.cors import CORSMiddleware

from src.api.models import RegisterCareTaker, RegisterDoctor, RegisterPatient, UserApi
from src.auth.jwt_auth import Token, create_access_token
from src.auth.util import authenticate_user, get_current_user, require_role
from src.config.config_env import Config
from src.database.create_tables import create_db_table, get_session
from src.database.crud import (
    create_caretaker,
    create_doctor,
    create_patient,
    create_user,
    delete_caretaker,
    delete_doctor,
    delete_patient,
    get_caretaker,
    get_caretakers,
    get_doctor,
    get_doctors,
    get_patient,
    get_patients,
    update_caretaker,
    update_doctor,
    update_patient,
)
from src.database.models import UserRole
from src.database.schemas import (
    CareTakerCreate,
    CareTakerRead,
    CareTakerUpdate,
    DoctorCreate,
    DoctorRead,
    DoctorUpdate,
    PatientCreate,
    PatientRead,
    PatientUpdate,
    UserCreate,
)
from src.gmaps.gmapsRouter import app as gmaps_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_table()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gmaps_router, prefix="/gmaps", tags=["gmaps"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the NuroBin Backend API!",
        "endpoints": [
            "/patients/",
            "/doctors/",
            "/caretaker/",
            "/gmaps/",
            "/users/me",
            "/token",
            "/profile",
        ],
        "description": "This API allows you to manage patients, doctors, and caretakers. You can create, read, update, and delete records for each of these entities. Additionally, you can authenticate users and access protected endpoints based on their roles.",
        "health": "OK",
    }


@app.post("/patients/", response_model=PatientRead)
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


@app.get("/patients/{patient_id}", response_model=PatientRead)
async def read_patient(patient_id: int, session: Session = Depends(get_session)):
    return get_patient(session, patient_id)


@app.get("/patients/", response_model=list[PatientRead])
async def read_all_patient(session: Session = Depends(get_session)):
    return get_patients(session)


@app.patch("/patients/{patient_id}", response_model=PatientRead)
async def patch_patient(
    patient_id: int, patient: PatientUpdate, session: Session = Depends(get_session)
):
    return update_patient(session, patient_id, patient)


@app.delete("/patients/{patient_id}", response_model=PatientRead)
async def remove_patient(patient_id, session: Session = Depends(get_session)):
    return delete_patient(session, patient_id)


@app.post("/doctors/", response_model=DoctorRead)
async def add_doctor(doctor: RegisterDoctor, session: Session = Depends(get_session)):
    user_in = UserCreate.model_validate_json(doctor.model_dump_json(), extra="ignore")
    doctor_in = DoctorCreate.model_validate_json(
        doctor.model_dump_json(), extra="ignore"
    )
    user_in.sqlmodel_update({"role": UserRole.doctor})
    user = create_user(session, user_in)
    doctor_in.sqlmodel_update({"user_id": user.id})
    return create_doctor(session, doctor_in)


@app.get("/doctors/{doctor_id}", response_model=DoctorRead)
async def read_doctor(doctor_id, session: Session = Depends(get_session)):
    return get_doctor(doctor_id, session)


@app.get("/doctors/", response_model=list[DoctorRead])
async def read_all_doctors(session: Session = Depends(get_session)):
    return get_doctors(session)


@app.patch("/doctors/{doctor_id}", response_model=DoctorRead)
async def patch_doctor(
    doctor_id: int, doctor: DoctorUpdate, session: Session = Depends(get_session)
):
    return update_doctor(session, doctor_id, doctor)


@app.delete("/doctors/{doctor_id}", response_model=DoctorRead)
async def remove_doctor(doctor_id: int, session: Session = Depends(get_session)):
    return delete_doctor(session, doctor_id)


@app.post("/caretaker/", response_model=CareTakerRead)
async def add_caretaker(
    caretaker: RegisterCareTaker, session: Session = Depends(get_session)
):
    user_in = UserCreate.model_validate_json(
        caretaker.model_dump_json(), extra="ignore"
    )
    caretaker_in = CareTakerCreate.model_validate_json(
        caretaker.model_dump_json(), extra="ignore"
    )
    user_in.sqlmodel_update({"role": UserRole.caretaker})
    user = create_user(session, user_in)
    caretaker_in.sqlmodel_update({"user_id": user.id})
    return create_caretaker(session, caretaker_in)


@app.get("/caretaker/{caretaker_id}", response_model=CareTakerRead)
async def read_caretaker(caretaker_id: int, session: Session = Depends(get_session)):
    return get_caretaker(caretaker_id, session)


@app.get("/caretaker/", response_model=list[CareTakerRead])
async def read_all_caretakers(session: Session = Depends(get_session)):
    return get_caretakers(session)


@app.patch("/caretaker/{caretaker_id}", response_model=CareTakerRead)
async def patch_caretaker(
    caretaker_id: int,
    caretaker: CareTakerUpdate,
    session: Session = Depends(get_session),
):
    return update_caretaker(session, caretaker_id, caretaker)


@app.delete("/caretaker/{caretaker_id}", response_model=CareTakerRead)
async def remove_caretaker(caretaker_id: int, session: Session = Depends(get_session)):
    return delete_caretaker(session, caretaker_id)


@app.get("/users/me")
async def read_users_me(current_user: Annotated[UserApi, Depends(get_current_user)]):
    return current_user


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    session: Session = Depends(get_session),
):
    username = authenticate_user(session, form_data.username, form_data.password)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=float(Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/profile")
async def profile(
    current_user: Annotated[
        UserApi, Depends(require_role(UserRole.patient, UserRole.doctor))
    ],
):
    return current_user
