from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.interfaces.edit_media import EditMedia
from app.providers.media import MediaProvider
from app.schemas.edit_media import EditMediaCreateRequest

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/edit/{media_id}", dependencies=[Depends(get_current_user)])
async def edit_media(
    media_id: int,
    request: EditMediaCreateRequest,
    edit_media_service: EditMedia = Depends(MediaProvider.get_edit_media_service),
):
    return await edit_media_service.edit_media(media_id, request)
