from zipfile import Path

from app.error_handler.error_handler import FfmpegError, NotFoundError
from app.interfaces.edit_media import EditMedia
import ffmpeg

from app.models.media import MediaType
from app.repositories.media import MediaModelRepository
from app.schemas.edit_media import (
    EditMediaBatchRequest,
    EditMediaBatchResponse,
    EditMediaBatchErrorItem,
    EditMediaBatchResultItem,
    EditMediaCreateRequest,
)


class EditMediaImpl(EditMedia):
    def __init__(
        self, server_root: Path, upload_dir: Path, repository: MediaModelRepository
    ):
        self.SERVER_ROOT = server_root
        self.UPLOAD_DIR = upload_dir
        self.repository = repository

    async def edit_media(self, media_id: int, edits: EditMediaCreateRequest) -> dict:
        media_file = self.repository.get_media_model_by_id(media_id)
        if not media_file:
            raise NotFoundError(f"Media file with ID {media_id} not found")
        input_path = self.UPLOAD_DIR / media_file.media_name
        output_path = self.UPLOAD_DIR / f"edited_{media_file.media_name}"

        try:
            stream = ffmpeg.input(str(input_path))
            if edits.cuts:
                cut_streams = []

                for cut in edits.cuts:
                    start, end = cut.start, cut.end

                    if media_file.media_type == MediaType.VIDEO:
                        v_cut = stream.video.trim(start=start, end=end).setpts(
                            "PTS-STARTPTS"
                        )
                        a_cut = stream.audio.filter_(
                            "atrim", start=start, end=end
                        ).filter_("asetpts", "PTS-STARTPTS")
                        cut_streams.append(v_cut)
                        cut_streams.append(a_cut)
                    elif media_file.media_type == MediaType.AUDIO:
                        a_cut = stream.filter_("atrim", start=start, end=end).filter_(
                            "asetpts", "PTS-STARTPTS"
                        )
                        cut_streams.append(a_cut)

                v = 1 if media_file.media_type == MediaType.VIDEO else 0

                stream = ffmpeg.concat(*cut_streams, v=v, a=1)

            ffmpeg.output(stream, str(output_path)).overwrite_output().run(quiet=True)

        except ffmpeg.Error as e:
            raise FfmpegError(f"Error editing media: {e.stderr.decode()}")

        return {"edited_media_path": str(output_path)}

    async def edit_media_batch(
        self, request: EditMediaBatchRequest
    ) -> EditMediaBatchResponse:
        results: list[EditMediaBatchResultItem] = []
        errors: list[EditMediaBatchErrorItem] = []

        for item in request.edits:
            try:
                result = await self.edit_media(item.media_id, item.edits)
                results.append(
                    EditMediaBatchResultItem(
                        media_id=item.media_id,
                        status="success",
                        edited_media_path=result["edited_media_path"],
                    )
                )
            except (NotFoundError, FfmpegError) as e:
                errors.append(
                    EditMediaBatchErrorItem(
                        media_id=item.media_id,
                        status="error",
                        detail=e.message,
                    )
                )

        return EditMediaBatchResponse(results=results, errors=errors)
