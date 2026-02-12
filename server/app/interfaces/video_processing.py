from abc import ABC, abstractmethod

class VideoProcessing(ABC):
    @abstractmethod
    async def upload_video(self, video_path: str) -> str:
        """Uploads a video file to the server and returns the path where it is stored."""
        raise NotImplementedError("Subclasses must implement upload_video method")
    
    @abstractmethod
    async def send_video(self) -> bytes:
        """Sends the processed video file back to the client."""
        raise NotImplementedError("Subclasses must implement send_video method")