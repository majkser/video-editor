from app.error_handler.error_handler import FfmpegError, NotFoundError, ValidationError
from app.models.media import MediaType

from ..interfaces.still_video import StillVideo
from app.repositories.media import MediaModelRepository
from pathlib import Path
from app.schemas.still_video import StillVideoResult
import ffmpeg


class StillVideoImpl(StillVideo):
    def __init__(
        self, server_root: Path, upload_dir: Path, repository: MediaModelRepository
    ):
        self.SERVER_ROOT = server_root
        self.UPLOAD_DIR = upload_dir
        self.repository = repository

    async def combine_still_with_audio(
        self, still_id: int, audio_id: int
    ) -> StillVideoResult:
        still = self.repository.get_media_model_by_id(still_id)
        audio = self.repository.get_media_model_by_id(audio_id)

        if not still:
            raise NotFoundError(f"Still image with ID {still_id} not found.")
        elif still.media_type != MediaType.IMAGE:
            raise ValidationError(
                f"{still.media_name} is not an image file, it is a {still.media_type}."
            )

        if not audio:
            raise NotFoundError(f"Audio file with ID {audio_id} not found.")
        elif audio.media_type != MediaType.AUDIO:
            raise ValidationError(
                f"{audio.media_name} is not an audio file, it is a {audio.media_type}."
            )

        still_path = str(self.SERVER_ROOT / self.UPLOAD_DIR / still.media_name)
        audio_path = str(self.SERVER_ROOT / self.UPLOAD_DIR / audio.media_name)
        output_filename = f"{still.media_original_name.split('.')[0]}_with_{audio.media_original_name.split('.')[0]}.mp4"
        output_path = self.UPLOAD_DIR / output_filename

        try:
            (
                ffmpeg.output(
                    ffmpeg.input(still_path, loop=1),
                    ffmpeg.input(audio_path),
                    str(output_path),
                    vcodec="libx264",
                    shortest=None,
                    tune="stillimage",
                )
                .overwrite_output()
                .run(quiet=True)
            )
        except ffmpeg.Error as e:
            raise FfmpegError(f"Error combining still and audio: {e.stderr.decode()}")

        return StillVideoResult(video_path=str(output_path), video_name=output_filename)
