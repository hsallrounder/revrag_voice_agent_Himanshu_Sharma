# 🎙️ Real-Time Voice Agent (LiveKit)

## Overview

This project implements a real-time voice agent that joins a LiveKit room and interacts via audio only.

The agent listens to user speech, converts it to text, generates a response, and replies using synthesized speech.

---

## 🚀 Features

* Real-time audio interaction
* Speech-to-Text using Whisper
* Text-to-Speech using gTTS
* No-overlap speaking logic (interrupt handling)
* Silence detection (20s timeout)

---

## 🧠 Voice AI Pipeline

Speech → Text → Response → Speech

---

## ⚙️ Setup

```bash
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python main.py
```

---

## 🧩 Tech Stack

* LiveKit (conceptual integration)
* Whisper (STT)
* gTTS (TTS)
* WebRTC VAD

---

## 🚫 No Overlap Handling

* Uses VAD to detect speech
* If user starts speaking:

  * Stops current response immediately
* Responds only after user finishes speaking

---

## ⏱️ Silence Handling

* If no speech for 20 seconds:

  * Plays "Are you still there?"
* Triggered once per silence window

---

## ⚠️ Limitations

* Mock LiveKit client (can be replaced with real SDK)
* Non-streaming STT/TTS
* Whisper latency

---

## 📌 Future Improvements

* LiveKit full integration
* Streaming STT (Deepgram)
* Streaming TTS
