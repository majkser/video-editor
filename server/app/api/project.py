from fastapi import APIRouter, Depends

from ..schemas.project import ProjectCreateRequest
from ..providers.project import ProjectProvider
from ..services.project import ProjectImpl

router = APIRouter(prefix="projects", tags=["projects"])


@router.post("/create_project")
async def create_project(
    request: ProjectCreateRequest,
    project_service: ProjectImpl = Depends(ProjectProvider.get_service),
):
    # TODO: Call project_service.create_project() with request data

    return {"message": "Project created successfully"}
