from ..models.video_processing import VideoProcessingModel
from sqlalchemy.orm import Session


class VideoProcessingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_video_processing_entry(
        self, video_name: str, user_id: int
    ) -> VideoProcessingModel:
        new_entry = VideoProcessingModel(video_name=video_name, user_id=user_id)
        self.db.add(new_entry)
        self.db.commit()
        self.db.refresh(new_entry)
        return new_entry
