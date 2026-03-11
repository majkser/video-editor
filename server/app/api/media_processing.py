from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import Response
from urllib.parse import quote

from app.dependencies.auth import get_current_user
from app.dependencies.annotated import CurrentUser, Project_id, MediaProcessingService

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/upload")
async def upload_media(
    file: UploadFile,
    project_id: Project_id,
    current_user: CurrentUser,
    media_processing: MediaProcessingService,
):
    return await media_processing.upload_media(file, project_id, current_user.user_id)


@router.get("/download/{media_id}", dependencies=[Depends(get_current_user)])
async def download_media(
    media_id: int,
    media_processing: MediaProcessingService,
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
