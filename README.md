# 🎙️ Real-Time Voice Agent using LiveKit

This project implements a real-time conversational voice agent using:

- **LiveKit** for audio streaming  
- **OpenAI Whisper (local)** for Speech-to-Text  
- **pyttsx3 (local)** for Text-to-Speech  
- Custom energy-based **VAD (Voice Activity Detection)** for speech detection  

The agent listens to a user in a LiveKit room, transcribes speech, generates a response, and speaks back in real time.

---

## Requirements

### Python Version

- **Python 3.10 – 3.12** recommended

### Python Dependencies

Install using:

```bash
pip install -r requirements.txt
```

### Required libraries

```bash
livekit
sounddevice
numpy
scipy
pyttsx3
openai-whisper
python-dotenv
soundfile
librosa
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create virtual environment

```bash
python -m venv venv
```

#### Activate

- Windows:

```bash
venv\Scripts\activate
```

- Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env file in the root directory

```bash
LIVEKIT_URL=wss://your-livekit-server-url
LIVEKIT_TOKEN=your-generated-token
```

## Required Environment Variables

| Variable        | Description                                 |
| --------------- | ------------------------------------------- |
| `LIVEKIT_URL`   | WebSocket URL of your LiveKit server        |
| `LIVEKIT_TOKEN` | Generated access token for joining the room |

## How to Run

### Start the agent

```bash
python main.py
```

### Then

1. Start the LiveKit server (if self-hosted)

2. Open your frontend client or LiveKit test room

3. Join the room

4. Speak into microphone

### The agent will

- Detect speech

- Transcribe using Whisper

- Respond using TTS

- Stream response back via LiveKit

## Architecture Overview

```bash
User Mic
   ↓
LiveKit Audio Track
   ↓
Energy-Based VAD
   ↓
Audio Buffer
   ↓
Whisper (Speech-to-Text)
   ↓
Response Generation
   ↓
pyttsx3 (Text-to-Speech)
   ↓
LiveKit Audio Track (Agent)
```

## SDK Used

- LiveKit Python SDK

- Whisper (local model - base)

- pyttsx3 (SAPI on Windows)

- Librosa (resampling)

- NumPy

## External Services Used

| Service         | Usage                     |
| --------------- | ------------------------- |
| LiveKit         | Real-time audio streaming |
| Whisper (local) | Speech recognition        |
| pyttsx3 (local) | Speech synthesis          |

No external paid APIs are used. Everything runs locally.

## VAD (Voice Activity Detection)

The system uses a custom energy-based VAD:

- Detects speech using amplitude threshold

- Detects silence to trigger transcription

- Prevents self-trigger during agent speech

## Known Limitations

- Whisper runs on CPU → Higher latency

- Energy-based VAD may misbehave in noisy environments

- pyttsx3 may block if not properly threaded

- No streaming transcription (batch-based processing)

- Agent must typically join before user for consistent track subscription

- No LLM integration (currently echo-style response)

## Possible Improvements

- Replace energy VAD with Silero VAD

- Use streaming STT

- Replace pyttsx3 with Edge-TTS

- Add LLM (GPT / local model)

- Add interrupt handling (barge-in)

- GPU acceleration for Whisper

## Tested On

- Windows 10

- Python 3.11

- CPU-only environment

## Project Structure

```bash
├── main.py
├── livekit_client.py
├── stt.py
├── tts.py
├── vad.py
├── state_manager.py
├── .env
├── requirements.txt
└── README.md
```

## Current Status

- Real-time two-way audio
- Speech detection
- Transcription
- TTS response
- Stable multi-response handling
