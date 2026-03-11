from fastapi import APIRouter
from fastapi import status

from app.schemas.user import UserRegisterRequest, UserRegisterResponse
from app.dependencies.annotated import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    request: UserRegisterRequest,
    user_service: UserService,
):
    user = await user_service.register_user(request.username)
    return UserRegisterResponse(
        username=user.username,
        api_key=user.api_key,
    )
