from src.auth.util import get_password_hash
from src.database.models import User, UserRole


def test_profile_patient_success(client, session):
    user = User(
        username="patient1",
        email="patient1@example.com",
        password=get_password_hash("password123"),
        role=UserRole.patient,
        is_active=True,
    )
    session.add(user)
    session.commit()

    token_response = client.post(
        "/token",
        data={
            "username": "patient1",
            "password": "password123",
            "grant_type": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    access_token = token_response.json()["access_token"]

    response = client.get(
        "/profile",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "patient1"
    assert data["role"] == UserRole.patient


def test_profile_doctor_success(client, session):
    user = User(
        username="doctor1",
        email="doctor1@example.com",
        password=get_password_hash("password123"),
        role=UserRole.doctor,
        is_active=True,
    )
    session.add(user)
    session.commit()

    token_response = client.post(
        "/token",
        data={
            "username": "doctor1",
            "password": "password123",
            "grant_type": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    access_token = token_response.json()["access_token"]

    response = client.get(
        "/profile",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "doctor1"
    assert data["role"] == UserRole.doctor


def test_profile_forbidden_role(client, session):
    user = User(
        username="admin1",
        email="admin1@example.com",
        password=get_password_hash("password123"),
        role=UserRole.caretaker,
        is_active=True,
    )
    session.add(user)
    session.commit()

    token_response = client.post(
        "/token",
        data={
            "username": "admin1",
            "password": "password123",
            "grant_type": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    access_token = token_response.json()["access_token"]

    response = client.get(
        "/profile",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


def test_profile_unauthorized(client):
    response = client.get("/profile")

    assert response.status_code == 401
