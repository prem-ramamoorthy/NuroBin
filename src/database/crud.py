from typing import Tuple
from sqlmodel import Session, select
from src.database.models import Patient, Doctor, CareTaker, User
from src.database.schemas import (
    PatientCreate,
    PatientRead,
    PatientUpdate,
    DoctorCreate,
    DoctorRead,
    DoctorUpdate,
    CareTakerCreate,
    CareTakerRead,
    CareTakerUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
)


def create_user(session: Session, user_in: UserCreate) -> UserRead:
    user = User.model_validate(user_in)

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserRead.model_validate(user)


def get_user(session: Session, user_id: str) -> UserRead | None:
    user = session.get(User, user_id)
    return UserRead.model_validate(user) if user else None


def get_user_username(session: Session, username: str) -> UserRead | None:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return UserRead.model_validate(user) if user else None


def get_user_auth(
    session: Session, username: str
) -> Tuple[str, str] | Tuple[None, None]:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return (user.username, user.password) if user else (None, None)


def get_users(session: Session) -> list[UserRead]:
    users = session.exec(select(User)).all()
    return [UserRead.model_validate(u) for u in users]


def update_user(session: Session, user_id: int, user_in: UserUpdate) -> UserRead | None:
    user = session.get(User, user_id)
    if not user:
        return None

    update_data = user_in.model_dump(exclude_unset=True)
    user.sqlmodel_update(update_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserRead.model_validate(user)


def delete_user(session: Session, user_id: int) -> UserRead | None:
    user = session.get(User, user_id)
    if not user:
        return None
    session.delete(user)
    session.commit()
    return UserRead.model_validate(user)


def create_patient(
    session: Session,
    patient_in: PatientCreate,
) -> PatientRead:
    patient = Patient.model_validate(patient_in)

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return PatientRead.model_validate(patient)


def get_patients(session: Session) -> list[PatientRead]:
    patients = session.exec(select(Patient)).all()
    return [PatientRead.model_validate(p) for p in patients]


def get_patient(
    session: Session,
    patient_id: int,
) -> PatientRead | None:
    patient = session.get(Patient, patient_id)
    return PatientRead.model_validate(patient) if patient else None


def update_patient(
    session: Session,
    patient_id: int,
    patient_in: PatientUpdate,
) -> PatientRead | None:
    patient = session.get(Patient, patient_id)
    if not patient:
        return None

    update_data = patient_in.model_dump(exclude_unset=True)
    patient.sqlmodel_update(update_data)

    session.add(patient)
    session.commit()
    session.refresh(patient)

    return PatientRead.model_validate(patient)


def delete_patient(
    session: Session,
    patient_id: int,
) -> PatientRead | None:
    patient = session.get(Patient, patient_id)
    if not patient:
        return None
    val = PatientRead.model_validate(patient) if patient else None
    session.delete(patient)
    session.commit()
    return val


def create_doctor(
    session: Session,
    doctor_in: DoctorCreate,
) -> DoctorRead:
    doctor = Doctor.model_validate(doctor_in)

    session.add(doctor)
    session.commit()
    session.refresh(doctor)

    return DoctorRead.model_validate(doctor)


def get_doctors(session: Session) -> list[DoctorRead]:
    doctors = session.exec(select(Doctor)).all()
    return [DoctorRead.model_validate(d) for d in doctors]


def get_doctor(doctor_id, session: Session) -> DoctorRead | None:
    doctor = session.get(Doctor, doctor_id)
    return DoctorRead.model_validate(doctor) if doctor else None


def update_doctor(
    session: Session,
    doctor_id: int,
    doctor_in: DoctorUpdate,
) -> DoctorRead | None:
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        return None

    update_data = doctor_in.model_dump(exclude_unset=True)
    doctor.sqlmodel_update(update_data)

    session.add(doctor)
    session.commit()
    session.refresh(doctor)

    return DoctorRead.model_validate(doctor)


def delete_doctor(session: Session, doctor_id: int) -> DoctorRead | None:
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        return None
    val = DoctorRead.model_validate(doctor) if doctor else None
    session.delete(doctor)
    session.commit()
    return val


def create_caretaker(
    session: Session,
    caretaker_in: CareTakerCreate,
) -> CareTakerRead:
    caretaker = CareTaker.model_validate(caretaker_in)

    session.add(caretaker)
    session.commit()
    session.refresh(caretaker)

    return CareTakerRead.model_validate(caretaker)


def get_caretaker(caretaker_id: int, session: Session) -> CareTakerRead | None:
    caretaker = session.get(CareTaker, caretaker_id)
    return CareTakerRead.model_validate(caretaker) if caretaker else None


def get_caretakers(session: Session) -> list[CareTakerRead]:
    caretakers = session.exec(select(CareTaker)).all()
    return [CareTakerRead.model_validate(c) for c in caretakers]


def update_caretaker(
    session: Session,
    caretaker_id: int,
    caretaker_in: CareTakerUpdate,
) -> CareTakerRead | None:
    caretaker = session.get(CareTaker, caretaker_id)
    if not caretaker:
        return None

    update_data = caretaker_in.model_dump(exclude_unset=True)
    caretaker.sqlmodel_update(update_data)

    session.add(caretaker)
    session.commit()
    session.refresh(caretaker)

    return CareTakerRead.model_validate(caretaker)


def delete_caretaker(session: Session, caretaker_id: int) -> CareTakerRead | None:
    caretaker = session.get(CareTaker, caretaker_id)
    if not caretaker:
        return None
    val = CareTakerRead.model_validate(caretaker) if caretaker else None
    session.delete(caretaker)
    session.commit()
    return val
