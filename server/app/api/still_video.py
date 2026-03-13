from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.dependencies.auth import get_current_user
from app.schemas.still_video import StillVideoRequest
from app.providers.media import StillVideoServiceDep

router = APIRouter(prefix="/still", tags=["still to video"])


@router.post("/generate-video", dependencies=[Depends(get_current_user)])
async def combine_still_with_audio(
    request: StillVideoRequest,
    still_video_service: StillVideoServiceDep,
) -> FileResponse:
    result = await still_video_service.combine_still_with_audio(
        request.still_id, request.audio_id
    )
    return FileResponse(
        result.video_path,
        media_type="video/mp4",
        filename=result.video_name,
    )
