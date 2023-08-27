from typing import Annotated, Optional
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.utilities import verify_password


from src.auth.exceptions import token_credential_exception, inactive_user_exception
from src.auth.schema import TokenData
from src.users.schema import User
from src.users.services import get_user_by_username

from src.config import Settings
from src.dependencies import get_db, get_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(
    data: dict, settings: Settings, expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire_date = datetime.utcnow() + expires_delta
    else:
        expire_date = datetime.utcnow() + timedelta(
            minutes=settings.token_expire_minutes
        )
    to_encode.update({"exp": expire_date})
    encoded_jwt = jwt.encode(
        to_encode, settings.token_secret_key, algorithm=settings.token_algorithm
    )
    return encoded_jwt


def decode_token(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session, settings: Settings
) -> User:
    try:
        payload = jwt.decode(
            token, settings.token_secret_key, algorithms=[settings.token_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise token_credential_exception

    except JWTError:
        raise token_credential_exception

    token_data = TokenData(username=username)
    user = get_user_by_username(token_data.username, db)

    if user is None:
        raise token_credential_exception

    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> User:
    user = decode_token(token, db, settings)
    return user


async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    return current_user


def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    db_user = get_user_by_username(username, db)
    if not db_user:
        return None
    if not verify_password(password, db_user.password):
        return None
    return User(**db_user.__dict__)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.active:
        raise inactive_user_exception

    return current_user
