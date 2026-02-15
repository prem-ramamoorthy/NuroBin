from pydantic import BaseModel, Field
from typing import Optional

class LocationUpdate(BaseModel):
    lat: float
    lng: float
    accuracy: Optional[float] = None
    speed: Optional[float] = None
    heading: Optional[float] = None
    timestamp: Optional[float] = None

class PlaceCreate(BaseModel):
    label: str = Field(..., examples=["home", "office", "gym"])
    name: Optional[str] = None
    lat: float
    lng: float
    address: Optional[str] = None
    geofence_radius_m: Optional[int] = 150 # default geofence radius for notifications in meters