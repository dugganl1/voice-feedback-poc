from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG_MODE: bool = True
    RETAIN_AUDIO_FOR_DEBUG: bool = True
    MAX_AUDIO_DURATION_SECONDS: int = 300  # 5 minutes
    MAX_FILE_SIZE_MB: int = 25
    ALLOWED_AUDIO_FORMATS: List[str] = ["mp3", "wav"]

    class Config:
        env_file = ".env"


settings = Settings()
