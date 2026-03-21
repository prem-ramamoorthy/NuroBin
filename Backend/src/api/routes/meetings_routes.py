from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.database.crud import (
    create_meeting,
    get_meeting,
    get_meetings,
    update_meeting,
    delete_meeting,
)
from src.database.schemas import (
    MeetingCreate,
    MeetingRead,
    MeetingUpdate,
)
from src.database.create_tables import get_session

meeting_router = APIRouter(prefix="/meetings", tags=["Meetings"])


@meeting_router.post("/", response_model=MeetingRead)
def create(meeting_in: MeetingCreate, session: Session = Depends(get_session)):
    return create_meeting(session, meeting_in)


@meeting_router.get("/", response_model=list[MeetingRead])
def read_all(session: Session = Depends(get_session)):
    return get_meetings(session)


@meeting_router.get("/{meeting_id}", response_model=MeetingRead)
def read_one(meeting_id: int, session: Session = Depends(get_session)):
    meeting = get_meeting(session, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@meeting_router.put("/{meeting_id}", response_model=MeetingRead)
def update(
    meeting_id: int,
    meeting_in: MeetingUpdate,
    session: Session = Depends(get_session),
):
    meeting = update_meeting(session, meeting_id, meeting_in)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@meeting_router.delete("/{meeting_id}", response_model=MeetingRead)
def delete(meeting_id: int, session: Session = Depends(get_session)):
    meeting = delete_meeting(session, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting
