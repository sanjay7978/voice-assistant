from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from pathlib import Path

from config import Settings
from src.audio.player import AudioPlayer
from src.audio.recorder import AudioRecorder
from src.llm.ollama_service import OllamaService
from src.stt.whisper_service import WhisperService
from src.tts.piper_service import PiperService
from src.utils.fallbacks import fallback_for


@dataclass(frozen=True)
class PipelineTimings:
    stt_seconds: float = 0.0
    llm_seconds: float = 0.0
    tts_seconds: float = 0.0
    total_seconds: float = 0.0


@dataclass(frozen=True)
class PipelineResult:
    user_text: str
    assistant_text: str
    audio_path: Path | None
    timings: PipelineTimings
    used_fallback: bool
    warning: str | None = None


class ConversationPipeline:
    def __init__(
        self,
        settings: Settings,
        recorder: AudioRecorder,
        stt_service: WhisperService,
        llm_service: OllamaService,
        tts_service: PiperService,
        player: AudioPlayer,
        logger: logging.Logger,
    ) -> None:
        self.settings = settings
        self.recorder = recorder
        self.stt_service = stt_service
        self.llm_service = llm_service
        self.tts_service = tts_service
        self.player = player
        self.logger = logger

    async def run_once(self) -> PipelineResult:
        started = time.perf_counter()
        used_fallback = False
        audio_path: Path | None = None
        stt_seconds = 0.0
        llm_seconds = 0.0
        tts_seconds = 0.0

        try:
            audio_path = await asyncio.to_thread(self.recorder.record_to_file)
            stt_started = time.perf_counter()
            user_text = await asyncio.wait_for(
                asyncio.to_thread(self.stt_service.transcribe, audio_path),
                timeout=self.settings.stt_timeout_seconds,
            )
            stt_seconds = time.perf_counter() - stt_started
            if not user_text:
                used_fallback = True
                return self._result(
                    "No speech detected",
                    fallback_for("empty_transcript"),
                    None,
                    started,
                    stt_seconds,
                    llm_seconds,
                    tts_seconds,
                    used_fallback,
                )
        except asyncio.TimeoutError:
            self.logger.exception("Speech-to-text timed out")
            return self._fallback_result("Audio input", "slow_stt", started, stt_seconds, llm_seconds, tts_seconds)
        except Exception:
            self.logger.exception("Speech-to-text failed")
            return self._fallback_result("Audio input", "stt_error", started, stt_seconds, llm_seconds, tts_seconds)

        return await self._respond(user_text, started, stt_seconds)

    async def run_text(self, user_text: str) -> PipelineResult:
        started = time.perf_counter()
        return await self._respond(user_text.strip(), started, 0.0)

    async def transcribe_once(self) -> tuple[str, float, float]:
        started = time.perf_counter()
        stt_seconds = 0.0
        try:
            audio_path = await asyncio.to_thread(self.recorder.record_to_file)
            stt_started = time.perf_counter()
            user_text = await asyncio.wait_for(
                asyncio.to_thread(self.stt_service.transcribe, audio_path),
                timeout=self.settings.stt_timeout_seconds,
            )
            stt_seconds = time.perf_counter() - stt_started
            if not user_text:
                return "No speech detected", stt_seconds, started
            return user_text, stt_seconds, started
        except asyncio.TimeoutError:
            self.logger.exception("Speech-to-text timed out")
            return "Audio input", stt_seconds, started
        except Exception:
            self.logger.exception("Speech-to-text failed")
            return "Audio input", stt_seconds, started

    async def generate_text(self, user_text: str) -> tuple[str, float, bool]:
        llm_seconds = 0.0
        try:
            llm_started = time.perf_counter()
            assistant_text = await asyncio.wait_for(
                asyncio.to_thread(self.llm_service.generate, user_text),
                timeout=self.settings.llm_timeout_seconds,
            )
            llm_seconds = time.perf_counter() - llm_started
            return assistant_text, llm_seconds, False
        except asyncio.TimeoutError:
            self.logger.exception("LLM response timed out")
            return fallback_for("slow_llm"), llm_seconds, True
        except Exception:
            self.logger.exception("LLM response failed")
            return fallback_for("llm_error"), llm_seconds, True

    async def speak_text(self, assistant_text: str) -> tuple[Path | None, float, str | None, bool]:
        tts_seconds = 0.0
        if not self.tts_service.is_available():
            warning = self.tts_service.unavailable_message()
            self.logger.warning(warning)
            return None, tts_seconds, warning, True

        try:
            tts_started = time.perf_counter()
            audio_path = await asyncio.wait_for(
                asyncio.to_thread(self.tts_service.synthesize, assistant_text),
                timeout=self.settings.tts_timeout_seconds,
            )
            tts_seconds = time.perf_counter() - tts_started
            await asyncio.to_thread(self.player.play, audio_path)
            return audio_path, tts_seconds, None, False
        except asyncio.TimeoutError:
            self.logger.exception("TTS timed out")
            return None, tts_seconds, fallback_for("tts_error"), True
        except Exception:
            self.logger.exception("TTS or playback failed")
            return None, tts_seconds, fallback_for("tts_error"), True

    async def _respond(self, user_text: str, started: float, stt_seconds: float) -> PipelineResult:
        used_fallback = False
        audio_path: Path | None = None
        llm_seconds = 0.0
        tts_seconds = 0.0

        try:
            llm_started = time.perf_counter()
            assistant_text = await asyncio.wait_for(
                asyncio.to_thread(self.llm_service.generate, user_text),
                timeout=self.settings.llm_timeout_seconds,
            )
            llm_seconds = time.perf_counter() - llm_started
        except asyncio.TimeoutError:
            self.logger.exception("LLM response timed out")
            assistant_text = fallback_for("slow_llm")
            used_fallback = True
        except Exception:
            self.logger.exception("LLM response failed")
            assistant_text = fallback_for("llm_error")
            used_fallback = True

        if not self.tts_service.is_available():
            warning = self.tts_service.unavailable_message()
            self.logger.warning(warning)
            return self._result(
                user_text,
                assistant_text,
                None,
                started,
                stt_seconds,
                llm_seconds,
                tts_seconds,
                True,
                warning=warning,
            )

        try:
            tts_started = time.perf_counter()
            audio_path = await asyncio.wait_for(
                asyncio.to_thread(self.tts_service.synthesize, assistant_text),
                timeout=self.settings.tts_timeout_seconds,
            )
            tts_seconds = time.perf_counter() - tts_started
            await asyncio.to_thread(self.player.play, audio_path)
        except asyncio.TimeoutError:
            self.logger.exception("TTS timed out")
            assistant_text = f"{assistant_text}\n\n{fallback_for('tts_error')}"
            used_fallback = True
        except Exception:
            self.logger.exception("TTS or playback failed")
            assistant_text = f"{assistant_text}\n\n{fallback_for('tts_error')}"
            used_fallback = True

        return self._result(
            user_text,
            assistant_text,
            audio_path,
            started,
            stt_seconds,
            llm_seconds,
            tts_seconds,
            used_fallback,
        )

    def _fallback_result(
        self,
        user_text: str,
        fallback_key: str,
        started: float,
        stt_seconds: float,
        llm_seconds: float,
        tts_seconds: float,
    ) -> PipelineResult:
        return self._result(
            user_text,
            fallback_for(fallback_key),
            None,
            started,
            stt_seconds,
            llm_seconds,
            tts_seconds,
            True,
        )

    @staticmethod
    def _result(
        user_text: str,
        assistant_text: str,
        audio_path: Path | None,
        started: float,
        stt_seconds: float,
        llm_seconds: float,
        tts_seconds: float,
        used_fallback: bool,
        warning: str | None = None,
    ) -> PipelineResult:
        return PipelineResult(
            user_text=user_text,
            assistant_text=assistant_text,
            audio_path=audio_path,
            timings=PipelineTimings(
                stt_seconds=stt_seconds,
                llm_seconds=llm_seconds,
                tts_seconds=tts_seconds,
                total_seconds=time.perf_counter() - started,
            ),
            used_fallback=used_fallback,
            warning=warning,
        )
