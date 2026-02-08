def test_create_caretaker(client):
    payload = {
        "name": "Caretaker One",
        "age": 35,
        "license_number": "CARE123",
        "experience": 10,
        "salary": 50000.0,
        "grade": "A",
        "phone": "7777777777",
    }

    response = client.post("/caretaker/", json=payload)
    assert response.status_code == 200
    assert response.json()["grade"] == "A"


def test_get_caretaker(client):
    create = client.post(
        "/caretaker/",
        json={
            "name": "Caretaker Two",
            "age": None,
            "license_number": "CARE456",
            "experience": 5,
            "salary": 30000.0,
            "grade": "B",
            "phone": "8888888888",
        },
    )

    caretaker_id = create.json()["id"]

    response = client.get(f"/caretaker/{caretaker_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Caretaker Two"


def test_get_all_caretakers(client):
    response = client.get("/caretaker/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_patch_caretaker(client):
    create = client.post(
        "/caretaker/",
        json={
            "name": "Caretaker Patch",
            "age": 40,
            "license_number": "CARE789",
            "experience": 15,
            "salary": 60000.0,
            "grade": "A",
            "phone": "9999999998",
        },
    )

    caretaker_id = create.json()["id"]

    response = client.patch(
        f"/caretaker/{caretaker_id}",
        json={"salary": 65000.0},
    )

    assert response.status_code == 200
    assert response.json()["salary"] == 65000.0


def test_delete_caretaker(client):
    create = client.post(
        "/caretaker/",
        json={
            "name": "Caretaker Delete",
            "age": 50,
            "license_number": "CAREDEL",
            "experience": 20,
            "salary": 70000.0,
            "grade": "C",
            "phone": "1010101010",
        },
    )

    caretaker_id = create.json()["id"]

    response = client.delete(f"/caretaker/{caretaker_id}")
    assert response.status_code == 200
    assert response.json()["id"] == caretaker_id
