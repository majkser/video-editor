from ..interfaces.still_video import StillVideo
from app.repositories.media import MediaModelRepository
from pathlib import Path
import ffmpeg

class StillVideoImpl(StillVideo):
    def __init__(
        self, server_root: Path, upload_dir: Path, repository: MediaModelRepository
    ):
        self.SERVER_ROOT = server_root
        self.UPLOAD_DIR = upload_dir
        self.repository = repository
    
    async def combine_still_with_audio(self, still_id: int, audio_id: int) -> dict:
        still = self.repository.get_media_model_by_id(still_id)
        audio = self.repository.get_media_model_by_id(audio_id)

        if not still or still.media_type != "image":
            raise ValueError(f"Still image with ID {still_id} not found or is not an image.")
        
        if not audio or audio.media_type != "audio":
            raise ValueError(f"Audio file with ID {audio_id} not found or is not an audio file.")

        output_filename = f"{still.media_name.split('.')[0]}_with_{audio.media_name.split('.')[0]}.mp4"
        output_path = self.UPLOAD_DIR / output_filename

        try:
            (
                ffmpeg.output(
                    ffmpeg.input(str(self.SERVER_ROOT / self.UPLOAD_DIR / still.media_name), loop=1),
                    ffmpeg.input(str(self.SERVER_ROOT / self.UPLOAD_DIR / audio.media_name)),
                    str(output_path),
                    vcodec="libx264",
                    shortest=None,
                    tune="stillimage"
                )
                .overwrite_output()
                .run()
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Error combining still and audio: {e.stderr.decode()}")