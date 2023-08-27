from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.users.schema import UserCreate, User
from src.users.services import create_user, get_all_users
from src.dependencies import get_db


router = APIRouter()


@router.get("/", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    db_users = get_all_users(db)
    users = [User(**db_user.__dict__) for db_user in db_users]
    return users


@router.post("/", response_model=User)
def store_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(user, db)
    return User(**db_user.__dict__)
