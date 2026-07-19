<div align="center">

# 🤖 F.R.I.D.A.Y.
### *Fully Responsive Intelligent Digital Assistant for You*

<!-- 🖼️ INSERT HERO BANNER IMAGE HERE (1280x640 recommended) -->
<!-- ![FRIDAY Hero Banner](./assets/hero-banner.png) -->

**A real-time, offline-first, voice-native AI assistant — inspired by Tony Stark's J.A.R.V.I.S. & F.R.I..A.Y.**

<!-- Animated typing banner placeholder — generate at https://readme-typing-svg.demolab.com -->
<!-- ![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=00F5FF&center=true&vCenter=true&width=600&lines=Listening...;Thinking...;Speaking...;Your+Personal+AI+is+Online.) -->

<p>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Ollama-Qwen3--8B-000000?style=for-the-badge&logo=ollama&logoColor=white" />
  <img src="https://img.shields.io/badge/Speech-Faster--Whisper-FF6F00?style=for-the-badge" />
  <img src="https://img.shields.io/badge/TTS-Piper-8A2BE2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/UI-Gradio-F97316?style=for-the-badge&logo=gradio&logoColor=white" />
</p>

<p>
  <img src="https://img.shields.io/github/stars/yourusername/friday?style=flat-square&color=yellow" />
  <img src="https://img.shields.io/github/forks/yourusername/friday?style=flat-square&color=blue" />
  <img src="https://img.shields.io/github/last-commit/yourusername/friday?style=flat-square" />
  <img src="https://img.shields.io/github/license/yourusername/friday?style=flat-square" />
  <img src="https://img.shields.io/badge/status-active--development-brightgreen?style=flat-square" />
</p>

<p>
  <a href="#-demo">Demo</a> •
  <a href="#-key-highlights">Highlights</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-roadmap">Roadmap</a> •
  <a href="#-contributing">Contributing</a>
</p>

</div>

---

## 📖 Overview

**F.R.I.D.A.Y.** is a fully offline, real-time conversational AI assistant that listens, thinks, and speaks — all running locally on your machine. No cloud APIs, no data leaving your device, no latency from network round-trips.

Built from the ground up as a personal engineering challenge, F.R.I.D.A.Y. combines **offline speech recognition**, **local LLM reasoning**, and **offline speech synthesis** into a single low-latency pipeline — wrapped in a clean, interactive web interface.

> *"The goal isn't just a chatbot with a microphone. It's a foundation for a true personal assistant — one that can eventually see, remember, act, and automate."*

### ✨ Why This Project Is Unique

| | |
|---|---|
| 🔒 **100% Offline** | Every component — STT, LLM, TTS — runs locally. Zero API keys, zero cloud dependency, zero data leakage. |
| ⚡ **Low Latency Pipeline** | Engineered audio-to-audio pipeline optimized for near real-time conversation. |
| 🧩 **Modular by Design** | Each component (ASR, LLM, TTS, UI) is swappable — upgrade any piece without rewriting the system. |
| 🛠 **Built for Extension** | Architected from day one to support tool calling, memory, and multi-agent workflows. |
| 🎯 **Real Engineering, Not a Wrapper** | This isn't a thin wrapper around an API — it's a full-stack voice AI system built piece by piece. |

---

## 🚀 Key Highlights

- 🎤 Real-time microphone capture with streaming audio input
- 🧠 Local reasoning powered by **Qwen3:8B** via **Ollama**
- 🗣️ Natural offline text-to-speech using **Piper**
- 💬 Context-aware multi-turn conversations with persistent history
- 🖥️ Clean, responsive **Gradio** web interface (voice + text)
- 🔌 Architecture designed for future tool calling & automation
- 🌐 Fully self-hosted — runs entirely on your own hardware

---

## 🎬 Demo

<!-- 🖼️ INSERT DEMO GIF HERE -->
<!-- ![FRIDAY Demo](./assets/demo.gif) -->

<div align="center">
<i>🎥 Full demo video: <a href="#">Watch on YouTube</a> (placeholder link)</i>
</div>

<br>

<details>
<summary>📸 <b>Click to view Screenshots</b></summary>
<br>

<!-- 🖼️ INSERT SCREENSHOT: Gradio Home Interface -->
<!-- ![Home Interface](./assets/screenshot-home.png) -->

<!-- 🖼️ INSERT SCREENSHOT: Live Voice Conversation -->
<!-- ![Voice Conversation](./assets/screenshot-conversation.png) -->

<!-- 🖼️ INSERT SCREENSHOT: Text Chat Mode -->
<!-- ![Text Chat](./assets/screenshot-textchat.png) -->

