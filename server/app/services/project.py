from ..interfaces.project import Project, ProjectModel
from ..repositories.project import ProjectRepository


class ProjectImpl(Project):
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    # TODO: implement methods like create_project
