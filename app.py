from __future__ import annotations

import asyncio
import os
import random
import time
from typing import Any, Dict, Generator, List

os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
os.environ.setdefault("GRADIO_SERVER_NAME", "127.0.0.1")

import gradio as gr

from config import Settings, load_settings
from src.audio.player import AudioPlayer
from src.audio.recorder import AudioRecorder
from src.llm.ollama_service import OllamaService
from src.pipeline.conversation_pipeline import ConversationPipeline
from src.stt.whisper_service import WhisperService
from src.tts.piper_service import PiperService
from src.utils.logger import configure_logger

ChatMessage = Dict[str, str]
ChatHistory = List[ChatMessage]

ACKNOWLEDGEMENTS = [
    "🤔 Let me think about that...",
    "🧠 I'm thinking...",
    "💭 Give me a moment...",
]


settings: Settings = load_settings()
logger = configure_logger(settings.log_dir)

recorder = AudioRecorder(settings=settings, logger=logger)
player = AudioPlayer(logger=logger)
stt_service = WhisperService(settings=settings, logger=logger)
llm_service = OllamaService(settings=settings, logger=logger)
tts_service = PiperService(settings=settings, logger=logger)

pipeline = ConversationPipeline(
    settings=settings,
    recorder=recorder,
    stt_service=stt_service,
    llm_service=llm_service,
    tts_service=tts_service,
    player=player,
    logger=logger,
)


def _safe_text(value):
    if value is None:
        return ""

    if isinstance(value, list):
        if value and isinstance(value[0], dict):
            return value[0].get("text", "")
        return ""

    if isinstance(value, dict):
        return value.get("text", "")

    return str(value)


def _normalize_history(history: Any) -> ChatHistory:
    normalized: ChatHistory = []
    if not history:
        return normalized

    for item in history:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")
            if role in {"user", "assistant"} and content is not None:
                normalized.append({"role": role, "content": _safe_text(content)})
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_text, assistant_text = item
            if user_text is not None:
                normalized.append({"role": "user", "content": _safe_text(user_text)})
            if assistant_text is not None:
                normalized.append({"role": "assistant", "content": _safe_text(assistant_text)})
    return normalized


def _append_exchange(history: ChatHistory, user_text: str, assistant_text: str) -> ChatHistory:
    history = _normalize_history(history)
    history.append({"role": "user", "content": _safe_text(user_text)})
    history.append({"role": "assistant", "content": _safe_text(assistant_text)})
    return history


def _append_message(history: ChatHistory, role: str, content: str) -> ChatHistory:
    history = _normalize_history(history)
    history.append({"role": role, "content": _safe_text(content)})
    return history


def _replace_last_assistant(history: ChatHistory, content: str) -> ChatHistory:
    history = _normalize_history(history)
    for index in range(len(history) - 1, -1, -1):
        if history[index]["role"] == "assistant":
            history[index] = {"role": "assistant", "content": _safe_text(content)}
            return history
    return _append_message(history, "assistant", content)


def _acknowledgement() -> str:
    return random.choice(ACKNOWLEDGEMENTS)


def _status_from_result(result: Any, include_stt: bool) -> str:
    parts = []
    if include_stt:
        parts.append(f"STT: {result.timings.stt_seconds:.2f}s")
    parts.extend(
        [
            f"LLM: {result.timings.llm_seconds:.2f}s",
            f"TTS: {result.timings.tts_seconds:.2f}s",
            f"Total: {result.timings.total_seconds:.2f}s",
        ]
    )
    if result.used_fallback:
        parts.append("Fallback/text-only mode used")
    if result.warning:
        parts.append(result.warning)
    return " | ".join(parts)


def _ui_error(history: ChatHistory, user_text: str, error: Exception) -> tuple[ChatHistory, str]:
    logger.exception("UI request failed")
    assistant_text = "Something went wrong in the app UI, but the assistant is still running. Please try again."
    return _append_exchange(history, user_text, assistant_text), f"UI error handled: {error}"


def record_and_respond(history: ChatHistory) -> tuple[ChatHistory, str]:
    history = _normalize_history(history)
    try:
        result = asyncio.run(pipeline.run_once())
    except Exception as error:
        return _ui_error(history, "Audio input", error)

    history = _append_exchange(history, result.user_text, result.assistant_text)
    status = (
        _status_from_result(result, include_stt=True)
    )
    return history, status


def text_and_respond(message: str, history: ChatHistory) -> tuple[str, ChatHistory, str]:
    history = _normalize_history(history)
    if not message.strip():
        return "", history, "Type a message or use the microphone button."

    try:
        result = asyncio.run(pipeline.run_text(message))
    except Exception as error:
        next_history, status = _ui_error(history, message, error)
        return "", next_history, status

    history = _append_exchange(history, result.user_text, result.assistant_text)
    status = _status_from_result(result, include_stt=False)
    return "", history, status


