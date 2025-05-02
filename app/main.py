from fastapi import FastAPI
from app.routers import auth
from app.database import engine
from app.models import user


user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
