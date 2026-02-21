from ..models.user import UserModel
from sqlalchemy.orm import Session
from sqlalchemy import select
import hashlib


class UserModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user_model_entry(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> UserModel | None:
        statement = select(UserModel).where(UserModel.username == username)
        return self.db.scalars(statement).first()

    def get_user_by_api_key(self, api_key: str) -> UserModel | None:

        hashed_api_key = hashlib.sha256(api_key.encode()).hexdigest()
        statement = select(UserModel).where(UserModel.api_key == hashed_api_key)

        return self.db.scalars(statement).first()
