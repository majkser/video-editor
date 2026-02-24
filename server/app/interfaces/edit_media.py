from abc import ABC, abstractmethod

from app.schemas.edit_media import EditMediaBatchRequest, EditMediaBatchResponse


class EditMedia(ABC):
    @abstractmethod
    async def edit_media_batch(
        self, request: EditMediaBatchRequest
    ) -> EditMediaBatchResponse:
        """Applies edits to multiple media files and returns results and errors."""
        raise NotImplementedError("Subclasses must implement edit_media_batch method")
