def test_create_doctor(client):
    payload = {
        "name": "Dr Smith",
        "age": 45,
        "license_number": "LIC123",
        "experience": 20,
        "degree": "MD",
        "phone": "9999999999",
        "email": "drsmith@example.com",
    }

    response = client.post("/doctors/", json=payload)
    assert response.status_code == 200
    assert response.json()["license_number"] == "LIC123"


def test_get_doctor(client):
    create = client.post(
        "/doctors/",
        json={
            "name": "Dr Who",
            "age": None,
            "license_number": "WHO001",
            "experience": 100,
            "degree": "Time Lord",
            "phone": "1231231234",
            "email": "who@example.com",
        },
    )

    doctor_id = create.json()["id"]

    response = client.get(f"/doctors/{doctor_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Dr Who"


def test_get_all_doctors(client):
    response = client.get("/doctors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_patch_doctor(client):
    create = client.post(
        "/doctors/",
        json={
            "name": "Dr Patch",
            "age": 55,
            "license_number": "PATCH123",
            "experience": 25,
            "degree": "MBBS",
            "phone": "5555555555",
            "email": "patch@example.com",
        },
    )

    doctor_id = create.json()["id"]

    response = client.patch(
        f"/doctors/{doctor_id}",
        json={"experience": 30},
    )

    assert response.status_code == 200
    assert response.json()["experience"] == 30


def test_delete_doctor(client):
    create = client.post(
        "/doctors/",
        json={
            "name": "Dr Delete",
            "age": 60,
            "license_number": "DEL123",
            "experience": 35,
            "degree": "MD",
            "phone": "6666666666",
            "email": "delete@example.com",
        },
    )

    doctor_id = create.json()["id"]

    response = client.delete(f"/doctors/{doctor_id}")
    assert response.status_code == 200
    assert response.json()["id"] == doctor_id
