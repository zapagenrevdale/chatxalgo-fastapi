from fastapi import APIRouter, Depends
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db, get_settings

from src.auth.exceptions import unauthorize_exception
from src.auth.services import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from src.auth.schema import Token
from src.users.schema import User
from src.config import Settings


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise unauthorize_exception

    acces_token = create_access_token(
        {"sub": user.username}, settings, timedelta(minutes=15)
    )

    return Token(access_token=acces_token, token_type="bearer")


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
