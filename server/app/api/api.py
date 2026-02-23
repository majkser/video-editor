from fastapi import APIRouter
from .media_processing import router as media_processing_router
from .user import router as user_router
from .still_video import router as still_video_router
from .project import router as project_router
from .edit_media import router as edit_media_router

api_router = APIRouter()
api_router.include_router(media_processing_router)
api_router.include_router(user_router)
api_router.include_router(still_video_router)
api_router.include_router(project_router)
api_router.include_router(edit_media_router)
