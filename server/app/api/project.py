from fastapi import APIRouter
from fastapi import status

from app.schemas.project import ProjectCreateRequest, ProjectCreateResponse
from app.providers.project import ProjectServiceDep
from app.dependencies.auth import CurrentUserDep

router = APIRouter(prefix="/project", tags=["project"])


@router.post(
    "/create_project",
    response_model=ProjectCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    request: ProjectCreateRequest,
    current_user: CurrentUserDep,
    project_service: ProjectServiceDep,
):
    project = await project_service.create_project(
        project_name=request.project_name,
        owner_id=current_user.user_id,
    )

    return ProjectCreateResponse(
        project_id=project.project_id,
        project_name=project.project_name,
        created_at=project.created_at,
    )
