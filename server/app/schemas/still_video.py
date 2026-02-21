from pydantic import BaseModel, Field


class StillVideoRequest(BaseModel):
    still_id: int = Field(..., gt=0)
    audio_id: int = Field(..., gt=0)


class StillVideoResult(BaseModel):
    video_path: str
    video_name: str
