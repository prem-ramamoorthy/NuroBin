import pytest
from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient

from src.gmaps import gmapsRouter
from src.gmaps.schemas import LocationUpdate, PlaceCreate


@pytest.fixture
def gmaps_client():
    app = FastAPI()
    session_sentinel = object()

    def override_get_session():
        yield session_sentinel

    app.dependency_overrides[gmapsRouter.get_session] = override_get_session
    app.include_router(gmapsRouter.app, prefix="/gmaps")

    with TestClient(app) as client:
        yield client, session_sentinel


def test_update_location_route_delegates_to_controller(monkeypatch, gmaps_client):
    client, session_sentinel = gmaps_client

    expected = {"status": "ok", "user_id": 7, "data": {"lat": 12.3, "lng": 45.6}}

    async def fake_controller(user_id: int, payload: LocationUpdate, session):
        assert user_id == 7
        assert isinstance(payload, LocationUpdate)
        assert payload.lat == 12.3
        assert payload.lng == 45.6
        assert session is session_sentinel
        return expected

    monkeypatch.setattr(gmapsRouter, "update_location_controller", fake_controller)

    response = client.post(
        "/gmaps/location/update?user_id=7",
        json={"lat": 12.3, "lng": 45.6},
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_update_location_route_validates_payload(gmaps_client):
    client, _ = gmaps_client

    response = client.post(
        "/gmaps/location/update?user_id=7",
        json={"lng": 45.6},
    )

    assert response.status_code == 422


def test_get_latest_route_delegates_to_controller(monkeypatch, gmaps_client):
    client, session_sentinel = gmaps_client

    expected = {"status": "ok", "user_id": 9, "data": {"lat": 1.0, "lng": 2.0}}

    def fake_controller(user_id: int, session):
        assert user_id == 9
        assert session is session_sentinel
        return expected

    monkeypatch.setattr(gmapsRouter, "get_latest_controller", fake_controller)

    response = client.get("/gmaps/location/latest/9")

    assert response.status_code == 200
    assert response.json() == expected


def test_add_place_route_delegates_to_controller(monkeypatch, gmaps_client):
    client, session_sentinel = gmaps_client

    expected = {"status": "ok", "user_id": 5, "place": {"id": 1, "label": "home"}}

    def fake_controller(user_id: int, place: PlaceCreate, session):
        assert user_id == 5
        assert isinstance(place, PlaceCreate)
        assert place.label == "home"
        assert place.lat == 19.1
        assert place.lng == 72.8
        assert session is session_sentinel
        return expected

    monkeypatch.setattr(gmapsRouter, "add_place_controller", fake_controller)

    response = client.post(
        "/gmaps/places?user_id=5",
        json={"label": "home", "lat": 19.1, "lng": 72.8},
    )

    assert response.status_code == 200
    assert response.json() == expected


def test_list_places_route_delegates_to_controller(monkeypatch, gmaps_client):
    client, session_sentinel = gmaps_client

    expected = {"status": "ok", "user_id": 3, "places": []}

    def fake_controller(user_id: int, session):
        assert user_id == 3
        assert session is session_sentinel
        return expected

    monkeypatch.setattr(gmapsRouter, "list_places_controller", fake_controller)

    response = client.get("/gmaps/places?user_id=3")

    assert response.status_code == 200
    assert response.json() == expected


def test_get_place_route_delegates_to_controller(monkeypatch, gmaps_client):
    client, session_sentinel = gmaps_client

    expected = {"status": "ok", "user_id": 3, "place": {"id": 8, "label": "office"}}

    def fake_controller(user_id: int, place_id: int, session):
        assert user_id == 3
        assert place_id == 8
        assert session is session_sentinel
        return expected

    monkeypatch.setattr(gmapsRouter, "get_place_controller", fake_controller)

    response = client.get("/gmaps/places/8?user_id=3")

    assert response.status_code == 200
    assert response.json() == expected


def test_route_to_place_route_delegates_to_controller(monkeypatch, gmaps_client):
    client, session_sentinel = gmaps_client

    expected = {
        "status": "ok",
        "origin": {"lat": 12.9, "lng": 77.6},
        "destination": {"lat": 13.0, "lng": 77.7},
    }

    async def fake_controller(user_id: int, place_id: int, mode: str, session):
        assert user_id == 6
        assert place_id == 12
        assert mode == "walking"
        assert session is session_sentinel
        return expected

    monkeypatch.setattr(gmapsRouter, "route_to_place_controller", fake_controller)

    response = client.get("/gmaps/route/to-place/12?user_id=6&mode=walking")

    assert response.status_code == 200
    assert response.json() == expected


def test_ws_track_route_delegates_to_controller(monkeypatch, gmaps_client):
    client, session_sentinel = gmaps_client
    seen = {"called": False}

    async def fake_controller(user_id: int, websocket: WebSocket, session):
        seen["called"] = True
        assert user_id == 22
        assert session is session_sentinel
        await websocket.accept()
        await websocket.send_json({"status": "connected", "user_id": user_id})
        await websocket.close()

    monkeypatch.setattr(gmapsRouter, "ws_track_controller", fake_controller)

    with client.websocket_connect("/gmaps/ws/track/22") as websocket:
        payload = websocket.receive_json()

    assert seen["called"] is True
    assert payload == {"status": "connected", "user_id": 22}
