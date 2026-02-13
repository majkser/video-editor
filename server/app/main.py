from fastapi import FastAPI
from .api.api import api_router
from .database import Base, engine

app = FastAPI()

app.include_router(api_router, prefix="/api")

Base.metadata.create_all(bind=engine)
