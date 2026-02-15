from abc import ABC, abstractmethod
from ..models.user import UserModel


class User(ABC):
    @abstractmethod
    async def register_user(self, username: str) -> UserModel:
        """Registers a new user with the given username and generate an API key."""
        raise NotImplementedError("Subclasses must implement register_user method")