</details>

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A[🎤 User Voice Input] --> B[Audio Capture Module]
    B --> C[Faster-Whisper<br/>Speech-to-Text]
    C --> D[Text Query]
    D --> E[Ollama Runtime<br/>Qwen3:8B]
    E --> F[Conversation Memory<br/>Context Manager]
    F --> E
    E --> G[Generated Text Response]
    G --> H[Piper TTS Engine]
    H --> I[🔊 Audio Output]
    D --> J[Gradio Web UI]
    G --> J
    I --> J

    style A fill:#00F5FF,stroke:#0088aa,color:#000
    style I fill:#00F5FF,stroke:#0088aa,color:#000
    style E fill:#8A2BE2,stroke:#5c1a99,color:#fff
    style J fill:#F97316,stroke:#b45309,color:#fff
```

### 🔄 AI Pipeline Flow

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant M as 🎙️ Microphone
    participant W as Faster-Whisper (ASR)
    participant L as Ollama (Qwen3:8B)
    participant P as Piper (TTS)
    participant S as 🔊 Speaker

    U->>M: Speaks
    M->>W: Raw audio stream
    W->>L: Transcribed text
    L->>L: Reasoning + context lookup
    L->>P: Generated response text
    P->>S: Synthesized speech
    S->>U: Audio response
    Note over U,S: End-to-end target latency: low-latency, near real-time
```

---

## 🧩 Features Grid

<table>
<tr>
<td width="33%" valign="top">

### 🎤 Voice Interaction
- Real-time mic input
- Offline ASR (Faster-Whisper)
- Natural conversation flow
- Low-latency audio pipeline

</td>
<td width="33%" valign="top">

### 🧠 AI Intelligence
- Local inference via Ollama
- Powered by Qwen3:8B
- Persistent conversation history
- Context-aware responses

</td>
<td width="33%" valign="top">

### 🔊 Voice Output
- Offline TTS via Piper
- Natural-sounding synthesis
- Configurable voice profiles
- Low-latency generation

