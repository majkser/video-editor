from ..models.video import VideoModel
from sqlalchemy.orm import Session


class VideoModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_video_model_entry(self, video_name: str, project_id: int) -> VideoModel:
        new_entry = VideoModel(video_name=video_name, project_id=project_id)
        self.db.add(new_entry)
        self.db.commit()
        self.db.refresh(new_entry)
        return new_entry
