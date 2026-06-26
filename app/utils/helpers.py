import os
import uuid
from fastapi import UploadFile


UPLOAD_DIR = "uploads"


async def save_upload_file(file: UploadFile, folder: str) -> str:
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    save_path = os.path.join(UPLOAD_DIR, folder, filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return save_path
