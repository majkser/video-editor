from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
