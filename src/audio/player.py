from __future__ import annotations

import logging
from pathlib import Path

import sounddevice as sd
import soundfile as sf


class AudioPlayer:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def play(self, audio_path: Path) -> None:
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        self.logger.info("Playing audio file %s", audio_path)
        audio, sample_rate = sf.read(audio_path, dtype="float32")
        sd.play(audio, samplerate=sample_rate)
        sd.wait()
