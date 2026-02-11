from fastapi import WebSocket, APIRouter
from .schemas import LocationUpdate, PlaceCreate
from .controllers import update_location as update_location_controller, get_latest as get_latest_controller, ws_track as ws_track_controller, route_to_place as route_to_place_controller, get_place as get_place_controller, add_place as add_place_controller, list_places as list_places_controller

app = APIRouter()

@app.post("/location/update")
async def update_location_route(user_id: str, payload: LocationUpdate):
    return await update_location_controller(user_id, payload)

@app.get("/location/latest/{user_id}")
def get_latest_route(user_id: str):
    return get_latest_controller(user_id)

@app.websocket("/ws/track/{user_id}")
async def ws_track_route(user_id: str, websocket: WebSocket):
    await ws_track_controller(user_id, websocket)

@app.post("/places")
def add_place_route(user_id: str, place: PlaceCreate):
    return add_place_controller(user_id, place)

@app.get("/places")
def list_places_route(user_id: str):
    return list_places_controller(user_id)

@app.get("/places/{place_id}")
def get_place_route(user_id: str, place_id: str):
    return get_place_controller(user_id, place_id)

@app.get("/route/to-place/{place_id}")
async def route_to_place_route(user_id: str, place_id: str, mode: str = "driving"):
    return await route_to_place_controller(user_id, place_id, mode)