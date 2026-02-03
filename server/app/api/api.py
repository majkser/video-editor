from fastapi import APIRouter
from .upload_video.upload_video import router as fetch_video_router

api_router = APIRouter()

api_router.include_router(fetch_video_router)