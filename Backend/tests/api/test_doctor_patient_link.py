def test_create_doctor_patient_link(client):
    payload = {
        "doctor_id": 1,
        "patient_id": 1,
        "is_primary": True,
    }

    response = client.post("/doctor-patient-links/", json=payload)

    assert response.status_code == 200
    assert response.json()["doctor_id"] == 1


def test_get_doctor_patient_link(client):
    create = client.post(
        "/doctor-patient-links/",
        json={"doctor_id": 2, "patient_id": 2},
    )

    link_id = create.json()["id"]

    response = client.get(f"/doctor-patient-links/{link_id}")

    assert response.status_code == 200
    assert response.json()["id"] == link_id


def test_get_all_doctor_patient_links(client):
    response = client.get("/doctor-patient-links/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_doctor_patient_link(client):
    create = client.post(
        "/doctor-patient-links/",
        json={"doctor_id": 3, "patient_id": 3},
    )

    link_id = create.json()["id"]

    response = client.put(
        f"/doctor-patient-links/{link_id}",
        json={"is_primary": True},
    )

    assert response.status_code == 200
    assert response.json()["is_primary"] is True


def test_delete_doctor_patient_link(client):
    create = client.post(
        "/doctor-patient-links/",
        json={"doctor_id": 4, "patient_id": 4},
    )

    link_id = create.json()["id"]

    response = client.delete(f"/doctor-patient-links/{link_id}")

    assert response.status_code == 200
    assert response.json()["id"] == link_id
