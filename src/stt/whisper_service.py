from __future__ import annotations

import logging
from pathlib import Path

from faster_whisper import WhisperModel

from config import Settings


class WhisperService:
    def __init__(self, settings: Settings, logger: logging.Logger) -> None:
        self.settings = settings
        self.logger = logger
        self.model: WhisperModel | None = None

    def _load_model(self) -> WhisperModel:
        if self.model is None:
            self.logger.info("Loading Faster-Whisper model: %s", self.settings.whisper_model)
            self.model = WhisperModel(
                self.settings.whisper_model,
                device=self.settings.whisper_device,
                compute_type=self.settings.whisper_compute_type,
            )
        return self.model

    def transcribe(self, audio_path: Path) -> str:
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        model = self._load_model()
        segments, _ = model.transcribe(
            str(audio_path),
            beam_size=1,
            vad_filter=True,
            without_timestamps=True,
        )
        transcript = " ".join(segment.text.strip() for segment in segments).strip()
        self.logger.info("Transcript: %s", transcript)
        return transcript
