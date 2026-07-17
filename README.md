# Real-Time Offline Conversational AI Assistant

## 1. Project Overview

This project is a lightweight, offline-first conversational AI assistant that accepts microphone input, transcribes speech to text, generates a response using a local LLM, converts the response to speech, and plays the audio back to the user.

The MVP is designed for an AI Engineering Internship assignment where speed, clarity, and completeness matter more than advanced features. The system avoids paid APIs, cloud services, databases, authentication, Docker, LangChain, and vector databases.

## 2. Objectives

- Build a real-time audio-in, audio-out AI assistant.
- Use free and preferably offline tools.
- Keep latency low enough for natural conversation.
- Handle slow responses and failures with friendly conversational fallback messages.
- Keep the code modular, readable, and easy for a beginner to run.
- Deliver a clean MVP that satisfies every assignment requirement without extra complexity.

## 3. Functional Requirements

- Capture voice input from the microphone.
- Convert recorded speech to text using offline speech recognition.
- Send the transcribed text to a local LLM.
- Generate a concise conversational response.
- Convert the LLM response to natural speech.
- Play the generated speech through the speaker.
- Show the conversation in a simple Gradio UI.
- Log key events, latency, and errors.
- Provide graceful fallback responses when any step is delayed or fails.

## 4. Non-Functional Requirements

- Free to use.
- Offline-first.
- Easy to install and run on a normal laptop.
- Low-latency pipeline.
- Modular architecture.
- No paid APIs.
- No cloud services.
- No authentication.
- No database.
- No Docker.
- No deployment setup.
- Clear error handling.
- Type hints and production-quality structure.

## 5. Tech Stack With Reasons

| Area | Tool | Reason |
|---|---|---|
| Language | Python | Simple, fast to build, strong AI/audio ecosystem |
| UI | Gradio | Quick local interface for recording, viewing text, and testing |
| Speech-to-Text | Faster-Whisper | Free, offline, faster than standard Whisper on many machines |
| LLM | Ollama | Free local LLM runtime with simple local HTTP API |
| Suggested LLM Model | `llama3.2:1b`, `qwen2.5:1.5b`, or `phi3:mini` | Lightweight enough for normal laptops |
| Text-to-Speech | Piper TTS | Free, offline, fast neural TTS |
| Microphone Input | sounddevice | Lightweight microphone capture |
| Audio File Handling | soundfile | Reliable WAV read/write support |
| Audio Playback | sounddevice | Simple local playback without an extra native SDL dependency |
| Async Runtime | asyncio | Keeps pipeline responsive and supports timeout handling |
| Config | python-dotenv | Simple local configuration without hardcoding machine-specific values |
| Logging | Python logging | Built-in and reliable |

## 6. Folder Structure

```text
offline-voice-assistant/
├── README.md
├── requirements.txt
├── .env.example
├── app.py
├── config.py
├── src/
│   ├── __init__.py
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── recorder.py
│   │   └── player.py
│   ├── stt/
│   │   ├── __init__.py
│   │   └── whisper_service.py
│   ├── llm/
│   │   ├── __init__.py
│   │   └── ollama_service.py
│   ├── tts/
│   │   ├── __init__.py
│   │   └── piper_service.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── conversation_pipeline.py
│   └── utils/
│       ├── __init__.py
│       ├── fallbacks.py
│       └── logger.py
├── models/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
└── logs/
    └── .gitkeep
```

## 7. High-Level Architecture

The assistant follows a simple sequential pipeline:

```text
Microphone
   ↓
Audio Recorder
   ↓
Speech-to-Text
   ↓
Local LLM
   ↓
Text-to-Speech
   ↓
Audio Playback
   ↓
Gradio UI + Logs
```

Each component has one responsibility. This keeps the MVP easy to build, test, and debug.

## 8. Workflow Diagram

```text
User speaks
   ↓
Record audio from microphone
   ↓
Save temporary WAV file
   ↓
Transcribe WAV with Faster-Whisper
   ↓
Validate transcript
   ↓
Send transcript to Ollama
   ↓
Receive assistant text response
   ↓
Generate speech with Piper
   ↓
Play response audio
   ↓
Update Gradio chat history
```

