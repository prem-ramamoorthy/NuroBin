from src.api.routes.patient_route import patient_router
from src.api.routes.doctor_route import doctor_router
from src.api.routes.caretaker_routes import caretaker_router
from src.gmaps.gmapsRouter import app as gmaps_router
from src.video.route import router as face_router

routers = [patient_router, doctor_router, caretaker_router, gmaps_router, face_router]
