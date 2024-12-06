from fastapi import FastAPI, File, HTTPException, UploadFile

from app.config import settings
from app.utils.file_handlers import save_upload

app = FastAPI(title="Voice Feedback API")


@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "debug_mode": settings.DEBUG_MODE}


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload an audio file for processing.
    Returns a confirmation of upload with file details.
    """
    # 1. Validate file extension
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in settings.ALLOWED_AUDIO_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Must be one of: {settings.ALLOWED_AUDIO_FORMATS}",
        )

    # 2. Read file content
    content = await file.read()

    # 3. Validate file size
    file_size = len(content) / (1024 * 1024)  # Convert to MB
    if file_size > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File size ({file_size:.2f}MB) exceeds maximum allowed size ({settings.MAX_FILE_SIZE_MB}MB)",
        )

    # Reset file pointer for saving
    await file.seek(0)

    # 4. Save the file
    try:
        filepath = await save_upload(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    return {
        "filename": file.filename,
        "saved_path": filepath,
        "size_mb": file_size,
        "content_type": file.content_type,
        "status": "saved",
    }
