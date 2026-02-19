from fastapi import HTTPException
from pathlib import Path
from fastapi import UploadFile
from random import uniform
import ffmpeg
from PIL import Image
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
        file_ext = Path(file.filename).suffix.lower()
        all_extensions = (
            MediaProcessingImpl.VIDEO_EXTENSIONS
            + MediaProcessingImpl.AUDIO_EXTENSIONS
            + MediaProcessingImpl.IMAGE_EXTENSIONS
        )

        if file_ext not in all_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: Videos {MediaProcessingImpl.VIDEO_EXTENSIONS}, Audio {MediaProcessingImpl.AUDIO_EXTENSIONS}, Images {MediaProcessingImpl.IMAGE_EXTENSIONS}",
            )

        file_path = (
            self.UPLOAD_DIR
            / f"{file.filename.split('.')[0]}_{uniform(0, 99999999)}.{file.filename.split('.')[-1]}"
        )
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        metadata = self.__extract_media_metadata(file_path)

        media_model = MediaModel(
            media_name=file_path.name,
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
            "filename": file_path.name,
            "media_type": metadata["media_type"].value,
            "status": "uploaded",
        }

    async def send_media(self, media_name: str) -> bytes:

        file_path = self.UPLOAD_DIR / media_name

        if not file_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Media '{media_name}' not found"
            )

        with open(file_path, "rb") as buffer:
            return buffer.read()

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
            raise ValueError(f"Unknown media type for extension: {ext}")

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
                        raise ValueError("No video stream found in file")
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
                        raise ValueError("No audio stream found in file")
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
                    raise ValueError(f"Unsupported media type: {media_type}")

        except Exception as e:
            raise ValueError(f"Error extracting media metadata: {str(e)}")
