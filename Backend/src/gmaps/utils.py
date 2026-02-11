import httpx
from fastapi import HTTPException
from src.config.config_env import Config

GOOGLE_KEY = Config.GOOGLE_MAPS_API_KEY

async def get_directions(origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float, mode: str = "driving"):
    if not GOOGLE_KEY:
        raise HTTPException(status_code=500, detail="Google API key not configured")

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{origin_lat},{origin_lng}",
        "destination": f"{dest_lat},{dest_lng}",
        "mode": mode,
        "key": GOOGLE_KEY
    }
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        data = r.json()

    if data.get("status") != "OK":
        raise HTTPException(status_code=400, detail=f"Directions failed: {data.get('status')} - {data.get('error_message')}")
    return data
