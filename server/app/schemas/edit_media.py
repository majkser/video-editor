from pydantic import BaseModel, Field, model_validator


class Cut(BaseModel):
    start: float = Field()
    end: float = Field()

    @model_validator(mode="after")
    def check_start_less_than_end(self) -> "Cut":
        if self.start >= self.end:
            raise ValueError("start time must be less than end time")
        return self


class EditMediaModel(BaseModel):
    cuts: list[Cut] = Field(
        ...,
        description="List of cuts to apply to the media file. Each cut should have a 'start' and 'end' time in seconds.",
        example=[{"start": 10, "end": 20}, {"start": 30, "end": 40}],
    )


class EditMediaBatchItem(BaseModel):
    media_id: int = Field(..., description="ID of the media file to edit.")
    edits: EditMediaModel = Field(..., description="Edits to apply to the media file.")


class EditMediaBatchRequest(BaseModel):
    edits: list[EditMediaBatchItem] = Field(
        ...,
        min_length=1,
        description="List of media edit operations to perform.",
    )
    project_id: int = Field(
        ..., description="ID of the project containing the media files to edit."
    )
    output_format: str = Field(
        default="mp4",
        description="Output file format (e.g., 'mp4', 'mp3', 'avi', 'mov')",
        example="mp4",
    )
    target_width: int | None = Field(
        default=None,
        description="Target width for video output. If not specified, uses the first video's width.",
        example=1920,
    )
    target_height: int | None = Field(
        default=None,
        description="Target height for video output. If not specified, uses the first video's height.",
        example=1080,
    )
    target_fps: float | None = Field(
        default=None,
        description="Target frames per second for video output. If not specified, uses the first video's fps.",
        example=30,
    )
    target_sample_rate: int | None = Field(
        default=None,
        description="Target audio sample rate in Hz (e.g., 44100, 48000). If not specified, uses the first media's sample rate.",
        example=48000,
    )

    class Config:
        json_schema_extra = {
            "example": {
                "edits": [
                    {
                        "media_id": 1,
                        "edits": {"cuts": [{"start": 1, "end": 3}]},
                    },
                    {
                        "media_id": 2,
                        "edits": {"cuts": [{"start": 3, "end": 6}]},
                    },
                ],
                "project_id": 1,
                "output_format": "mp4",
                "target_width": 1920,
                "target_height": 1080,
                "target_fps": 30,
                "target_sample_rate": 48000,
            }
        }


class EditMediaBatchResponse(BaseModel):
    status: str
