from sqlalchemy.orm import Session
from ..models.project import ProjectModel
from sqlalchemy import select


class ProjectModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_project_model_entry(self, project: ProjectModel) -> ProjectModel:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_project_by_name_and_owner(
        self, project_name: str, owner_id: int
    ) -> ProjectModel | None:
        statement = select(ProjectModel).where(
            ProjectModel.project_name == project_name, ProjectModel.owner_id == owner_id
        )
        return self.db.scalars(statement).first()

    def get_project_by_id_and_owner(
        self, project_id: int, owner_id: int
    ) -> ProjectModel | None:
        statement = select(ProjectModel).where(
            ProjectModel.project_id == project_id, ProjectModel.owner_id == owner_id
        )
        return self.db.scalars(statement).first()
