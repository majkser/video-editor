from ..models.media import MediaModel
from sqlalchemy.orm import Session
from sqlalchemy import select


class MediaModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_media_model_entry(
        self,
        model: MediaModel,
    ) -> MediaModel:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_media_model_by_id(self, media_model_id: int) -> MediaModel:
        statement = select(MediaModel).where(MediaModel.media_id == media_model_id)
        return self.db.scalars(statement).first()
