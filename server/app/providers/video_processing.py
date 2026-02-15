from pathlib import Path
from fastapi import Depends
from app.database import get_db_session
from app.interfaces.provider import BaseProvider
from ..services.video_processing import VideoProcessingImpl
from ..repositories.video import VideoModelRepository
from sqlalchemy.orm import Session


class VideoProcessingProvider(BaseProvider):
    SERVER_ROOT = Path(__file__).parent.parent.parent
    UPLOAD_DIR = SERVER_ROOT / "uploaded_videos"

    @staticmethod
    def get_repository(
        db: Session = Depends(get_db_session),
    ) -> VideoModelRepository:
        return VideoModelRepository(db)

    @staticmethod
    def get_service(
        repository: VideoModelRepository = Depends(get_repository),
    ) -> VideoProcessingImpl:
        VideoProcessingProvider.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        return VideoProcessingImpl(
            server_root=VideoProcessingProvider.SERVER_ROOT,
            upload_dir=VideoProcessingProvider.UPLOAD_DIR,
            repository=repository,
        )
