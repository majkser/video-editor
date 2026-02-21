from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.interfaces.still_video import StillVideo
from app.providers.still_video import StillVideoProvider
from app.schemas.still_video import StillVideoRequest

router = APIRouter(prefix="/still", tags=["still to video"])


@router.post("/generate-video")
async def combine_still_with_audio(
    request: StillVideoRequest,
    still_video_service: StillVideo = Depends(StillVideoProvider.get_service),
) -> FileResponse:
    try:
        result = await still_video_service.combine_still_with_audio(
            request.still_id, request.audio_id
        )
        return FileResponse(
            result.video_path,
            media_type="video/mp4",
            filename=result.video_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
