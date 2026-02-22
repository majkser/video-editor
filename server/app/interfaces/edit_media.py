from abc import ABC, abstractmethod

from app.schemas.edit_media import EditMediaCreateRequest


class EditMedia(ABC):
    @abstractmethod
    async def edit_media(self, media_id: int, edits: EditMediaCreateRequest) -> dict:
        """Applies the specified edits to the media file and returns the path to the edited file."""
        raise NotImplementedError("Subclasses must implement edit_media method")
