from __future__ import annotations

import logging
import time
from pathlib import Path

import sounddevice as sd
import soundfile as sf

from config import Settings


class AudioRecorder:
    def __init__(self, settings: Settings, logger: logging.Logger) -> None:
        self.settings = settings
        self.logger = logger

    def record_to_file(self) -> Path:
        output_path = self.settings.output_dir / f"input_{int(time.time() * 1000)}.wav"
        self.logger.info("Recording audio for %s seconds", self.settings.record_seconds)

        audio = sd.rec(
            int(self.settings.record_seconds * self.settings.sample_rate),
            samplerate=self.settings.sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        sf.write(output_path, audio, self.settings.sample_rate)
        self.logger.info("Saved recorded audio to %s", output_path)
        return output_path
