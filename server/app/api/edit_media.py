from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.interfaces.edit_media import EditMedia
from app.providers.media import MediaProvider
from app.schemas.edit_media import EditMediaBatchRequest, EditMediaBatchResponse

router = APIRouter(prefix="/media", tags=["media"])


@router.post(
    "/edit",
    dependencies=[Depends(get_current_user)],
    response_model=EditMediaBatchResponse,
)
async def edit_media(
    request: EditMediaBatchRequest,
    edit_media_service: EditMedia = Depends(MediaProvider.get_edit_media_service),
):
    return await edit_media_service.edit_media_batch(request)
