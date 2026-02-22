from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db_session
from ..repositories.project import ProjectModelRepository
from ..services.project import ProjectImpl


class ProjectProvider:
    @staticmethod
    def get_repository(
        db: Session = Depends(get_db_session),
    ) -> ProjectModelRepository:
        return ProjectModelRepository(db)

    @staticmethod
    def get_service(
        repository: ProjectModelRepository = Depends(get_repository),
    ) -> ProjectImpl:
        return ProjectImpl(repository=repository)
