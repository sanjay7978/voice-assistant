from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str
    ollama_model: str
    ollama_num_predict: int
    whisper_model: str
    whisper_device: str
    whisper_compute_type: str
    piper_executable: str
    piper_voice_model: Path
    piper_voice_config: Path
    sample_rate: int
    record_seconds: int
    output_dir: Path
    log_dir: Path
    stt_timeout_seconds: float
    llm_timeout_seconds: float
    tts_timeout_seconds: float


def load_settings() -> Settings:
    load_dotenv()

    settings = Settings(
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2:1b"),
        ollama_num_predict=int(os.getenv("OLLAMA_NUM_PREDICT", "512")),
        whisper_model=os.getenv("WHISPER_MODEL", "base"),
        whisper_device=os.getenv("WHISPER_DEVICE", "cpu"),
        whisper_compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "int8"),
        piper_executable=os.getenv("PIPER_EXECUTABLE", "piper"),
        piper_voice_model=Path(os.getenv("PIPER_VOICE_MODEL", "models/en_US-lessac-medium.onnx")),
        piper_voice_config=Path(os.getenv("PIPER_VOICE_CONFIG", "models/en_US-lessac-medium.onnx.json")),
        sample_rate=int(os.getenv("SAMPLE_RATE", "16000")),
        record_seconds=int(os.getenv("RECORD_SECONDS", "5")),
        output_dir=Path(os.getenv("OUTPUT_DIR", "outputs")),
        log_dir=Path(os.getenv("LOG_DIR", "logs")),
        stt_timeout_seconds=float(os.getenv("STT_TIMEOUT_SECONDS", "20")),
        llm_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "60")),
        tts_timeout_seconds=float(os.getenv("TTS_TIMEOUT_SECONDS", "20")),
    )

    settings.output_dir.mkdir(parents=True, exist_ok=True)
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    Path("models").mkdir(parents=True, exist_ok=True)
    return settings
