from fastapi import APIRouter, HTTPException, UploadFile, Depends
from fastapi.responses import Response
from urllib.parse import quote

from app.services.media_processing import MediaProcessingImpl
from app.providers.media_processing import MediaProcessingProvider

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/upload")
async def upload_media(
    file: UploadFile,
    media_processing: MediaProcessingImpl = Depends(
        MediaProcessingProvider.get_service
    ),
):
    return await media_processing.upload_media(file)


@router.get("/download/{media_id}")
async def download_media(
    media_id: int,
    media_processing: MediaProcessingImpl = Depends(
        MediaProcessingProvider.get_service
    ),
):

    media_bytes = await media_processing.send_media(media_id)

    # Get media name for encoding filename
    media = media_processing.repository.get_media_model_by_id(media_id)
    if media is None:
        raise HTTPException(
            status_code=404, detail=f"Media with id {media_id} not found"
        )

    # Encode filename for non-ASCII resolves problem of polish chars
    encoded_filename = quote(media.media_orginal_name)

    return Response(
        content=media_bytes,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        },
    )
