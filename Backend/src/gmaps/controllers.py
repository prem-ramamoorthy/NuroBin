import time
from .websocket import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, List
from .utils import get_directions

latest_location: Dict[str, dict] = {}
places_store: Dict[str, List[dict]] = {}

manager = ConnectionManager()

async def update_location(user_id, payload):
    ts = payload.timestamp or time.time()
    data = payload.model_dump()
    data["timestamp"] = ts

    latest_location[user_id] = data
    await manager.broadcast(user_id, {"type": "location", "user_id": user_id, "data": data})
    return {"status": "ok", "user_id": user_id, "data": data}

def get_latest(user_id):
    loc = latest_location.get(user_id)
    if not loc:
        raise HTTPException(404, "No location found")
    return {"user_id": user_id, "data": loc}

async def ws_track(user_id, websocket):
    await manager.connect(user_id, websocket)
    try:
        if user_id in latest_location:
            await websocket.send_json({"type": "location", "user_id": user_id, "data": latest_location[user_id]})

        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)

async def route_to_place(user_id, place_id, mode="driving"):
    loc = latest_location.get(user_id)
    if not loc:
        raise HTTPException(404, "No latest location for this user")

    place = None
    for p in places_store.get(user_id, []):
        if p["id"] == place_id:
            place = p
            break
    if not place:
        raise HTTPException(404, "Place not found")

    directions = await get_directions(loc["lat"], loc["lng"], place["lat"], place["lng"], mode=mode)

    try:
        leg = directions["routes"][0]["legs"][0]
        overview_polyline = directions["routes"][0]["overview_polyline"]["points"]
    except (KeyError, IndexError):
        raise HTTPException(500, "Invalid response from directions API")
    return {
        "origin": {"lat": loc["lat"], "lng": loc["lng"]},
        "destination": {"lat": place["lat"], "lng": place["lng"]},
        "distance": leg["distance"],
        "duration": leg["duration"],
        "polyline": overview_polyline,
        "raw": directions
    }
    
def get_place(user_id, place_id):
    for p in places_store.get(user_id, []):
        if p["id"] == place_id:
            return p
    raise HTTPException(404, "Place not found")

def add_place(user_id, place):
    place_id = f"{int(time.time() * 1000)}"
    record = {"id": place_id, **place.model_dump()}
    places_store.setdefault(user_id, []).append(record)
    return {"status": "ok", "place": record}

def list_places(user_id):
    return {"user_id": user_id, "places": places_store.get(user_id, [])}