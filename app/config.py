from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # fallback values if .config not set up
    DEBUG_MODE: bool = True
    RETAIN_AUDIO_FOR_DEBUG: bool = True
    MAX_AUDIO_DURATION_SECONDS: int = 300  # 5 minutes
    MAX_FILE_SIZE_MB: int = 25
    ALLOWED_AUDIO_FORMATS: List[str] = ["mp3", "wav", "webm"]
    ANTHROPIC_API_KEY: str  # Add this line

    class Config:
        env_file = ".env"


settings = Settings()
