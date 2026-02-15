from ..interfaces.user import User
from ..repositories.user import UserModelRepository
from ..models.user import UserModel


class UserImpl(User):
    def __init__(self, repository: UserModelRepository):
        self.repository = repository

    async def register_user(self, username: str) -> UserModel:
        existing_user = self.repository.get_user_by_username(username)

        if existing_user:
            raise ValueError(f"Username '{username}' already exists.")

        user = UserModel(username=username)

        return self.repository.create_user_model_entry(user)
