from fastapi import APIRouter
from .video_processing import router as video_processing_router

api_router = APIRouter()
api_router.include_router(video_processing_router)