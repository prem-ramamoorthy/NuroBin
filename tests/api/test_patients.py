def test_create_patient(client):
    response = client.post(
        "/patients/",
        json={
            "name": "John Doe",
            "age": 30,
            "address": "123 Main St",
            "medical_history": "None",
            "phone": "1234567890",
            "email": "john@example.com",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert "id" in data


def test_get_patient(client):
    # create first
    create = client.post(
        "/patients/",
        json={
            "name": "Jane Doe",
            "age": 40,
            "address": "456 Elm St",
            "medical_history": None,
            "phone": "0987654321",
            "email": None,
        },
    )
    patient_id = create.json()["id"]

    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200
    assert response.json()["id"] == patient_id


def test_get_all_patients(client):
    response = client.get("/patients/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_patient(client):
    create = client.post(
        "/patients/",
        json={
            "name": "Mark",
            "age": 25,
            "address": "789 Oak St",
            "medical_history": None,
            "phone": "1112223333",
            "email": None,
        },
    )
    patient_id = create.json()["id"]

    response = client.patch(
        f"/patients/{patient_id}",
        json={"age": 26},
    )
    print(response)

    assert response.status_code == 200
    assert response.json()["age"] == 26


def test_delete_patient(client):
    create = client.post(
        "/patients/",
        json={
            "name": "Delete Me",
            "age": 50,
            "address": "Nowhere",
            "medical_history": None,
            "phone": "0000000000",
            "email": None,
        },
    )
    patient_id = create.json()["id"]

    response = client.delete(f"/patients/{patient_id}")
    assert response.status_code == 200
