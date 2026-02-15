from ..models.user import UserModel
from sqlalchemy.orm import Session


class UserModelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user_model_entry(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.username == username).first()
