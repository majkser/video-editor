from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db_session
from app.repositories.project import ProjectModelRepository
from app.services.project import ProjectImpl
from app.interfaces.project import Project


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


ProjectServiceDep = Annotated[Project, Depends(ProjectProvider.get_service)]
