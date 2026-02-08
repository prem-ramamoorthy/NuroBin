from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlmodel.orm.session import Session

from src.database.create_tables import create_db_table, get_session
from src.database.crud import (
    create_caretaker,
    create_doctor,
    create_patient,
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
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_table()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/patients/", response_model=PatientRead)
def add_patient(patient: PatientCreate, session: Session = Depends(get_session)):
    return create_patient(session, patient)


@app.get("/patients/{patient_id}", response_model=PatientRead)
def read_patient(patient_id: int, session: Session = Depends(get_session)):
    return get_patient(session, patient_id)


@app.get("/patients/", response_model=list[PatientRead])
def read_all_patient(session: Session = Depends(get_session)):
    return get_patients(session)


@app.patch("/patients/{patient_id}", response_model=PatientRead)
def patch_patient(
    patient_id: int, patient: PatientUpdate, session: Session = Depends(get_session)
):
    return update_patient(session, patient_id, patient)


@app.delete("/patients/{patient_id}", response_model=PatientRead)
def remove_patient(patient_id, session: Session = Depends(get_session)):
    return delete_patient(session, patient_id)


@app.post("/doctors/", response_model=DoctorRead)
def add_doctor(doctor: DoctorCreate, session: Session = Depends(get_session)):
    return create_doctor(session, doctor)


@app.get("/doctors/{doctor_id}", response_model=DoctorRead)
def read_doctor(doctor_id, session: Session = Depends(get_session)):
    return get_doctor(doctor_id, session)


@app.get("/doctors/", response_model=list[DoctorRead])
def read_all_doctors(session: Session = Depends(get_session)):
    return get_doctors(session)


@app.patch("/doctors/{doctor_id}", response_model=DoctorRead)
def patch_doctor(
    doctor_id: int, doctor: DoctorUpdate, session: Session = Depends(get_session)
):
    return update_doctor(session, doctor_id, doctor)


@app.delete("/doctors/{doctor_id}", response_model=DoctorRead)
def remove_doctor(doctor_id: int, session: Session = Depends(get_session)):
    return delete_doctor(session, doctor_id)


@app.post("/caretaker/", response_model=CareTakerRead)
def add_caretaker(caretaker: CareTakerCreate, session: Session = Depends(get_session)):
    return create_caretaker(session, caretaker)


@app.get("/caretaker/{caretaker_id}", response_model=CareTakerRead)
def read_caretaker(caretaker_id: int, session: Session = Depends(get_session)):
    return get_caretaker(caretaker_id, session)


@app.get("/caretaker/", response_model=list[CareTakerRead])
def read_all_caretakers(session: Session = Depends(get_session)):
    return get_caretakers(session)


@app.patch("/caretaker/{caretaker_id}", response_model=CareTakerRead)
def patch_caretaker(
    caretaker_id: int,
    caretaker: CareTakerUpdate,
    session: Session = Depends(get_session),
):
    return update_caretaker(session, caretaker_id, caretaker)


@app.delete("/caretaker/{caretaker_id}", response_model=CareTakerRead)
def remove_caretaker(caretaker_id: int, session: Session = Depends(get_session)):
    return delete_caretaker(session, caretaker_id)
