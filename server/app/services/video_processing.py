from fastapi import HTTPException
from pathlib import Path
from fastapi import UploadFile
from random import uniform
import ffmpeg
from ..interfaces.video_processing import VideoProcessing
from ..repositories.video import VideoModelRepository


class VideoProcessingImpl(VideoProcessing):
    def __init__(
        self, server_root: Path, upload_dir: Path, repository: VideoModelRepository
    ):
        self.SERVER_ROOT = server_root
        self.UPLOAD_DIR = upload_dir
        self.repository = repository

    def __extract_video_metadata(self, file_path: Path) -> dict:
        try:
            probe = ffmpeg.probe(str(file_path))
            video_streams = [s for s in probe["streams"] if s["codec_type"] == "video"]
            video_stream = video_streams[0]
            return {
                "width": int(video_stream["width"]),
                "height": int(video_stream["height"]),
                "duration": float(video_stream["duration"]),
                "codec": video_stream["codec_name"],
                "fps": eval(video_stream["r_frame_rate"]),
                "size_in_bytes": int(probe["format"]["size"]),
            }
        except ffmpeg.Error as e:
            raise ValueError(f"Error probing video: {e.stderr.decode()}")

    async def upload_video(self, file: UploadFile) -> dict:
        if not file.filename.lower().endswith(((".mp4", ".mov"))):
            raise HTTPException(
                status_code=400, detail="Only .mp4 and .mov files are allowed"
            )

        file_path = self.UPLOAD_DIR / f"{file.filename}_{uniform(0, 99999999)}.mp4"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        metadata = self.__extract_video_metadata(file_path)

        self.repository.create_video_model_entry(
            video_name=file_path.name,
            project_id=1,  # Replace 1 with the actual project_id
            width=metadata["width"],
            height=metadata["height"],
            duration=metadata["duration"],
            codec=metadata["codec"],
            size_in_bytes=metadata["size_in_bytes"],
        )

        return {"filename": file_path.name, "status": "uploaded"}

    async def send_video(self, video_name: str) -> bytes:

        file_path = self.UPLOAD_DIR / video_name

        if not file_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Video '{video_name}' not found"
            )

        with open(file_path, "rb") as buffer:
            return buffer.read()
