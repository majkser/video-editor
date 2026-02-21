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

    media_bytes, orginal_filename = await media_processing.send_media(media_id)

    # Encode filename for non-ASCII resolves problem of polish chars
    encoded_filename = quote(orginal_filename)

    return Response(
        content=media_bytes,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        },
    )
