from pydantic import BaseModel, Field


class ProjectCreateRequest(BaseModel):
    api_key: str
    project_name: str = Field(..., min_length=1, max_length=50)
