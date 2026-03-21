from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import (
    OAuth2PasswordRequestFormStrict,
)
from sqlmodel.orm.session import Session
from fastapi.middleware.cors import CORSMiddleware

from src.api.models import UserApi
from src.auth.jwt_auth import Token, create_access_token
from src.auth.util import authenticate_user, get_current_user, require_role
from src.config.config_env import Config
from src.database.create_tables import create_db_table, get_session
from src.database.models import UserRole
from src.api import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_table()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router=router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the NuroBin Backend API!",
        "endpoints": [
            "/patients/",
            "/doctors/",
            "/caretaker/",
            "/gmaps/",
            "/users/me",
            "/token",
            "/profile",
        ],
        "description": "This API allows you to manage patients, doctors, and caretakers. You can create, read, update, and delete records for each of these entities. Additionally, you can authenticate users and access protected endpoints based on their roles.",
        "health": "OK",
    }


@app.get("/users/me")
async def read_users_me(current_user: Annotated[UserApi, Depends(get_current_user)]):
    return current_user


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    session: Session = Depends(get_session),
):
    username = authenticate_user(session, form_data.username, form_data.password)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=float(Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/profile")
async def profile(
    current_user: Annotated[
        UserApi, Depends(require_role(UserRole.patient, UserRole.doctor))
    ],
):
    return current_user
