from abc import ABC, abstractmethod

from app.schemas.edit_media import (
    EditMediaBatchRequest,
    EditMediaBatchResponse,
    EditMediaCreateRequest,
)


class EditMedia(ABC):
    @abstractmethod
    async def edit_media(self, media_id: int, edits: EditMediaCreateRequest) -> dict:
        """Applies the specified edits to the media file and returns the path to the edited file."""
        raise NotImplementedError("Subclasses must implement edit_media method")

    @abstractmethod
    async def edit_media_batch(
        self, request: EditMediaBatchRequest
    ) -> EditMediaBatchResponse:
        """Applies edits to multiple media files and returns results and errors."""
        raise NotImplementedError("Subclasses must implement edit_media_batch method")
