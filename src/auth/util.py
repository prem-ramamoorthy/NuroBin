from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pwdlib import PasswordHash
from sqlmodel import Session
from src.api.models import UserApi
from src.auth.jwt_auth import TokenData
from src.config.config_env import Config
from src.database.create_tables import get_session
from src.database.crud import get_user_auth, get_user_username
from src.database.models import User, UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hash = PasswordHash.recommended()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = (
        get_user_username(session, token_data.username) if token_data.username else None
    )
    if user is None:
        raise credentials_exception
    return UserApi.model_validate_json(user.model_dump_json(), extra="ignore")


async def get_current_active_user(
    current_user: Annotated[UserApi, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return password_hash.hash(password=plain_password)


def authenticate_user(session: Session, username: str, password: str) -> str | bool:
    user, user_password = get_user_auth(session, username)
    if not user:
        return False
    if not verify_password(password, user_password):
        return False
    return user


def require_role(required_roles: list[UserRole]):
    def role_dependency(current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user

    return role_dependency
