from fastapi import HTTPException
from pathlib import Path
from fastapi import UploadFile
from random import uniform
from ..interfaces.video_processing import VideoProcessing
from ..repositories.video import VideoModelRepository


class VideoProcessingImpl(VideoProcessing):
    def __init__(
        self, server_root: Path, upload_dir: Path, repository: VideoModelRepository
    ):
        self.SERVER_ROOT = server_root
        self.UPLOAD_DIR = upload_dir
        self.repository = repository

    async def upload_video(self, file: UploadFile) -> dict:
        if not file.filename.lower().endswith(((".mp4", ".mov"))):
            raise HTTPException(
                status_code=400, detail="Only .mp4 and .mov files are allowed"
            )

        file_path = self.UPLOAD_DIR / f"{file.filename}_{uniform(0, 99999999)}.mp4"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        self.repository.create_video_model_entry(
            video_name=file_path.name, project_id=1
        )  # Replace 1 with the actual project_id

        return {"filename": file_path.name, "status": "uploaded"}

    async def send_video(self, video_name: str) -> bytes:

        file_path = self.UPLOAD_DIR / video_name

        if not file_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Video '{video_name}' not found"
            )

        with open(file_path, "rb") as buffer:
            return buffer.read()
