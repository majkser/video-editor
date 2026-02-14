from ..database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class VideoModel(Base):
    __tablename__ = "videos"

    video_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    video_name: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.project_id"), nullable=False
    )

    def __repr__(self):
        return f"<Video(id={self.video_id}, name='{self.video_name}', project_id={self.project_id})>"
