from abc import ABC, abstractmethod
from app.schemas.still_video import StillVideoResult


from pathlib import Path


class StillVideo(ABC):
    @abstractmethod
    async def combine_still_with_audio(
        self, still_id: int, audio_id: int
    ) -> StillVideoResult:
        """Combines a still image with a audio file and returns the path of the combined media."""
        raise NotImplementedError(
            "Subclasses must implement combine_still_with_audio method"
        )
