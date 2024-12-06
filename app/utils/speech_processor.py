from faster_whisper import WhisperModel


class AudioTranscriber:
    def __init__(self, model_size="base"):
        """Initialize the Whisper model."""
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    async def transcribe(self, audio_path: str) -> dict:
        """
        Transcribe audio file and return transcription with metadata.
        """
        try:
            # Run transcription
            segments, info = self.model.transcribe(audio_path)

            # Compile results
            text = " ".join([segment.text for segment in segments])

            return {
                "text": text,
                "language": info.language,
                "duration": info.duration,
                "success": True,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
