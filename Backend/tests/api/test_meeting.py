from datetime import datetime, timezone


def test_create_meeting(client):
    payload = {
        "patient_id": 1,
        "doctor_id": 1,
        "scheduled_time": datetime.now(timezone.utc).isoformat(),
        "duration_minutes": 30,
    }

    response = client.post("/meetings/", json=payload)

    assert response.status_code == 200
    assert response.json()["patient_id"] == 1


def test_get_meeting(client):
    create = client.post(
        "/meetings/",
        json={
            "patient_id": 2,
            "doctor_id": 2,
            "scheduled_time": datetime.now(timezone.utc).isoformat(),
        },
    )

    meeting_id = create.json()["id"]

    response = client.get(f"/meetings/{meeting_id}")

    assert response.status_code == 200
    assert response.json()["id"] == meeting_id


def test_get_all_meetings(client):
    response = client.get("/meetings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_meeting(client):
    create = client.post(
        "/meetings/",
        json={
            "patient_id": 3,
            "doctor_id": 3,
            "scheduled_time": datetime.now(timezone.utc).isoformat(),
        },
    )

    meeting_id = create.json()["id"]

    response = client.put(
        f"/meetings/{meeting_id}",
        json={"notes": "Updated notes"},
    )

    assert response.status_code == 200
    assert response.json()["notes"] == "Updated notes"


def test_delete_meeting(client):
    create = client.post(
        "/meetings/",
        json={
            "patient_id": 4,
            "doctor_id": 4,
            "scheduled_time": datetime.now(timezone.utc).isoformat(),
        },
    )

    meeting_id = create.json()["id"]

    response = client.delete(f"/meetings/{meeting_id}")

    assert response.status_code == 200
    assert response.json()["id"] == meeting_id
