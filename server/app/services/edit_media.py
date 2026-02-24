import uuid
from zipfile import Path

from app.error_handler.error_handler import FfmpegError, NotFoundError
from app.interfaces.edit_media import EditMedia
import ffmpeg

from app.models.media import MediaModel, MediaType
from app.repositories.media import MediaModelRepository
from app.schemas.edit_media import (
    EditMediaBatchRequest,
    EditMediaBatchResponse,
    EditMediaModel,
)


class EditMediaImpl(EditMedia):
    def __init__(
        self, server_root: Path, upload_dir: Path, repository: MediaModelRepository
    ):
        self.SERVER_ROOT = server_root
        self.UPLOAD_DIR = upload_dir
        self.repository = repository

    async def edit_media_batch(
        self, request: EditMediaBatchRequest
    ) -> EditMediaBatchResponse:
        all_segments = []
        media_type = None

        for item in request.edits:
            try:
                result = await self.__edit_media(item.media_id, item.edits)
                all_segments.append(result)
                if media_type is None:
                    media_type = result["media_type"]
            except (NotFoundError, FfmpegError) as e:
                pass

        target_resolution = (request.target_width, request.target_height)
        target_fps = request.target_fps
        target_sample_rate = request.target_sample_rate

        if all_segments:
            output_filename = f"combined_edited_{uuid.uuid4()}.{request.output_format}"
            output_path = self.UPLOAD_DIR / output_filename
            self.__combine_streams_into_output(
                all_segments,
                output_path,
                media_type,
                target_resolution,
                target_fps,
                target_sample_rate,
            )

            self.repository.create_media_model_entry(
                MediaModel(
                    media_name=output_filename,
                    media_original_name=output_filename,
                    media_type=media_type,
                    project_id=request.project_id,
                    width=target_resolution[0],
                    height=target_resolution[1],
                    duration=ffmpeg.probe(str(output_path))["format"]["duration"],
                    codec=ffmpeg.probe(str(output_path))["streams"][0][
                        "codec_name"
                    ],  # TODO: allow user to choose codec (add req param)
                    fps=target_fps,
                    size_in_bytes=output_path.stat().st_size,
                )
            )

            return EditMediaBatchResponse(status="success")
        else:
            raise NotFoundError("No valid media edits were found to process.")

    async def __edit_media(self, media_id: int, edits: EditMediaModel) -> dict:
        media_file = self.repository.get_media_model_by_id(media_id)
        if not media_file:
            raise NotFoundError(f"Media file with ID {media_id} not found")
        input_path = self.UPLOAD_DIR / media_file.media_name

        stream = ffmpeg.input(str(input_path))
        streams_to_concat = []

        if edits.cuts:
            for cut in edits.cuts:
                start, end = cut.start, cut.end

                if media_file.media_type == MediaType.VIDEO:
                    v_cut = stream.video.trim(start=start, end=end).setpts(
                        "PTS-STARTPTS"
                    )
                    a_cut = stream.audio.filter_("atrim", start=start, end=end).filter_(
                        "asetpts", "PTS-STARTPTS"
                    )
                    streams_to_concat.append(v_cut)
                    streams_to_concat.append(a_cut)
                elif media_file.media_type == MediaType.AUDIO:
                    a_cut = stream.filter_("atrim", start=start, end=end).filter_(
                        "asetpts", "PTS-STARTPTS"
                    )
                    streams_to_concat.append(a_cut)
        else:
            if media_file.media_type == MediaType.VIDEO:
                streams_to_concat.append(stream.video)
                streams_to_concat.append(stream.audio)
            else:
                streams_to_concat.append(stream)

        return {
            "streams": streams_to_concat,
            "media_type": media_file.media_type,
            "media_id": media_id,
        }

    def __combine_streams_into_output(
        self,
        all_segments: list[dict],
        output_path: Path,
        media_type: MediaType,
        target_resolution: tuple[int, int],
        target_fps: float,
        target_sample_rate: int,
    ):
        all_streams = []
        for segment in all_segments:
            streams = segment["streams"]

            if media_type == MediaType.VIDEO:
                normalized_streams = []
                for i in range(0, len(streams), 2):
                    v_stream = streams[i]
                    a_stream = streams[i + 1]

                    v_stream = v_stream.filter(
                        "scale", target_resolution[0], target_resolution[1]
                    )
                    v_stream = v_stream.filter("setsar", "1/1")
                    v_stream = v_stream.filter("fps", fps=target_fps)
                    v_stream = v_stream.filter("format", "yuv420p")

                    a_stream = a_stream.filter("aresample", target_sample_rate)

                    normalized_streams.append(v_stream)
                    normalized_streams.append(a_stream)
                all_streams.extend(normalized_streams)
            else:
                normalized_streams = []
                for stream in streams:
                    stream = stream.filter("aresample", target_sample_rate)
                    normalized_streams.append(stream)
                all_streams.extend(normalized_streams)

        v = 1 if media_type == MediaType.VIDEO else 0
        combined_stream = ffmpeg.concat(*all_streams, v=v, a=1)
        ffmpeg.output(combined_stream, str(output_path)).overwrite_output().run(
            quiet=True
        )
