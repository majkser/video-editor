from typing import Annotated
from fastapi import Depends, Query

from app.dependencies.auth import get_current_user

from app.models.user import UserModel
from app.interfaces.media_processing import MediaProcessing
from app.providers.media import MediaProvider
from app.interfaces.still_video import StillVideo
from app.interfaces.edit_media import EditMedia
from app.providers.user import UserProvider
from app.interfaces.user import User
from app.interfaces.project import Project
from app.providers.project import ProjectProvider

CurrentUser = Annotated[UserModel, Depends(get_current_user)]

Project_id = Annotated[
    int, Query(..., description="ID of the project to link the media to")
]

MediaProcessingService = Annotated[
    MediaProcessing, Depends(MediaProvider.get_media_processing_service)
]

EditMediaService = Annotated[EditMedia, Depends(MediaProvider.get_edit_media_service)]

StillVideoService = Annotated[
    StillVideo, Depends(MediaProvider.get_still_video_service)
]

UserService = Annotated[User, Depends(UserProvider.get_service)]

ProjectService = Annotated[Project, Depends(ProjectProvider.get_service)]
