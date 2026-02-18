from fastapi import APIRouter, Depends, HTTPException

from app.interfaces.still_video import StillVideo
from app.providers.still_video import StillVideoProvider

router = APIRouter(prefix="/still", tags=["still-video"])


@router.post("/generate-video")
async def combine_still_with_audio(
    still_id: int,
    audio_id: int,
    still_video_service: StillVideo = Depends(StillVideoProvider.get_service),
):
    try:
        result = await still_video_service.combine_still_with_audio(still_id, audio_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))