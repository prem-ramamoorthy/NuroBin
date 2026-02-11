from fastapi import WebSocket, APIRouter, Depends
from sqlmodel import Session
from .schemas import LocationUpdate, PlaceCreate
from .controllers import update_location as update_location_controller, get_latest as get_latest_controller, ws_track as ws_track_controller, route_to_place as route_to_place_controller, get_place as get_place_controller, add_place as add_place_controller, list_places as list_places_controller
from src.database.create_tables import get_session

app = APIRouter()

@app.post("/location/update")
async def update_location_route(
    user_id: int,
    payload: LocationUpdate,
    session: Session = Depends(get_session),
):
    return await update_location_controller(user_id, payload, session)

@app.get("/location/latest/{user_id}")
def get_latest_route(user_id: int, session: Session = Depends(get_session)):
    return get_latest_controller(user_id, session)

@app.websocket("/ws/track/{user_id}")
async def ws_track_route(
    user_id: int,
    websocket: WebSocket,
    session: Session = Depends(get_session),
):
    await ws_track_controller(user_id, websocket, session)

@app.post("/places")
def add_place_route(
    user_id: int,
    place: PlaceCreate,
    session: Session = Depends(get_session),
):
    return add_place_controller(user_id, place, session)

@app.get("/places")
def list_places_route(user_id: int, session: Session = Depends(get_session)):
    return list_places_controller(user_id, session)

@app.get("/places/{place_id}")
def get_place_route(user_id: int, place_id: int, session: Session = Depends(get_session)):
    return get_place_controller(user_id, place_id, session)

@app.get("/route/to-place/{place_id}")
async def route_to_place_route(
    user_id: int,
    place_id: int,
    mode: str = "driving",
    session: Session = Depends(get_session),
):
    return await route_to_place_controller(user_id, place_id, mode, session)
