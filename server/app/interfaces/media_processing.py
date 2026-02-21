from abc import ABC, abstractmethod

from fastapi import UploadFile


class MediaProcessing(ABC):
    @abstractmethod
    async def upload_media(self, file: UploadFile) -> dict:
        """Uploads a media file to the server and returns the path where it is stored."""
        raise NotImplementedError("Subclasses must implement upload_media method")

    @abstractmethod
    async def send_media(self, media_id: int) -> bytes:
        """Sends the processed media file back to the client."""
        raise NotImplementedError("Subclasses must implement send_media method")
