from ..database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class ProjectModel(Base):
    __tablename__ = "projects"

    project_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    project_name: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.user_id"), nullable=False
    )

    def __repr__(self):
        return f"<Project(id={self.project_id}, name='{self.project_name}', owner_id={self.owner_id})>"
