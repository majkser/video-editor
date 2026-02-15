from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db_session
from ..repositories.user import UserModelRepository
from ..services.user import UserImpl
from ..interfaces.provider import BaseProvider


class UserProvider(BaseProvider):
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
