from abc import ABC, abstractmethod

from fastapi import UploadFile


class MediaProcessing(ABC):
    @abstractmethod
    async def upload_media(
        self, file: UploadFile, project_id: int, user_id: int
    ) -> dict:
        """Uploads a media file to the server, links it to the given project owned by user_id."""
        raise NotImplementedError("Subclasses must implement upload_media method")

    @abstractmethod
    async def send_media(self, media_id: int) -> bytes:
        """Sends the processed media file back to the client."""
        raise NotImplementedError("Subclasses must implement send_media method")
