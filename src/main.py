from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlmodel.orm.session import Session

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
    update_user,
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_table()
    yield


app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class RegisterPatient(BaseModel):
    username: str
    email: str
    password: str
    name: str
    age: int
    address: str
    medical_history: str | None
    phone: str


class RegisterDoctor(BaseModel):
    username: str
    email: str
    password: str
    name: str
    age: int
    license_number: str
    experience: int
    degree: str
    phone: str


class RegisterCareTaker(BaseModel):
    username: str
    email: str
    password: str
    name: str
    age: int
    license_number: str
    experience: int
    salary: float
    grade: str
    phone: str


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
