from fastapi import Header, Depends

from app.error_handler.error_handler import UnauthorizedError
from ..models.user import UserModel
from ..repositories.user import UserModelRepository
from ..providers.user import UserProvider
from fastapi import status


async def get_current_user(
    api_key: str = Header(..., alias="API-Key"),
    user_repository: UserModelRepository = Depends(UserProvider.get_repository),
) -> UserModel:

    user = user_repository.get_user_by_api_key(api_key)

    if not user:
        raise UnauthorizedError("Invalid API key provided")

    return user
