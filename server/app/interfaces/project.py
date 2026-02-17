from abc import ABC, abstractmethod
from ..models.project import ProjectModel


class Project(ABC):
    @abstractmethod
    async def create_project(self, api_key: str, project_name: str) -> ProjectModel:
        """ "Creates a new project with given api_key and project name"""
        raise NotImplementedError
