from ..database import Base
from sqlalchemy import Integer, String, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from enum import Enum


class MediaType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"


class MediaModel(Base):
    __tablename__ = "media"

    media_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    media_name: Mapped[str] = mapped_column(String, nullable=False)
    media_original_name: Mapped[str] = mapped_column(String, nullable=False)
    media_type: Mapped[MediaType] = mapped_column(SQLEnum(MediaType), nullable=False)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.project_id"), nullable=False
    )
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    duration: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    codec: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fps: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    size_in_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"<Media(id={self.media_id}, name='{self.media_original_name}', project_id={self.project_id})>"
