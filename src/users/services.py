from typing import Optional, List

from sqlalchemy.orm import Session

from src.utilities import get_hash_password

from src.users.schema import UserCreate
from src.users.models import User

from src.users.exceptions import username_conflict_exception, email_conflict_exception


def create_user(user: UserCreate, db: Session) -> User:
    if get_user_by_username(user.username, db):
        raise username_conflict_exception
    if get_user_by_email(user.email, db):
        raise email_conflict_exception
    user.password = get_hash_password(user.password)
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(id: int, db: Session) -> Optional[User]:
    return db.query(User).get(id)


def get_user_by_username(username: str, db: Session) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(email: str, db: Session) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session) -> List[Optional[User]]:
    return db.query(User).all()
