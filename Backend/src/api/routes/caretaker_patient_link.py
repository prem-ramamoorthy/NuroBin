from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.database.crud import (
    create_caretaker_patient_link,
    get_caretaker_patient_link,
    get_caretaker_patient_links,
    update_caretaker_patient_link,
    delete_caretaker_patient_link,
)
from src.database.schemas import (
    CaretakerPatientLinkCreate,
    CaretakerPatientLinkRead,
    CaretakerPatientLinkUpdate,
)
from src.database.create_tables import get_session

caretaker_patient_link_router = APIRouter(
    prefix="/caretaker-patient-links", tags=["CaretakerPatientLink"]
)


@caretaker_patient_link_router.post("/", response_model=CaretakerPatientLinkRead)
def create(
    link_in: CaretakerPatientLinkCreate, session: Session = Depends(get_session)
):
    return create_caretaker_patient_link(session, link_in)


@caretaker_patient_link_router.get("/", response_model=list[CaretakerPatientLinkRead])
def read_all(session: Session = Depends(get_session)):
    return get_caretaker_patient_links(session)


@caretaker_patient_link_router.get(
    "/{link_id}", response_model=CaretakerPatientLinkRead
)
def read_one(link_id: int, session: Session = Depends(get_session)):
    link = get_caretaker_patient_link(session, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@caretaker_patient_link_router.put(
    "/{link_id}", response_model=CaretakerPatientLinkRead
)
def update(
    link_id: int,
    link_in: CaretakerPatientLinkUpdate,
    session: Session = Depends(get_session),
):
    link = update_caretaker_patient_link(session, link_id, link_in)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@caretaker_patient_link_router.delete(
    "/{link_id}", response_model=CaretakerPatientLinkRead
)
def delete(link_id: int, session: Session = Depends(get_session)):
    link = delete_caretaker_patient_link(session, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link
