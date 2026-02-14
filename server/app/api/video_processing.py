from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import Response

from app.services.video_processing import VideoProcessingImpl
from app.providers.video_processing import VideoProcessingProvider

router = APIRouter()


@router.post("/upload-video")
async def upload_video(
    file: UploadFile,
    video_processing: VideoProcessingImpl = Depends(
        VideoProcessingProvider.get_service
    ),
):
    return await video_processing.upload_video(file)


@router.get("/download-video/{video_name}")
async def download_video(
    video_name: str,
    video_processing: VideoProcessingImpl = Depends(
        VideoProcessingProvider.get_service
    ),
):

    video_bytes = await video_processing.send_video(video_name)

    return Response(
        content=video_bytes,
        media_type="video/mp4",
        headers={"Content-Disposition": f"attachment; filename={video_name}"},
    )
