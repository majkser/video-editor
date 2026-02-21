from pathlib import Path
from fastapi import Depends
from app.database import get_db_session
from app.interfaces.provider import BaseProvider
from app.services.still_video import StillVideoImpl
from ..services.media_processing import MediaProcessingImpl
from ..repositories.media import MediaModelRepository
from sqlalchemy.orm import Session


class StillVideoProvider(BaseProvider):
    SERVER_ROOT = Path(__file__).parent.parent.parent
    UPLOAD_DIR = SERVER_ROOT / "uploaded_media"

    @staticmethod
    def get_repository(
        db: Session = Depends(get_db_session),
    ) -> MediaModelRepository:
        return MediaModelRepository(db)

    @staticmethod
    def get_service(
        repository: MediaModelRepository = Depends(get_repository),
    ) -> StillVideoImpl:
        StillVideoProvider.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        return StillVideoImpl(
            server_root=StillVideoProvider.SERVER_ROOT,
            upload_dir=StillVideoProvider.UPLOAD_DIR,
            repository=repository,
        )
