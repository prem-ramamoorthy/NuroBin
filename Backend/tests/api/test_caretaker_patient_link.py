def test_create_caretaker_patient_link(client):
    payload = {
        "caretaker_id": 1,
        "patient_id": 1,
        "shift": "day",
        "is_primary": True,
    }

    response = client.post("/caretaker-patient-links/", json=payload)

    assert response.status_code == 200
    assert response.json()["caretaker_id"] == 1
    assert response.json()["shift"] == "day"


def test_get_caretaker_patient_link(client):
    create = client.post(
        "/caretaker-patient-links/",
        json={"caretaker_id": 2, "patient_id": 2},
    )

    link_id = create.json()["id"]

    response = client.get(f"/caretaker-patient-links/{link_id}")

    assert response.status_code == 200
    assert response.json()["id"] == link_id


def test_get_all_caretaker_patient_links(client):
    response = client.get("/caretaker-patient-links/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_caretaker_patient_link(client):
    create = client.post(
        "/caretaker-patient-links/",
        json={"caretaker_id": 3, "patient_id": 3},
    )

    link_id = create.json()["id"]

    response = client.put(
        f"/caretaker-patient-links/{link_id}",
        json={"shift": "night"},
    )

    assert response.status_code == 200
    assert response.json()["shift"] == "night"


def test_delete_caretaker_patient_link(client):
    create = client.post(
        "/caretaker-patient-links/",
        json={"caretaker_id": 4, "patient_id": 4},
    )

    link_id = create.json()["id"]

    response = client.delete(f"/caretaker-patient-links/{link_id}")

    assert response.status_code == 200
    assert response.json()["id"] == link_id
