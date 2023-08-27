from fastapi import FastAPI

from src.users.router import router as user_router
from src.auth.router import router as auth_router

from src.database import engine
from src.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user_router, prefix="/users", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
