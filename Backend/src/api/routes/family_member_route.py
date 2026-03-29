from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.database.create_tables import get_session
from src.database.crud import (
    create_family_member,
    get_family_member,
    get_family_members_by_patient,
    update_family_member,
    delete_family_member,
    get_patient
)
from src.database.schemas import FamilyMemberCreate, FamilyMemberRead, FamilyMemberUpdate
from src.database.models import UserRole
from src.auth.util import get_current_active_user, require_role
from src.api.models import UserApi
from typing import Annotated
from sqlmodel import select
from src.database.models import Patient

router = APIRouter(prefix="/family", tags=["family"])

@router.post("/", response_model=FamilyMemberRead)
def add_family_member(
    fm_in: FamilyMemberCreate,
    current_user: Annotated[UserApi, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    # Only doctors, caretakers, or admins can add family members/memory triggers usually
    # But let's allow the patient to add their own if they want? 
    # The paper says "caregivers remotely input Memory Triggers". 
    # So we restrict to non-patients or the patient themselves.
    return create_family_member(session, fm_in)

@router.get("/patient/{patient_id}", response_model=list[FamilyMemberRead])
def list_family_members(
    patient_id: int,
    session: Session = Depends(get_session)
):
    return get_family_members_by_patient(session, patient_id)

@router.get("/me", response_model=list[FamilyMemberRead])
def list_my_family_members(
    current_user: Annotated[UserApi, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role != UserRole.patient:
        raise HTTPException(status_code=403, detail="Only patients can use /me")
    
    # Find patient record
    patient = session.exec(select(Patient).where(Patient.user_id == current_user.id)).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    
    return get_family_members_by_patient(session, patient.id)

@router.patch("/{fm_id}", response_model=FamilyMemberRead)
def patch_family_member(
    fm_id: int,
    fm_in: FamilyMemberUpdate,
    session: Session = Depends(get_session)
):
    return update_family_member(session, fm_id, fm_in)

@router.delete("/{fm_id}")
def remove_family_member(
    fm_id: int,
    session: Session = Depends(get_session)
):
    if not delete_family_member(session, fm_id):
        raise HTTPException(status_code=404, detail="Family member not found")
    return {"message": "Deleted successfully"}
