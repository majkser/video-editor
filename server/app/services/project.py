from app.error_handler.error_handler import AlreadyExistsError

from ..interfaces.project import Project, ProjectModel
from ..repositories.project import ProjectModelRepository


class ProjectImpl(Project):
    def __init__(
        self,
        repository: ProjectModelRepository,
    ):
        self.repository = repository

    async def create_project(self, project_name: str, owner_id: int) -> ProjectModel:
        existing_project = self.repository.get_project_by_name_and_owner(
            project_name, owner_id
        )

        if existing_project:
            raise AlreadyExistsError(
                f"Project name '{project_name}' already exist. Choose a different name to create new project"
            )

        project = ProjectModel(project_name=project_name, owner_id=owner_id)

        return self.repository.create_project_model_entry(project)
