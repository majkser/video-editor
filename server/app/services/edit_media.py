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
        has_video = False

        for item in request.edits:
            try:
                result = await self.__edit_media(item.media_id, item.edits)
                all_segments.append(result)
                if result["media_type"] == MediaType.VIDEO:
                    has_video = True
            except (NotFoundError, FfmpegError) as e:
                pass

        output_media_type = MediaType.VIDEO if has_video else MediaType.AUDIO

        target_resolution = (request.target_width, request.target_height)
        target_fps = request.target_fps
        target_sample_rate = request.target_sample_rate

        if all_segments:
            output_filename = f"combined_edited_{uuid.uuid4()}.{request.output_format}"
            output_path = self.UPLOAD_DIR / output_filename
            self.__combine_streams_into_output(
                all_segments,
                output_path,
                output_media_type,
                target_resolution,
                target_fps,
                target_sample_rate,
            )

            self.repository.create_media_model_entry(
                MediaModel(
                    media_name=output_filename,
                    media_original_name=output_filename,
                    media_type=output_media_type,
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
        video_streams = []
        audio_streams = []

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
                    video_streams.append(v_cut)
                    audio_streams.append(a_cut)
                elif media_file.media_type == MediaType.AUDIO:
                    a_cut = stream.filter_("atrim", start=start, end=end).filter_(
                        "asetpts", "PTS-STARTPTS"
                    )
                    audio_streams.append(a_cut)
        else:
            if media_file.media_type == MediaType.VIDEO:
                video_streams.append(stream.video)
                audio_streams.append(stream.audio)
            else:
                audio_streams.append(stream)

        return {
            "video_streams": video_streams,
            "audio_streams": audio_streams,
            "media_type": media_file.media_type,
            "media_id": media_id,
        }

    def __combine_streams_into_output(
        self,
        all_segments: list[dict],
        output_path: Path,
        output_media_type: MediaType,
        target_resolution: tuple[int, int],
        target_fps: float,
        target_sample_rate: int,
    ):
        all_video_streams = []
        all_audio_streams = []

        for segment in all_segments:

            for v in segment["video_streams"]:
                v = v.filter("scale", target_resolution[0], target_resolution[1])
                v = v.filter("setsar", "1/1")
                v = v.filter("fps", fps=target_fps)
                v = v.filter("format", "yuv420p")
                all_video_streams.append(v)

            for a in segment["audio_streams"]:
                a = a.filter("aresample", target_sample_rate)
                all_audio_streams.append(a)

        if output_media_type == MediaType.VIDEO:

            if len(all_video_streams) == len(all_audio_streams):
                interleaved_streams = []
                for v, a in zip(all_video_streams, all_audio_streams):
                    interleaved_streams.append(v)
                    interleaved_streams.append(a)
                out = ffmpeg.concat(*interleaved_streams, v=1, a=1)
                ffmpeg.output(out, str(output_path)).overwrite_output().run(quiet=True)

            else:
                video_part = (
                    ffmpeg.concat(*all_video_streams, v=1, a=0)
                    if len(all_video_streams) > 1
                    else all_video_streams[0]
                )
                audio_part = (
                    ffmpeg.concat(*all_audio_streams, v=0, a=1)
                    if len(all_audio_streams) > 1
                    else all_audio_streams[0]
                )

                ffmpeg.output(
                    video_part, audio_part, str(output_path)
                ).overwrite_output().run(quiet=True)

        else:
            out = (
                ffmpeg.concat(*all_audio_streams, v=0, a=1)
                if len(all_audio_streams) > 1
                else all_audio_streams[0]
            )
            ffmpeg.output(out, str(output_path)).overwrite_output().run(quiet=True)
