from __future__ import annotations


FALLBACKS: dict[str, str] = {
    "slow_stt": "I am still catching that. Could you repeat it once more?",
    "stt_error": "I had trouble understanding the audio. Please try speaking again.",
    "empty_transcript": "I did not catch enough audio. Please try again.",
    "slow_llm": "I am thinking through that. Give me a moment and ask again.",
    "llm_error": "I am having trouble forming a response right now. Could you ask that another way?",
    "tts_error": "I generated a response, but I could not speak it out loud.",
}


def fallback_for(key: str) -> str:
    return FALLBACKS.get(key, "Something slowed down. Please try again.")
