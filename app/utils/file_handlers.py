import os
from datetime import datetime

import aiofiles
from fastapi import UploadFile


async def save_upload(file: UploadFile) -> str:
    """
    Save uploaded file with a unique name and return the filepath.
    """
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join("uploads", filename)

    # Save file using aiofiles for async IO
    async with aiofiles.open(filepath, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    return filepath
