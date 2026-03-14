from fastapi import Header, Depends
from typing import Annotated

from app.error_handler.error_handler import UnauthorizedError
from app.models.user import UserModel
from app.repositories.user import UserModelRepository
from app.providers.user import UserProvider


async def get_current_user(
    api_key: str = Header(..., alias="API-Key"),
    user_repository: UserModelRepository = Depends(UserProvider.get_repository),
) -> UserModel:

    user = user_repository.get_user_by_api_key(api_key)

    if not user:
        raise UnauthorizedError("Invalid API key provided")

    return user


CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]
