from __future__ import annotations

import logging

import requests

from config import Settings


class OllamaService:
    def __init__(self, settings: Settings, logger: logging.Logger) -> None:
        self.settings = settings
        self.logger = logger

    def generate(self, user_text: str) -> str:
        payload = {
            "model": self.settings.ollama_model,
            "prompt": self._build_prompt(user_text),
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": self.settings.ollama_num_predict,
            },
        }
        response = requests.post(
            f"{self.settings.ollama_base_url}/api/generate",
            json=payload,
            timeout=self.settings.llm_timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        assistant_text = str(data.get("response", "")).strip()
        if not assistant_text:
            raise RuntimeError("Ollama returned an empty response")
        if data.get("done_reason") == "length":
            self.logger.warning(
                "Ollama stopped because it reached OLLAMA_NUM_PREDICT=%s. Increase this value for longer answers.",
                self.settings.ollama_num_predict,
            )
        self.logger.info("LLM response: %s", assistant_text)
        return assistant_text

    @staticmethod
    def _build_prompt(user_text: str) -> str:
        return (
            "You are a concise, helpful voice assistant. "
            "Answer naturally in one to three short sentences. "
            "Do not mention that you are offline unless asked.\n\n"
            f"User: {user_text}\n"
            "Assistant:"
        )
