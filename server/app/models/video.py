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
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[float] = mapped_column(Integer, nullable=False)
    codec: Mapped[str] = mapped_column(String, nullable=False)
    size_in_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"<Video(id={self.video_id}, name='{self.video_name}', project_id={self.project_id})>"
