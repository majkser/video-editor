from fastapi import APIRouter, Depends, HTTPException

from ..schemas.user import UserCreateRequest, UserCreateResponse
from ..services.user import UserImpl
from ..providers.user import UserProvider

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserCreateResponse)
async def register_user(
    request: UserCreateRequest,
    user_service: UserImpl = Depends(UserProvider.get_service),
):
    try:
        user = await user_service.register_user(request.username)
        return UserCreateResponse(
            user_id=user.user_id,
            username=user.username,
            api_key=user.api_key,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
