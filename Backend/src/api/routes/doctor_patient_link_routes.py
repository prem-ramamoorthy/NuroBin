from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.database.crud import (
    create_doctor_patient_link,
    get_doctor_patient_link,
    get_doctor_patient_links,
    update_doctor_patient_link,
    delete_doctor_patient_link,
)
from src.database.schemas import (
    DoctorPatientLinkCreate,
    DoctorPatientLinkRead,
    DoctorPatientLinkUpdate,
)
from src.database.create_tables import get_session

doctor_patient_link_router = APIRouter(
    prefix="/doctor-patient-links", tags=["DoctorPatientLink"]
)


@doctor_patient_link_router.post("/", response_model=DoctorPatientLinkRead)
def create(link_in: DoctorPatientLinkCreate, session: Session = Depends(get_session)):
    return create_doctor_patient_link(session, link_in)


@doctor_patient_link_router.get("/", response_model=list[DoctorPatientLinkRead])
def read_all(session: Session = Depends(get_session)):
    return get_doctor_patient_links(session)


@doctor_patient_link_router.get("/{link_id}", response_model=DoctorPatientLinkRead)
def read_one(link_id: int, session: Session = Depends(get_session)):
    link = get_doctor_patient_link(session, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@doctor_patient_link_router.put("/{link_id}", response_model=DoctorPatientLinkRead)
def update(
    link_id: int,
    link_in: DoctorPatientLinkUpdate,
    session: Session = Depends(get_session),
):
    link = update_doctor_patient_link(session, link_id, link_in)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@doctor_patient_link_router.delete("/{link_id}", response_model=DoctorPatientLinkRead)
def delete(link_id: int, session: Session = Depends(get_session)):
    link = delete_doctor_patient_link(session, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link
