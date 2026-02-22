from pathlib import Path
from fastapi import UploadFile
import uuid
import ffmpeg
from PIL import Image

from app.error_handler.error_handler import FfmpegError, NotFoundError, ValidationError
from ..interfaces.media_processing import MediaProcessing
from ..repositories.media import MediaModelRepository
from ..models.media import MediaModel, MediaType


class MediaProcessingImpl(MediaProcessing):
    VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi", ".webm")
    AUDIO_EXTENSIONS = (".mp3", ".wav")
    IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp")

    def __init__(
        self, server_root: Path, upload_dir: Path, repository: MediaModelRepository
    ):
        self.SERVER_ROOT = server_root
        self.UPLOAD_DIR = upload_dir
        self.repository = repository

    async def upload_media(self, file: UploadFile) -> dict:
        # Check if file extension is supported
        file_extension = Path(file.filename).suffix.lower()
        all_extensions = (
            MediaProcessingImpl.VIDEO_EXTENSIONS
            + MediaProcessingImpl.AUDIO_EXTENSIONS
            + MediaProcessingImpl.IMAGE_EXTENSIONS
        )

        if file_extension not in all_extensions:
            raise ValidationError(
                f"Unsupported file type. Allowed: Videos {MediaProcessingImpl.VIDEO_EXTENSIONS}, Audio {MediaProcessingImpl.AUDIO_EXTENSIONS}, Images {MediaProcessingImpl.IMAGE_EXTENSIONS}",
            )

        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = self.UPLOAD_DIR / unique_filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        metadata = self.__extract_media_metadata(file_path)

        media_model = MediaModel(
            media_name=unique_filename,
            media_original_name=file.filename,
            media_type=metadata.get("media_type"),
            project_id=1,  # TODO: Replace 1 with the actual project_id
            width=metadata.get("width"),
            height=metadata.get("height"),
            duration=metadata.get("duration"),
            codec=metadata.get("codec"),
            fps=metadata.get("fps"),
            size_in_bytes=metadata.get("size_in_bytes"),
        )

        self.repository.create_media_model_entry(media_model)

        return {
            "filename": file.filename,
            "media_type": metadata["media_type"].value,
            "status": "uploaded",
        }

    async def send_media(self, media_id: int) -> tuple[bytes, str]:

        media = self.repository.get_media_model_by_id(media_id)

        if media is None:
            raise NotFoundError(f"Media with id {media_id} not found")

        media_name = media.media_name
        file_path = self.UPLOAD_DIR / media_name

        if not file_path.exists():
            raise NotFoundError(f"Media file '{media_name}' not found on disk")

        with open(file_path, "rb") as buffer:
            return buffer.read(), media.media_orginal_name

    @staticmethod
    def __get_media_type(file_path: Path) -> MediaType:
        ext = file_path.suffix.lower()
        if ext in MediaProcessingImpl.VIDEO_EXTENSIONS:
            return MediaType.VIDEO
        elif ext in MediaProcessingImpl.AUDIO_EXTENSIONS:
            return MediaType.AUDIO
        elif ext in MediaProcessingImpl.IMAGE_EXTENSIONS:
            return MediaType.IMAGE
        else:
            raise ValidationError(f"Unknown media type for extension: {ext}")

    @staticmethod
    def __extract_media_metadata(file_path: Path) -> dict:
        media_type = MediaProcessingImpl.__get_media_type(file_path)

        try:
            if media_type == MediaType.IMAGE:
                with Image.open(file_path) as img:
                    return {
                        "media_type": MediaType.IMAGE,
                        "width": img.width,
                        "height": img.height,
                        "codec": img.format,
                        "size_in_bytes": file_path.stat().st_size,
                    }
            else:
                probe = ffmpeg.probe(str(file_path))

                if media_type == MediaType.VIDEO:
                    video_streams = [
                        s for s in probe["streams"] if s["codec_type"] == "video"
                    ]
                    if not video_streams:
                        raise FfmpegError("No video stream found in file")
                    video_stream = video_streams[0]

                    return {
                        "media_type": MediaType.VIDEO,
                        "width": int(video_stream["width"]),
                        "height": int(video_stream["height"]),
                        "duration": float(
                            video_stream.get(
                                "duration", probe["format"].get("duration", 0)
                            )
                        ),
                        "codec": video_stream["codec_name"],
                        "fps": (
                            eval(video_stream["r_frame_rate"])
                            if "r_frame_rate" in video_stream
                            else None
                        ),
                        "size_in_bytes": int(probe["format"]["size"]),
                    }
                elif media_type == MediaType.AUDIO:
                    audio_streams = [
                        s for s in probe["streams"] if s["codec_type"] == "audio"
                    ]
                    if not audio_streams:
                        raise FfmpegError("No audio stream found in file")
                    audio_stream = audio_streams[0]

                    return {
                        "media_type": MediaType.AUDIO,
                        "duration": float(
                            audio_stream.get(
                                "duration", probe["format"].get("duration", 0)
                            )
                        ),
                        "codec": audio_stream["codec_name"],
                        "size_in_bytes": int(probe["format"]["size"]),
                    }
                else:
                    raise ValidationError(f"Unsupported media type: {media_type}")

        except Exception as e:
            raise FfmpegError(f"Error extracting media metadata: {str(e)}")
