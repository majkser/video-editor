from fastapi import APIRouter, HTTPException
from pathlib import Path
from fastapi import UploadFile
from random import uniform

router = APIRouter()

SERVER_ROOT = Path(__file__).parent.parent.parent.parent
UPLOAD_DIR = SERVER_ROOT / "uploaded_videos"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload_video")
async def upload_video(file: UploadFile) -> dict:
    if not file.filename.lower().endswith(((".mp4", ".mov"))):
        raise HTTPException(status_code=400, detail="Only .mp4 and .mov files are allowed")
    
    file_path = UPLOAD_DIR / f"{file.filename}_{uniform(0, 99999999)}.mp4"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {"filename": file_path.name, "status": "uploaded"}
    