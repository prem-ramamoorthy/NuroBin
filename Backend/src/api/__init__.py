from src.api.routes.patient_route import patient_router
from src.api.routes.doctor_route import doctor_router
from src.api.routes.caretaker_routes import caretaker_router
from src.api.routes.meetings_routes import meeting_router
from src.api.routes.caretaker_patient_link import caretaker_patient_link_router
from src.api.routes.doctor_patient_link_routes import doctor_patient_link_router
from src.gmaps.gmapsRouter import app as gmaps_router
from src.video.route import router as face_router

routers = [
    patient_router,
    doctor_router,
    caretaker_router,
    gmaps_router,
    face_router,
    meeting_router,
    caretaker_patient_link_router,
    doctor_patient_link_router,
]
