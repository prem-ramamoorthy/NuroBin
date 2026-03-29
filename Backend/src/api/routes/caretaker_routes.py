from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.api.models import RegisterCareTaker
from src.database.create_tables import get_session
from src.database.crud import (
    create_caretaker,
    create_user,
    delete_caretaker,
    get_caretaker,
    get_caretakers,
    update_caretaker,
)
from src.database.models import UserRole
from src.database.schemas import (
    CareTakerCreate,
    CareTakerRead,
    CareTakerUpdate,
    UserCreate,
)

caretaker_router = APIRouter(prefix="/caretaker", tags=["caretakers"])


@caretaker_router.post("/", response_model=CareTakerRead)
async def add_caretaker(
    caretaker: RegisterCareTaker, session: Session = Depends(get_session)
):
    user_in = UserCreate.model_validate_json(
        caretaker.model_dump_json(), extra="ignore"
    )
    caretaker_in = CareTakerCreate.model_validate_json(
        caretaker.model_dump_json(), extra="ignore"
    )
    user_in.sqlmodel_update({"role": UserRole.caretaker})
    user = create_user(session, user_in)
    caretaker_in.sqlmodel_update({"user_id": user.id})
    return create_caretaker(session, caretaker_in)


@caretaker_router.get("/{caretaker_id}", response_model=CareTakerRead)
async def read_caretaker(caretaker_id: int, session: Session = Depends(get_session)):
    return get_caretaker(session, caretaker_id)


@caretaker_router.get("/", response_model=list[CareTakerRead])
async def read_all_caretakers(session: Session = Depends(get_session)):
    return get_caretakers(session)


@caretaker_router.patch("/{caretaker_id}", response_model=CareTakerRead)
async def patch_caretaker(
    caretaker_id: int,
    caretaker: CareTakerUpdate,
    session: Session = Depends(get_session),
):
    return update_caretaker(session, caretaker_id, caretaker)


@caretaker_router.delete("/{caretaker_id}", response_model=CareTakerRead)
async def remove_caretaker(caretaker_id: int, session: Session = Depends(get_session)):
    return delete_caretaker(session, caretaker_id)
