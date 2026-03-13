from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db_session
from app.repositories.user import UserModelRepository
from app.services.user import UserImpl
from app.interfaces.user import User


class UserProvider:
    @staticmethod
    def get_repository(
        db: Session = Depends(get_db_session),
    ) -> UserModelRepository:
        return UserModelRepository(db)

    @staticmethod
    def get_service(
        repository: UserModelRepository = Depends(get_repository),
    ) -> UserImpl:
        return UserImpl(repository=repository)


UserServiceDep = Annotated[User, Depends(UserProvider.get_service)]
