from fastapi import FastAPI
from .api.api import api_router
from .database import Base, engine
from .models.user import UserModel
from .models.project import ProjectModel
from .models.video import VideoModel


app = FastAPI()

app.include_router(api_router, prefix="/api")

Base.metadata.create_all(bind=engine)
