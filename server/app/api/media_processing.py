from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import Response

from app.services.media_processing import MediaProcessingImpl
from app.providers.media_processing import MediaProcessingProvider

router = APIRouter(prefix='/media', tags=['media'])


@router.post("/upload")
async def upload_media(
    file: UploadFile,
    media_processing: MediaProcessingImpl = Depends(
        MediaProcessingProvider.get_service
    ),
):
    return await media_processing.upload_media(file)


@router.get("/download/{media_name}")
async def download_media(
    media_name: str,
    media_processing: MediaProcessingImpl = Depends(
        MediaProcessingProvider.get_service
    ),
):

    media_bytes = await media_processing.send_media(media_name)

    return Response(
        content=media_bytes,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={media_name}"},
    )
