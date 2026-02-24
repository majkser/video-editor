from pydantic import BaseModel, Field, model_validator


class Cut(BaseModel):
    start: float = Field()
    end: float = Field()

    @model_validator(mode="after")
    def check_start_less_than_end(self) -> "Cut":
        if self.start >= self.end:
            raise ValueError("start time must be less than end time")
        return self


class EditMediaCreateRequest(BaseModel):
    cuts: list[Cut] = Field(
        ...,
        description="List of cuts to apply to the media file. Each cut should have a 'start' and 'end' time in seconds.",
        example=[{"start": 10, "end": 20}, {"start": 30, "end": 40}],
    )


class EditMediaBatchItem(BaseModel):
    media_id: int = Field(..., description="ID of the media file to edit.")
    edits: EditMediaCreateRequest = Field(
        ..., description="Edits to apply to the media file."
    )


class EditMediaBatchRequest(BaseModel):
    edits: list[EditMediaBatchItem] = Field(
        ...,
        min_length=1,
        description="List of media edit operations to perform.",
        example=[
            {
                "media_id": 1,
                "edits": {"cuts": [{"start": 1, "end": 3}]},
            },
            {
                "media_id": 2,
                "edits": {"cuts": [{"start": 3, "end": 6}]},
            },
        ],
    )


class EditMediaBatchResultItem(BaseModel):
    media_id: int
    edited_media_path: str


class EditMediaBatchResponse(BaseModel):
    results: list[EditMediaBatchResultItem] = Field(default_factory=list)
