from fastapi import APIRouter, Depends
from fastapi import status

from app.interfaces.user import User

from ..schemas.user import UserRegisterRequest, UserRegisterResponse
from ..providers.user import UserProvider

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    request: UserRegisterRequest,
    user_service: User = Depends(UserProvider.get_service),
):
    user = await user_service.register_user(request.username)
    return UserRegisterResponse(
        username=user.username,
        api_key=user.api_key,
    )
