from __future__ import annotations

import logging
import shutil
import subprocess
import time
from pathlib import Path

from config import Settings


class PiperService:
    def __init__(self, settings: Settings, logger: logging.Logger) -> None:
        self.settings = settings
        self.logger = logger

    def executable_exists(self) -> bool:
        executable = self.settings.piper_executable
        executable_path = Path(executable)
        if executable_path.parent != Path("."):
            return executable_path.exists()
        return shutil.which(executable) is not None

    def voice_model_exists(self) -> bool:
        return self.settings.piper_voice_model.exists()

    def voice_config_exists(self) -> bool:
        return self.settings.piper_voice_config.exists()

    def is_available(self) -> bool:
        return self.executable_exists() and self.voice_model_exists() and self.voice_config_exists()

    def unavailable_message(self) -> str:
        if not self.executable_exists():
            return (
                "Offline voice output is unavailable because Piper is not installed. "
                "The assistant will continue with text responses. Install Piper from "
                "https://github.com/rhasspy/piper/releases, then ensure `PIPER_EXECUTABLE` in `.env` "
                "points to the `piper` command."
            )
        if not self.voice_model_exists():
            return (
                f"Offline voice output is unavailable because the Piper voice model was not found at "
                f"`{self.settings.piper_voice_model}`. The assistant will continue with text responses. "
                "Download a Piper `.onnx` voice and its matching `.onnx.json` config from "
                "https://github.com/rhasspy/piper/blob/master/VOICES.md, place both files in `models/`, "
                "then update `PIPER_VOICE_MODEL` and `PIPER_VOICE_CONFIG` in `.env`."
            )
        if not self.voice_config_exists():
            return (
                f"Offline voice output is unavailable because the Piper voice config was not found at "
                f"`{self.settings.piper_voice_config}`. The assistant will continue with text responses. "
                "Download the matching `.onnx.json` config for your Piper voice and update "
                "`PIPER_VOICE_CONFIG` in `.env`."
            )
        return "Offline voice output is unavailable because Piper is not ready."

    def missing_model_message(self) -> str:
        return self.unavailable_message()

    def synthesize(self, text: str) -> Path:
        if not self.is_available():
            self.logger.warning(self.unavailable_message())
            raise RuntimeError(self.unavailable_message())

        output_path = self.settings.output_dir / f"response_{int(time.time() * 1000)}.wav"
        command = [
            self.settings.piper_executable,
            "--model",
            str(self.settings.piper_voice_model),
            "--config",
            str(self.settings.piper_voice_config),
            "--output_file",
            str(output_path),
        ]

        self.logger.info(
            "Generating speech with Piper executable=%s model=%s config=%s output=%s",
            self.settings.piper_executable,
            self.settings.piper_voice_model,
            self.settings.piper_voice_config,
            output_path,
        )
        completed = subprocess.run(
            command,
            input=text,
            text=True,
            capture_output=True,
            timeout=self.settings.tts_timeout_seconds,
            check=False,
        )
        if completed.returncode != 0:
            self.logger.error(
                "Piper failed with return code %s. stdout=%s stderr=%s",
                completed.returncode,
                completed.stdout.strip(),
                completed.stderr.strip(),
            )
            raise RuntimeError(completed.stderr.strip() or "Piper failed to generate speech")
        if not output_path.exists():
            self.logger.error("Piper completed but output file was not created: %s", output_path)
            raise RuntimeError("Piper completed but did not create an audio file")
        self.logger.info("Piper generated audio file: %s", output_path)
        return output_path
