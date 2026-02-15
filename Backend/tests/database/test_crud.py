import pytest
from sqlalchemy.exc import IntegrityError

from src.database.crud import (
    create_place,
    create_caretaker,
    create_doctor,
    create_patient,
    create_user,
    get_place,
    delete_user,
    get_patient,
    get_user_username,
    get_users,
    update_doctor,
    update_patient,
    delete_patient,
    update_user,
)
from src.database.models import UserRole
from src.database.schemas import (
    CareTakerCreate,
    DoctorCreate,
    DoctorUpdate,
    PatientCreate,
    PatientUpdate,
    PlaceCreate,
    UserCreate,
    UserUpdate,
)


def test_create_user(session):
    user_in = UserCreate(
        username="johndoe",
        email="john@example.com",
        password="secret123",
        role=UserRole.patient,
    )

    user = create_user(session, user_in)

    assert user.id is not None
    assert user.username == "johndoe"
    assert user.email == "john@example.com"
    assert user.is_active is True
    assert user.role is not None


def test_get_user(session):
    user = create_user(
        session,
        UserCreate(
            role=UserRole.patient,
            username="janedoe",
            email="jane@example.com",
            password="secret123",
        ),
    )

    fetched = get_user_username(session, user.username)

    assert fetched is not None
    assert fetched.id == user.id
    assert fetched.username == "janedoe"
    assert fetched.email == "jane@example.com"


def test_get_users(session):
    create_user(
        session,
        UserCreate(
            username="user1",
            email="u1@example.com",
            password="pass1",
            role=UserRole.patient,
        ),
    )

    create_user(
        session,
        UserCreate(
            username="user2",
            email="u2@example.com",
            password="pass2",
            role=UserRole.patient,
        ),
    )

    users = get_users(session)

    assert len(users) >= 2
    usernames = [u.username for u in users]
    assert "user1" in usernames
    assert "user2" in usernames


def test_update_user(session):
    user = create_user(
        session,
        UserCreate(
            username="olduser",
            email="old@example.com",
            password="oldpass",
            role=UserRole.patient,
        ),
    )

    updated = update_user(
        session,
        user.id,
        UserUpdate(
            username="newuser",
            email="new@example.com",
            role=UserRole.patient,
        ),
    )

    assert updated is not None
    assert updated.username == "newuser"
    assert updated.email == "new@example.com"
    assert updated.role == UserRole.patient


def test_update_user_not_found(session):
    updated = update_user(
        session,
        user_id=9999,
        user_in=UserUpdate(email="noone@example.com"),
    )

    assert updated is None


def test_delete_user(session):
    user = create_user(
        session,
        UserCreate(
            username="tobedeleted",
            email="delete@example.com",
            password="deletepass",
            role=UserRole.patient,
        ),
    )

    deleted = delete_user(session, user.id)

    assert deleted.id == user.id
    assert deleted.username == "tobedeleted"
    assert get_user_username(session, user.username) is None


def test_delete_user_not_found(session):
    deleted = delete_user(session, user_id=9999)

    assert deleted is None


def make_user(session):
    return create_user(
        session,
        UserCreate(
            username="xyz", email="yzw", password="abc", role=UserRole.caretaker
        ),
    )


def test_create_patient(session):
    user = make_user(session)
    patient_in = PatientCreate(
        name="John Doe",
        user_id=user.id,
        age=40,
        address="123 Main St",
        phone="555-1234",
        medical_history="Diabetes",
    )

    patient = create_patient(session, patient_in)

    assert patient.id is not None
    assert patient.name == "John Doe"


def test_update_patient(session):
    user = make_user(session)
    patient = create_patient(
        session,
        PatientCreate(
            name="Old Name",
            user_id=user.id,
            age=30,
            address="Old Addr",
            phone="111",
            medical_history="",
        ),
    )

    updated = update_patient(
        session,
        patient.id,
        PatientUpdate(
            name="New Name",
            age=31,
            address="New Addr",
            phone="222",
            medical_history="",
        ),
    )

    assert updated.name == "New Name"
    assert updated.age == 31


def test_delete_patient(session):
    user = make_user(session)
    patient = create_patient(
        session,
        PatientCreate(
            name="Delete Me",
            user_id=user.id,
            address="X",
            phone="999",
            age=10,
            medical_history="",
        ),
    )

    deleted = delete_patient(session, patient.id)

    assert deleted.id == patient.id
    assert get_patient(session, patient.id) is None


def test_create_doctor(session):
    user = make_user(session)
    doctor = create_doctor(
        session,
        DoctorCreate(
            name="Dr Strange",
            user_id=user.id,
            age=45,
            license_number="LIC123",
            experience=20,
            degree="MD",
            phone="555-2222",
        ),
    )

    assert doctor.id is not None


def test_update_doctor(session):
    user = make_user(session)
    doctor = create_doctor(
        session,
        DoctorCreate(
            name="Dr Old",
            user_id=user.id,
            license_number="OLD1",
            experience=10,
            degree="MBBS",
            phone="111",
        ),
    )

    updated = update_doctor(
        session,
        doctor.id,
        DoctorUpdate(
            name="Dr New",
            license_number="NEW1",
            experience=15,
            degree="MD",
            phone="222",
        ),
    )

    assert updated.license_number == "NEW1"


def test_create_caretaker(session):
    user = make_user(session)
    caretaker = create_caretaker(
        session,
        CareTakerCreate(
            user_id=user.id,
            name="Helper",
            license_number="CARE1",
            experience=5,
            salary=35000.0,
            grade="A",
            phone="555",
        ),
    )

    assert caretaker.id is not None


def test_create_place(session):
    user = make_user(session)
    place = create_place(
        session,
        PlaceCreate(
            name="home",
            user_id=user.id,
            lat=12.91,
            lng=77.59,
            place_type="home",
            geofence_radius_m=220,
        ),
    )

    assert place.id is not None
    assert place.user_id == user.id
    assert place.name == "home"
    assert place.lat == 12.91
    assert place.lng == 77.59
    assert place.geofence_radius_m == 220
    assert get_place(session, place.id) is not None


def test_create_place_duplicate_name_fails(session):
    user = make_user(session)
    create_place(
        session,
        PlaceCreate(
            name="unique-home",
            user_id=user.id,
            lat=12.91,
            lng=77.59,
            place_type="home",
        ),
    )

    with pytest.raises(IntegrityError):
        create_place(
            session,
            PlaceCreate(
                name="unique-home",
                user_id=user.id,
                lat=12.95,
                lng=77.61,
                place_type="office",
            ),
        )
