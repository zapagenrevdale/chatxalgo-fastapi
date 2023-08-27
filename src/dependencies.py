from functools import lru_cache
from src.database import SessionLocal
from src.config import Settings


# Dependency
def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
