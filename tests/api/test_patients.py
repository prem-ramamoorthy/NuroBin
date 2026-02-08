def test_register_patient_success(client):
    payload = {
        "username": "johndoe1",
        "email": "john@example.com",
        "password": "securepassword123",
        "name": "John Doe",
        "age": 35,
        "address": "123 Main St",
        "medical_history": "Diabetes",
        "phone": "1234567890",
    }

    response = client.post("/patients/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["name"] == "John Doe"
    assert data["age"] == 35
    assert data["phone"] == "1234567890"


def test_get_patient(client):
    create = client.post(
        "/patients/",
        json={
            "username": "johndoe2",
            "email": "john@example.com",
            "password": "securepassword123",
            "name": "Jane Doe",
            "age": 40,
            "address": "456 Elm St",
            "medical_history": None,
            "phone": "9876543210",
        },
    )

    patient_id = create.json()["id"]

    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"


def test_get_all_patients(client):
    response = client.get("/patients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_patch_patient(client):
    create = client.post(
        "/patients/",
        json={
            "username": "johndoe3",
            "email": "john@example.com",
            "password": "securepassword123",
            "name": "Patch Me",
            "age": 50,
            "address": "Old Address",
            "medical_history": None,
            "phone": "1111111111",
        },
    )

    patient_id = create.json()["id"]

    response = client.patch(
        f"/patients/{patient_id}",
        json={"address": "New Address"},
    )

    assert response.status_code == 200
    assert response.json()["address"] == "New Address"


def test_delete_patient(client):
    create = client.post(
        "/patients/",
        json={
            "username": "johndoe4",
            "email": "john@example.com",
            "password": "securepassword123",
            "name": "Delete Me",
            "age": 60,
            "address": "Somewhere",
            "medical_history": None,
            "phone": "2222222222",
        },
    )

    patient_id = create.json()["id"]

    response = client.delete(f"/patients/{patient_id}")
    assert response.status_code == 200
    assert response.json()["id"] == patient_id
