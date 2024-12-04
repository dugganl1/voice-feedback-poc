from fastapi import FastAPI

from app.config import settings

app = FastAPI(title="Voice Feedback API")


@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "debug_mode": settings.DEBUG_MODE}
