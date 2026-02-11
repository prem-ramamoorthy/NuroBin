import time
from .websocket import ConnectionManager
from fastapi import WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlmodel import Session
from typing import Dict
from .utils import get_directions
from src.database.crud import (
    create_location, get_location, update_location as update_location_db,
    delete_location, create_place, get_place as get_place_db, 
    get_places, update_place, delete_place
)
from src.database.create_tables import get_session

manager = ConnectionManager()

async def update_location(user_id: int, payload, session: Session = Depends(get_session)):
    try:
        ts = payload.timestamp or time.time()
        data = payload.model_dump()
        data["timestamp"] = ts
        data["user_id"] = user_id

        location = update_location_db(session, user_id, data)
        await manager.broadcast(user_id, {"type": "location", "user_id": user_id, "data": data})
        return {"status": "ok", "user_id": user_id, "data": location}
    except Exception as e:
        raise HTTPException(500, f"Failed to update location: {str(e)}")

def get_latest(user_id: int, session: Session = Depends(get_session)):
    try:
        location = get_location(session, user_id)
        if not location:
            raise HTTPException(404, "No location found for this user")
        return {"status": "ok", "user_id": user_id, "data": location}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Failed to retrieve location: {str(e)}")

async def ws_track(user_id: int, websocket: WebSocket, session: Session = Depends(get_session)):
    try:
        await manager.connect(user_id, websocket)
        location = get_location(session, user_id)
        if location:
            await websocket.send_json({"type": "location", "user_id": user_id, "data": location})
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
    except Exception as e:
        manager.disconnect(user_id, websocket)
        await websocket.close(code=1011, reason=f"Server error: {str(e)}")

async def route_to_place(user_id: int, place_id: int, mode: str = "driving", session: Session = Depends(get_session)):
    try:
        location = get_location(session, user_id)
        if not location:
            raise HTTPException(404, "No latest location found for this user")

        place = get_place_db(session, place_id)
        if not place:
            raise HTTPException(404, "Place not found")

        directions = await get_directions(location.lat, location.lng, place.lat, place.lng, mode=mode)
        
        if not directions:
            raise HTTPException(503, "Directions service unavailable")
            
        try:
            leg = directions["routes"][0]["legs"][0]
            overview_polyline = directions["routes"][0]["overview_polyline"]["points"]
        except (KeyError, IndexError, TypeError):
            raise HTTPException(500, "Invalid response from directions API")
        
        return {
            "status": "ok",
            "origin": {"lat": location.lat, "lng": location.lng},
            "destination": {"lat": place.lat, "lng": place.lng},
            "distance": leg["distance"],
            "duration": leg["duration"],
            "polyline": overview_polyline,
            "raw": directions
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Failed to calculate route: {str(e)}")

def add_place(user_id: int, place, session: Session = Depends(get_session)):
    try:
        place_data = place.model_dump()
        place_data["user_id"] = user_id
        record = create_place(session, place_data)
        return {"status": "ok", "user_id": user_id, "place": record}
    except Exception as e:
        raise HTTPException(500, f"Failed to create place: {str(e)}")

def list_places(user_id: int, session: Session = Depends(get_session)):
    try:
        places = get_places(user_id, session)
        return {"status": "ok", "user_id": user_id, "places": places}
    except Exception as e:
        raise HTTPException(500, f"Failed to retrieve places: {str(e)}")

def get_place(user_id: int, place_id: int, session: Session = Depends(get_session)):
    try:
        place = get_place_db(session, place_id)
        if not place:
            raise HTTPException(404, "Place not found")
        return {"status": "ok", "user_id": user_id, "place": place}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Failed to retrieve place: {str(e)}")