def text_and_respond_stream(
    message: str,
    history: ChatHistory,
) -> Generator[tuple[str, ChatHistory, str], None, None]:
    history = _normalize_history(history)
    user_text = message.strip()
    if not user_text:
        yield "", history, "Ready | Type a message or use the microphone button."
        return

    started = time.perf_counter()
    history = _append_message(history, "user", user_text)
    history = _append_message(history, "assistant", _acknowledgement())
    yield "", history, "Thinking | Generating response."

    try:
        assistant_text, llm_seconds, used_fallback = asyncio.run(pipeline.generate_text(user_text))
    except Exception as error:
        logger.exception("UI text request failed during LLM stage")
        assistant_text = "I had trouble thinking that through. Please try again."
        llm_seconds = 0.0
        used_fallback = True
        yield "", _replace_last_assistant(history, assistant_text), f"Ready | Conversational fallback used: {error}"
        return

    history = _replace_last_assistant(history, assistant_text)
    yield "", history, f"Speaking | LLM: {llm_seconds:.2f}s"

    try:
        _, tts_seconds, warning, tts_fallback = asyncio.run(pipeline.speak_text(assistant_text))
    except Exception as error:
        logger.exception("UI text request failed during speech stage")
        warning = f"Voice output failed, but the text response is ready: {error}"
        tts_seconds = 0.0
        tts_fallback = True

    total_seconds = time.perf_counter() - started
    status_parts = [
        "Ready",
        f"LLM: {llm_seconds:.2f}s",
        f"TTS: {tts_seconds:.2f}s",
        f"Total: {total_seconds:.2f}s",
    ]
    if used_fallback or tts_fallback:
        status_parts.append("Fallback used")
    if warning:
        status_parts.append(warning)
    yield "", history, " | ".join(status_parts)


def record_and_respond_stream(history: ChatHistory) -> Generator[tuple[ChatHistory, str], None, None]:
    history = _normalize_history(history)
    history = _append_message(history, "assistant", _acknowledgement())
    yield history, "Listening | Recording audio."

    try:
        user_text, stt_seconds, started = asyncio.run(pipeline.transcribe_once())
    except Exception as error:
        logger.exception("UI voice request failed during listening/STT stage")
        history = _replace_last_assistant(history, "I had trouble hearing that. Please try again.")
        yield history, f"Ready | Conversational fallback used: {error}"
        return

    if user_text in {"No speech detected", "Audio input"}:
        fallback = "I did not catch enough audio. Please try again."
        history = _replace_last_assistant(history, fallback)
        yield history, f"Ready | STT: {stt_seconds:.2f}s | Conversational fallback used"
        return

    history = _normalize_history(history)
    if history and history[-1]["role"] == "assistant":
        history.pop()
    history = _append_message(history, "user", user_text)
    history = _append_message(history, "assistant", _acknowledgement())
    yield history, f"Speech Recognized | STT: {stt_seconds:.2f}s"
    yield history, "Thinking | Generating response."

    try:
        assistant_text, llm_seconds, used_fallback = asyncio.run(pipeline.generate_text(user_text))
    except Exception as error:
        logger.exception("UI voice request failed during LLM stage")
        assistant_text = "I had trouble thinking that through. Please try again."
        llm_seconds = 0.0
        used_fallback = True
        yield _replace_last_assistant(history, assistant_text), f"Ready | Conversational fallback used: {error}"
        return

    history = _replace_last_assistant(history, assistant_text)
    yield history, f"Speaking | LLM: {llm_seconds:.2f}s"

    try:
        _, tts_seconds, warning, tts_fallback = asyncio.run(pipeline.speak_text(assistant_text))
    except Exception as error:
        logger.exception("UI voice request failed during speech stage")
        warning = f"Voice output failed, but the text response is ready: {error}"
        tts_seconds = 0.0
        tts_fallback = True

    total_seconds = time.perf_counter() - started
    status_parts = [
        "Ready",
        f"STT: {stt_seconds:.2f}s",
        f"LLM: {llm_seconds:.2f}s",
        f"TTS: {tts_seconds:.2f}s",
        f"Total: {total_seconds:.2f}s",
    ]
    if used_fallback or tts_fallback:
        status_parts.append("Fallback used")
    if warning:
        status_parts.append(warning)
    yield history, " | ".join(status_parts)


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Offline Voice Assistant") as demo:
        gr.Markdown("# Offline Voice Assistant")
        gr.Markdown("Speak into your microphone or type a test message. All AI components run locally.")
        if not tts_service.is_available():
            gr.Markdown(f"**Piper warning:** {tts_service.unavailable_message()}")

        chatbot = gr.Chatbot(
    label="Conversation",
    height=420,
)
        status = gr.Textbox(label="Status", value="Ready", interactive=False)

        with gr.Row():
            record_button = gr.Button("Record and Respond", variant="primary")
            clear_button = gr.Button("Clear")

        with gr.Row():
            text_input = gr.Textbox(
                label="Text test input",
                placeholder="Type a message to test the LLM and TTS pipeline...",
                scale=4,
            )
            send_button = gr.Button("Send", scale=1)

        record_button.click(
            fn=record_and_respond_stream,
            inputs=[chatbot],
            outputs=[chatbot, status],
        )
        send_button.click(
            fn=text_and_respond_stream,
            inputs=[text_input, chatbot],
            outputs=[text_input, chatbot, status],
        )
        text_input.submit(
            fn=text_and_respond_stream,
            inputs=[text_input, chatbot],
            outputs=[text_input, chatbot, status],
        )
        clear_button.click(lambda: ([], "Ready"), outputs=[chatbot, status])

    return demo.queue(status_update_rate="auto", default_concurrency_limit=2)


if __name__ == "__main__":
    logger.info("Starting Gradio app")
    demo = build_ui()
    for port in range(7860, 7870):
        try:
            demo.launch(
                server_name="127.0.0.1",
                server_port=port,
                share=False,
                inbrowser=False,
            )
            break
        except OSError:
            logger.warning("Port %s is unavailable, trying the next port", port)
    else:
        raise RuntimeError("Could not start Gradio on ports 7860-7869.")
