from pydantic import BaseModel, Field, model_validator


class Cut(BaseModel):
    start: float = (Field(),)
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
