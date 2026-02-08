from src.auth.util import get_password_hash
from src.database.models import User, UserRole


def test_login_success(client, session):
    user = User(
        username="testuser",
        email="test@example.com",
        password=get_password_hash(
            "password123"
        ),  # hash this if your auth expects hashing
        role=UserRole.patient,
        is_active=True,
    )
    session.add(user)
    session.commit()

    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "password123",
            "grant_type": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, session):
    user = User(
        username="wrongpass",
        email="wrong@example.com",
        password=get_password_hash("correctpassword"),
        role=UserRole.patient,
    )
    session.add(user)
    session.commit()

    response = client.post(
        "/token",
        data={
            "username": "wrongpass",
            "grant_type": "password",
            "password": "incorrectpassword",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_current_user(client, session):
    user = User(
        username="meuser",
        email="me@example.com",
        password=get_password_hash("secret123"),
        role=UserRole.patient,
    )
    session.add(user)
    session.commit()

    token_response = client.post(
        "/token",
        data={
            "username": "meuser",
            "grant_type": "password",
            "password": "secret123",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    access_token = token_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "meuser"
    assert data["email"] == "me@example.com"
    assert data["role"] == UserRole.patient
    assert data["is_active"] is True


def test_get_current_user_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == 401
