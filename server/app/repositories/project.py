from sqlalchemy.orm import Session
from ..models.project import ProjectModel


class ProjectModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_project_model_entry(self, project: ProjectModel) -> ProjectModel:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
