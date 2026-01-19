from fastapi import UploadFile , HTTPException
import shutil
import uuid
import os
from pathlib import Path
from App.core.config import settings

PATIENT_DOCS_PATH = settings.storage_path / "patientDocs"
DOB_DOCS_PATH = PATIENT_DOCS_PATH / "dob"

UPLOAD_DIR = "uploads/dob_documents"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}


async def save_upload_file(file:UploadFile)->str:

    ext=file.filename.split(".")[-1].lower()  #to extract the extension

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    file.file.seek(0)

    
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.{ext}"
    file_path = DOB_DOCS_PATH / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)