## 9. Component Responsibilities

| Component | Responsibility |
|---|---|
| `app.py` | Starts the Gradio UI and connects user actions to the pipeline |
| `config.py` | Loads local settings from environment variables |
| `recorder.py` | Records microphone audio and saves it as WAV |
| `player.py` | Plays generated audio responses |
| `whisper_service.py` | Loads Faster-Whisper and transcribes audio |
| `ollama_service.py` | Sends prompts to the local Ollama model |
| `piper_service.py` | Calls Piper TTS to generate speech |
| `conversation_pipeline.py` | Orchestrates recording, STT, LLM, TTS, playback, fallbacks, and logging |
| `fallbacks.py` | Provides conversational fallback responses |
| `logger.py` | Configures application logging |

## 10. Fallback Conversation Strategy

The assistant should avoid technical error messages during conversation. If a component is slow or fails, it should respond naturally.

Example fallback messages:

- Slow STT: "I am still catching that. Could you repeat it once more?"
- Empty transcript: "I did not catch enough audio. Please try again."
- Slow LLM: "I am thinking through that. Give me a moment."
- LLM failure: "I am having trouble forming a response right now. Could you ask that another way?"
- TTS failure: "I generated a response, but I could not speak it out loud."
- Playback failure: "The response is ready, but audio playback did not start."

Fallbacks should be short, conversational, and useful.

## 11. Error Handling Strategy

- Wrap each pipeline stage in clear exception handling.
- Use timeouts for STT, LLM, and TTS steps.
- Log errors with context for debugging.
- Return user-friendly fallback text to the UI.
- Avoid crashing the full app when one request fails.
- Validate required local dependencies at startup where practical.
- Keep errors visible in logs but not exposed as raw stack traces in the UI.

## 12. Performance Strategy

- Use a small Faster-Whisper model by default, such as `base` or `small`.
- Use a lightweight Ollama model, such as `llama3.2:1b`, `qwen2.5:1.5b`, or `phi3:mini`.
- Keep prompts short and ask the LLM for concise answers.
- Use WAV files with practical sample rates.
- Load models once at startup instead of per request.
- Use async timeouts around slow stages.
- Keep the UI simple.
- Avoid unnecessary background services.

## 13. Installation Guide

### Prerequisites

- Python 3.10 or newer
- A working microphone and speaker
- Ollama installed locally
- Piper installed locally if offline voice output is required
- At least one Ollama model downloaded
- At least one Piper voice model downloaded

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama

Download Ollama from:

```text
https://ollama.com
```

Then download a lightweight model:

```bash
ollama pull llama3.2:1b
```

Alternative lightweight models:

```bash
ollama pull qwen2.5:1.5b
ollama pull phi3:mini
```

### Install Piper

Piper is included as a Python dependency through `piper-tts`. After installing `requirements.txt`, the project uses:

```text
.venv/bin/piper
```

Piper is optional. If it is not installed, the app still runs as Speech-to-Text -> Ollama -> text response. To enable offline voice output, download a compatible Piper voice model and place it in the local `models/` folder.

Recommended source:

```text
https://github.com/rhasspy/piper/blob/master/VOICES.md
```

Download both files for the same voice:

- The `.onnx` model file.
- The matching `.onnx.json` config file.

Then update `.env`:

```bash
PIPER_EXECUTABLE=.venv/bin/piper
PIPER_VOICE_MODEL=models/en_US-lessac-medium.onnx
PIPER_VOICE_CONFIG=models/en_US-lessac-medium.onnx.json
```

## 14. Running Instructions

Phase 1 does not include application code. After Phase 2 implementation, the expected run command will be:

```bash
python app.py
```

The Gradio app will open locally in the browser.

Before running, copy `.env.example` to `.env` and update local paths:

```bash
cp .env.example .env
```

For longer complete LLM responses, keep these settings at these values or higher:

```bash
OLLAMA_NUM_PREDICT=512
LLM_TIMEOUT_SECONDS=60
```

## 21. Phase 2 Implementation Summary

