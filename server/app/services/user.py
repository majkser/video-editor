from app.error_handler.error_handler import AlreadyExistsError

from ..interfaces.user import User
from ..repositories.user import UserModelRepository
from ..models.user import UserModel
import secrets


class UserImpl(User):
    def __init__(self, repository: UserModelRepository):
        self.repository = repository

    async def register_user(self, username: str) -> UserModel:
        existing_user = self.repository.get_user_by_username(username)

        if existing_user:
            raise AlreadyExistsError(f"User with username '{username}' already exists")

        api_key = f"{username}_{secrets.token_urlsafe(16)}"

        user = UserModel(username=username, api_key=api_key)

        return self.repository.create_user_model_entry(user)
