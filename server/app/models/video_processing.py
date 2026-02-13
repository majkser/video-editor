from ..database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class VideoProcessingModel(Base):
    __tablename__ = "video_processing"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    video_name: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"<VideoProcessingModel(id={self.id}, video_name='{self.video_name}', user_id={self.user_id})>"