</td>
</tr>
</table>

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| 🧠 **AI / Reasoning** | [Ollama](https://ollama.com) + **Qwen3:8B** | Local LLM inference & reasoning engine |
| 🎤 **Speech-to-Text** | [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) | Offline, high-accuracy speech recognition |
| 🔊 **Text-to-Speech** | [Piper](https://github.com/rhasspy/piper) | Fast, natural offline voice synthesis |
| 💻 **Frontend** | [Gradio](https://gradio.app) | Interactive web UI for voice & text |
| 🐍 **Backend** | Python 3.11+ | Core orchestration logic |

### 🔮 Planned Additions

| Technology | Purpose |
|---|---|
| **MCP (Model Context Protocol)** | Standardized tool calling |
| **Gemini** | Multi-model reasoning fallback |
| **LiveKit** | Real-time audio/video streaming infrastructure |
| **FastMCP** | Lightweight MCP server framework |
| **Vector Databases** | Long-term memory & RAG storage |
| **LangChain / LlamaIndex** | RAG orchestration & agent workflows |

---

## 📁 Folder Structure

```
friday/
├── assets/                  # Images, GIFs, diagrams for docs
├── src/
│   ├── audio/
│   │   ├── capture.py        # Microphone input handling
│   │   └── playback.py       # Audio output handling
│   ├── stt/
│   │   └── whisper_engine.py # Faster-Whisper wrapper
│   ├── llm/
│   │   ├── ollama_client.py  # Ollama inference interface
│   │   └── memory.py         # Conversation history/context
│   ├── tts/
│   │   └── piper_engine.py   # Piper TTS wrapper
│   ├── ui/
│   │   └── gradio_app.py     # Gradio web interface
│   └── config.py             # Central configuration
├── tests/                    # Unit & integration tests
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- 🐍 Python 3.11+
- 🖥️ [Ollama](https://ollama.com) installed and running
- 🎧 A working microphone and speaker

### Steps

```bash
# 1️⃣ Clone the repository
git clone https://github.com/yourusername/friday.git
cd friday

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Pull the LLM model via Ollama
ollama pull qwen3:8b

# 5️⃣ Download Piper voice model
# (see /assets/voices or Piper docs for available voices)

# 6️⃣ Run the application
python src/ui/gradio_app.py
```

<details>
<summary>🐳 <b>Docker Setup (optional)</b></summary>

```bash
docker build -t friday-assistant .
docker run -p 7860:7860 friday-assistant
```

</details>

---

## ▶️ Usage

Once running, open your browser at:

```
http://localhost:7860
```

- 🎤 Click the **microphone icon** to speak naturally
- ⌨️ Or type your query in the **text input box**
- 🔊 F.R.I.D.A.Y. will respond with synthesized speech + text
- 🕓 Conversation history is maintained automatically for context

---

## 🔧 Configuration

All configuration lives in `src/config.py` / `.env`:

```env
# LLM Settings
OLLAMA_MODEL=qwen3:8b
OLLAMA_HOST=http://localhost:11434

# Speech-to-Text
WHISPER_MODEL_SIZE=base
WHISPER_DEVICE=cpu   # or cuda

# Text-to-Speech
PIPER_VOICE=en_US-amy-medium

# UI
GRADIO_SERVER_PORT=7860
```

---

## 💬 Example Conversations

<details>
<summary>Click to expand example interaction</summary>

```
👤 User: Hey FRIDAY, what's the weather like for coding today?
🤖 FRIDAY: I don't have live weather access yet, but I can already tell
           your coding forecast: 100% chance of debugging! Web search
           integration is coming in a future update.

👤 User: Remind me what we discussed earlier about the architecture.
🤖 FRIDAY: We talked about your audio pipeline — mic input feeding into
           Faster-Whisper for transcription, then Qwen3:8B for reasoning,
           and Piper for the voice response.
```

</details>

---

## 📊 Benchmarks & Performance

> ⚠️ *Placeholder — populate with real measurements on your target hardware.*

| Metric | Value |
|---|---|
| 🎤 ASR Latency (avg) | `_____ ms` |
| 🧠 LLM Response Time (avg) | `_____ ms` |
| 🔊 TTS Generation Time (avg) | `_____ ms` |
| ⚡ End-to-End Latency | `_____ ms` |
| 💾 RAM Usage (idle) | `_____ GB` |
| 💾 RAM Usage (active inference) | `_____ GB` |
| 🖥️ Tested On | `CPU / GPU model here` |

---

## 🗺 Future Roadmap

- [ ] 🧠 Long-term memory system
- [ ] 🌐 Web search integration
- [ ] 🛠 Tool calling / function execution
- [ ] 📅 Calendar integration
- [ ] 📧 Email assistant capabilities
- [ ] 💬 WhatsApp integration
- [ ] 👁️ Vision capabilities (image/screen understanding)
- [ ] 🏠 Smart home automation
- [ ] 📚 RAG-based knowledge retrieval
- [ ] 🤝 Multi-agent workflows

```mermaid
gantt
    title F.R.I.D.A.Y. Roadmap
    dateFormat  YYYY-MM-DD
    section Core
    Voice Pipeline (Done)      :done, 2024-01-01, 2024-03-01
    Memory System              :active, 2024-03-01, 60d
    Tool Calling                :2024-05-01, 45d
    section Expansion
    Web Search                  :2024-06-15, 30d
    Vision Capabilities         :2024-07-15, 60d
    Smart Home Automation       :2024-09-15, 45d
    Multi-Agent Workflows       :2024-11-01, 60d
```

---

## 🧗 Challenges Faced

- ⚡ **Latency optimization** — Chaining three real-time systems (ASR → LLM → TTS) without introducing noticeable lag required careful tuning of buffering and streaming.
- 🎙️ **Audio pipeline stability** — Handling microphone edge cases (background noise, silence detection, interruptions) reliably across platforms.
- 🧠 **Context management** — Balancing conversation history length against local LLM context window limits.
- 🔧 **Offline-first constraints** — Every capability had to work without internet access, which ruled out many common cloud-based shortcuts.

## 📚 What I Learned

- Building a real-time, multi-stage AI pipeline end-to-end from raw audio to synthesized speech
- Practical tradeoffs between local model size, latency, and response quality
- Designing modular architecture that anticipates future features (memory, tools, agents)
- Deep hands-on experience with offline ASR/TTS systems and local LLM orchestration

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 🚀 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔁 Open a Pull Request

Please check the [issues page](../../issues) for open tasks before starting.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 📸 Screenshots

<img width="1470" height="956" alt="image" src="https://github.com/user-attachments/assets/57ba6a02-55a6-41e4-bf9f-4ecd325cb970" />


---
## 👤 Author

<div align="center">

**R Sanjay**

<!-- 🖼️ INSERT PROFILE/AVATAR IMAGE HERE -->
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sanjay7978)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/r-sanjay-561805374/)

</div>

---

## ⭐ Star the Repository

<div align="center">

If you found this project interesting or useful, please consider giving it a ⭐ —
it genuinely helps and keeps the motivation going for building out the full roadmap.


**Made with ❤️, ☕, and a lot of debugging by [R Sanjay]**

</div>
