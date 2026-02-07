from src.database.crud import (
    create_caretaker,
    create_doctor,
    create_patient,
    get_patient,
    update_doctor,
    update_patient,
    delete_patient,
)
from src.database.schemas import CareTakerCreate, DoctorCreate, PatientCreate


def test_create_patient(session):
    patient_in = PatientCreate(
        name="John Doe",
        age=40,
        address="123 Main St",
        phone="555-1234",
        email="john@example.com",
        medical_history="Diabetes",
    )

    patient = create_patient(session, patient_in)

    assert patient.id is not None
    assert patient.name == "John Doe"


def test_update_patient(session):
    patient = create_patient(
        session,
        PatientCreate(
            name="Old Name",
            age=30,
            address="Old Addr",
            phone="111",
            email="old@mail.com",
            medical_history="",
        ),
    )

    updated = update_patient(
        session,
        patient.id,
        PatientCreate(
            name="New Name",
            age=31,
            address="New Addr",
            phone="222",
            email="new@mail.com",
            medical_history="",
        ),
    )

    assert updated.name == "New Name"
    assert updated.age == 31


def test_delete_patient(session):
    patient = create_patient(
        session,
        PatientCreate(
            name="Delete Me",
            address="X",
            phone="999",
            email="x@y.com",
            age=10,
            medical_history="",
        ),
    )

    deleted = delete_patient(session, patient.id)

    assert deleted.id == patient.id
    assert get_patient(session, patient.id) is None


def test_create_doctor(session):
    doctor = create_doctor(
        session,
        DoctorCreate(
            name="Dr Strange",
            age=45,
            license_number="LIC123",
            experience=20,
            degree="MD",
            phone="555-2222",
            email="doc@hospital.com",
        ),
    )

    assert doctor.id is not None


def test_update_doctor(session):
    doctor = create_doctor(
        session,
        DoctorCreate(
            name="Dr Old",
            license_number="OLD1",
            experience=10,
            degree="MBBS",
            phone="111",
            email="old@doc.com",
        ),
    )

    updated = update_doctor(
        session,
        doctor.id,
        DoctorCreate(
            name="Dr New",
            license_number="NEW1",
            experience=15,
            degree="MD",
            phone="222",
            email="new@doc.com",
        ),
    )

    assert updated.license_number == "NEW1"


def test_create_caretaker(session):
    caretaker = create_caretaker(
        session,
        CareTakerCreate(
            name="Helper",
            license_number="CARE1",
            experience=5,
            salary=35000.0,
            grade="A",
            phone="555",
        ),
    )

    assert caretaker.id is not None