Phase 2 adds the complete runnable MVP:

- Microphone recording with `sounddevice`.
- Offline transcription with Faster-Whisper.
- Local LLM response generation through Ollama.
- Offline speech synthesis through Piper.
- Audio playback with `sounddevice`.
- Async orchestration with timeouts and graceful fallbacks.
- Local logging.
- Simple Gradio UI for voice and text testing.

## 22. File Guide and Testing Notes

### `app.py`

What it does: Starts the Gradio UI and connects UI actions to the conversation pipeline.

Why it exists: It is the project entry point.

How to test it:

```bash
python app.py
```

### `config.py`

What it does: Loads environment variables and creates runtime folders.

Why it exists: It keeps machine-specific settings out of the code.

How to test it:

```bash
python -c "from config import load_settings; print(load_settings())"
```

### `src/audio/recorder.py`

What it does: Records microphone audio and saves a WAV file.

Why it exists: It isolates microphone capture from the rest of the app.

How to test it: Click `Record and Respond` in the Gradio UI and confirm a new `outputs/input_*.wav` file is created.

### `src/audio/player.py`

What it does: Plays generated WAV responses.

Why it exists: It keeps audio playback separate from TTS generation.

How to test it: Run the full pipeline and confirm the assistant speaks aloud.

### `src/stt/whisper_service.py`

What it does: Loads Faster-Whisper and transcribes recorded audio.

Why it exists: It provides offline speech-to-text.

How to test it: Record audio through the UI and verify the transcript appears in the chat.

### `src/llm/ollama_service.py`

What it does: Sends the user transcript to a local Ollama model.

Why it exists: It provides local LLM reasoning without paid APIs.

How to test it:

```bash
ollama serve
ollama pull llama3.2:1b
```

Then use the text input in the UI.

### `src/tts/piper_service.py`

What it does: Calls Piper to synthesize assistant text into a WAV file.

Why it exists: It provides offline text-to-speech.

How to test it: Confirm `outputs/response_*.wav` is created after a successful response.

### `src/pipeline/conversation_pipeline.py`

What it does: Orchestrates recording, transcription, LLM response, TTS, playback, timing, and fallbacks.

Why it exists: It keeps the app workflow in one testable place.

How to test it: Use either the voice button or text input in the UI.

### `src/utils/fallbacks.py`

What it does: Stores friendly fallback messages.

Why it exists: It prevents raw technical errors from becoming user-facing responses.

How to test it: Stop Ollama or remove the Piper model path temporarily and run a request.

### `src/utils/logger.py`

What it does: Configures console and rotating file logs.

Why it exists: It makes debugging easier without adding external dependencies.

How to test it: Run the app and check `logs/assistant.log`.

## 23. Final Folder Structure

```text
offline-voice-assistant/
├── README.md
├── requirements.txt
├── .env.example
├── app.py
├── config.py
├── src/
│   ├── __init__.py
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── recorder.py
│   │   └── player.py
│   ├── stt/
│   │   ├── __init__.py
│   │   └── whisper_service.py
│   ├── llm/
│   │   ├── __init__.py
│   │   └── ollama_service.py
│   ├── tts/
│   │   ├── __init__.py
│   │   └── piper_service.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── conversation_pipeline.py
│   └── utils/
│       ├── __init__.py
│       ├── fallbacks.py
│       └── logger.py
├── models/
│   └── .gitkeep
├── outputs/
│   └── .gitkeep
└── logs/
    └── .gitkeep
```

## 24. How to Run the Project

1. Create and activate a local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Create local environment config:

```bash
cp .env.example .env
```

4. Install and start Ollama:

```bash
ollama pull llama3.2:1b
ollama serve
```

5. Optional: download a Piper voice model into `models/` to enable spoken responses.

6. Start the app:

```bash
python app.py
```

## 25. How to Test Every Feature

- Audio recording: Click `Record and Respond` and check for `outputs/input_*.wav`.
- Speech-to-text: Confirm your spoken words appear as the user message.
- LLM: Type a message in the text box and confirm an assistant response appears.
- Piper executable: Run `.venv/bin/piper --help`.
- TTS: Confirm `outputs/response_*.wav` is created after a response.
- Playback: Confirm the assistant response is spoken aloud.
- Fallbacks: Stop Ollama or use an invalid Piper model path and confirm the UI shows a friendly fallback.
- Logging: Check `logs/assistant.log`.

