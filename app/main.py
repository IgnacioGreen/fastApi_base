from fastapi import FastAPI
from app.routers import auth, users, orders
from app.database import engine
from app.models import user


user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
