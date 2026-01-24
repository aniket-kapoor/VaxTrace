from fastapi import UploadFile, HTTPException
import cloudinary.uploader
import uuid
import os

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}


async def save_upload_file(file: UploadFile) -> dict:
    # 1️⃣ Validate extension
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 2️⃣ Validate file size
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    try:
        # 3️⃣ Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file.file,
            folder="vaxtrace/patient_docs/dob",
            resource_type="auto",  # IMPORTANT for PDFs
            public_id=str(uuid.uuid4()),
            allowed_formats=list(ALLOWED_EXTENSIONS),
        )

        # 4️⃣ Return useful info
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "format": result["format"],
            "resource_type": result["resource_type"],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document upload failed: {str(e)}"
        )