## 26. Common Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| No microphone input | Microphone permission or wrong device | Allow microphone access in system settings |
| Ollama request fails | Ollama is not running | Run `ollama serve` |
| Model not found | Ollama model was not pulled | Run `ollama pull llama3.2:1b` |
| Offline voice output unavailable | Piper is not installed | Install Piper from `https://github.com/rhasspy/piper/releases` or continue in text-only mode |
| Piper model not found | Voice model is missing or path is wrong | Download a voice from `https://github.com/rhasspy/piper/blob/master/VOICES.md`, place the `.onnx` and `.onnx.json` files in `models/`, and update `.env` |
| No audio playback | Speaker permission or audio output device issue | Check system output device and volume |
| First transcription is slow | Whisper model loads on first use | Wait for first run; later runs should be faster |
| App imports fail | Dependencies missing | Run `pip install -r requirements.txt` |

## 15. Project Structure

The final project will contain:

- Documentation and setup files.
- A simple Gradio entry point.
- Modular services for audio recording, transcription, LLM response generation, TTS, and playback.
- A central conversation pipeline.
- Local folders for models, generated audio, and logs.

No application code is generated in Phase 1.

## 16. Future Improvements

These are intentionally outside the MVP:

- Voice activity detection.
- Streaming STT.
- Streaming LLM responses.
- Streaming TTS.
- Wake word detection.
- Conversation memory persistence.
- Speaker diarization.
- Better interruption handling.
- Packaged desktop app.
- Advanced UI controls.

## 17. AI Usage Declaration

This project was planned and implemented with assistance from AI tools. AI was used to help design the architecture, documentation, implementation plan, and code structure. All selected technologies are free and intended to run locally without paid APIs or cloud services.

## 18. Deliverables Checklist

### Phase 1

- [x] Project Overview
- [x] Objectives
- [x] Functional Requirements
- [x] Non-functional Requirements
- [x] Tech Stack with reasons
- [x] Folder Structure
- [x] High-Level Architecture
- [x] Workflow Diagram
- [x] Component Responsibilities
- [x] Fallback Conversation Strategy
- [x] Error Handling Strategy
- [x] Performance Strategy
- [x] Installation Guide
- [x] Running Instructions
- [x] Project Structure
- [x] Future Improvements
- [x] AI Usage Declaration
- [x] Deliverables Checklist
- [x] Complete README.md
- [x] requirements.txt
- [x] .env.example

### Phase 2

- [ ] Audio Recording
- [ ] Speech-to-Text
- [ ] Offline LLM
- [ ] Text-to-Speech
- [ ] Audio Playback
- [ ] Conversation Pipeline
- [ ] Graceful Fallback
- [ ] Error Handling
- [ ] Logging
- [ ] Simple Gradio UI

## 19. Implementation Plan

### Phase 1: Planning and Documentation

Status: Complete.

Deliverables:

- `README.md`
- `requirements.txt`
- `.env.example`

No application code is included in Phase 1.

### Phase 2: Complete MVP Implementation

Planned implementation order:

1. Create configuration and logging modules.
2. Implement audio recording with `sounddevice`.
3. Implement playback with `sounddevice`.
4. Implement Faster-Whisper transcription service.
5. Implement Ollama local LLM service.
6. Implement Piper TTS service.
7. Implement fallback response helpers.
8. Implement the conversation pipeline.
9. Implement the Gradio UI.
10. Add final run and testing instructions.

## 20. MVP Acceptance Criteria

The project is complete when:

- The user can speak into the microphone.
- The assistant transcribes the speech.
- The assistant generates a response locally using Ollama.
- The assistant converts the response to speech using Piper.
- The assistant plays the response audio.
- The Gradio UI shows the conversation.
- Failures produce conversational fallback messages.
- The project runs without paid APIs, cloud services, Docker, databases, or authentication.
