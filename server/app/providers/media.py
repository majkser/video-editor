from pathlib import Path

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.interfaces.edit_media import EditMedia
from app.interfaces.media_processing import MediaProcessing
from app.interfaces.still_video import StillVideo
from app.repositories.media import MediaModelRepository
from app.services.edit_media import EditMediaImpl
from app.services.media_processing import MediaProcessingImpl
from app.services.still_video import StillVideoImpl
from app.providers.project import ProjectProvider
from app.repositories.project import ProjectModelRepository


class MediaProvider:
    SERVER_ROOT = Path(__file__).parent.parent.parent
    UPLOAD_DIR = SERVER_ROOT / "uploaded_media"

    @staticmethod
    def get_repository(
        db: Session = Depends(get_db_session),
    ) -> MediaModelRepository:
        return MediaModelRepository(db)

    @staticmethod
    def get_media_processing_service(
        repository: MediaModelRepository = Depends(get_repository),
        project_repository: ProjectModelRepository = Depends(ProjectProvider.get_repository),
    ) -> MediaProcessing:
        return MediaProcessingImpl(
            server_root=MediaProvider.SERVER_ROOT,
            upload_dir=MediaProvider.UPLOAD_DIR,
            repository=repository,
            project_repository=project_repository,
        )

    @staticmethod
    def get_still_video_service(
        repository: MediaModelRepository = Depends(get_repository),
    ) -> StillVideo:
        return StillVideoImpl(
            server_root=MediaProvider.SERVER_ROOT,
            upload_dir=MediaProvider.UPLOAD_DIR,
            repository=repository,
        )

    @staticmethod
    def get_edit_media_service(
        repository: MediaModelRepository = Depends(get_repository),
    ) -> EditMedia:
        return EditMediaImpl(
            server_root=MediaProvider.SERVER_ROOT,
            upload_dir=MediaProvider.UPLOAD_DIR,
            repository=repository,
        )
