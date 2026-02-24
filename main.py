import sounddevice as sd
import numpy as np
import queue
import whisper
import pyttsx3
import os
import time
import tempfile
import threading
from scipy.io.wavfile import write

# ==============================
# CONFIG
# ==============================
SAMPLE_RATE = 16000
SILENCE_TIMEOUT = 20
ENERGY_THRESHOLD = 0.01
SILENCE_DURATION = 0.8
MIN_AUDIO_LENGTH = 0.5

# ==============================
# LOAD MODEL
# ==============================
model = whisper.load_model("base")  # use "tiny" for faster

# ==============================
# STATE
# ==============================
audio_queue = queue.Queue()
recording = []

last_speech_time = time.time()
last_voice_detected = time.time()

is_listening = False
is_speaking = False

# ==============================
# AUDIO INPUT CALLBACK
# ==============================
def audio_callback(indata, frames, time_info, status):
    audio_queue.put(indata.copy())


# ==============================
# SIMPLE VAD (ENERGY BASED)
# ==============================
def is_speech(audio_chunk):
    return np.mean(np.abs(audio_chunk)) > ENERGY_THRESHOLD


# ==============================
# SAVE AUDIO
# ==============================
def save_wav(audio_data):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp.name, SAMPLE_RATE, audio_data)
    return temp.name


# ==============================
# STT
# ==============================
def transcribe(audio_np):
    path = save_wav(audio_np)

    try:
        result = model.transcribe(path)
        return result["text"].strip()
    finally:
        try:
            os.remove(path)
        except:
            pass


# ==============================
# TTS (THREAD SAFE)
# ==============================
def speak(text):
    global is_speaking

    if is_speaking:
        return  # prevent overlap

    def run():
        global is_speaking
        is_speaking = True

        print(f"🤖 Agent: {text}")

        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 170)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print("TTS error:", e)

        finally:
            is_speaking = False
            print("Speak Now.....")

    threading.Thread(target=run, daemon=True).start()


# ==============================
# MAIN LOOP
# ==============================
print("🎙️ Agent is listening... Speak now!")

with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback):

    while True:
        audio_chunk = audio_queue.get()

        if audio_chunk is None:
            continue

        speech = is_speech(audio_chunk)
        current_time = time.time()

        # ==========================
        # USER SPEAKING
        # ==========================
        if speech:
            last_speech_time = current_time
            last_voice_detected = current_time

            # 🔥 INTERRUPT (basic safe version)
            if is_speaking:
                print("⚠️ Interrupt detected — stopping response")
                is_speaking = False  # soft stop (best possible with pyttsx3)

            is_listening = True
            recording.append(audio_chunk)

        # ==========================
        # USER STOPPED SPEAKING
        # ==========================
        else:
            if is_listening and (current_time - last_voice_detected > SILENCE_DURATION):

                duration = sum(len(chunk) for chunk in recording) / SAMPLE_RATE

                if duration < MIN_AUDIO_LENGTH:
                    recording = []
                    is_listening = False
                    continue

                print("🧠 Processing speech...")

                full_audio = np.concatenate(recording, axis=0)

                text = transcribe(full_audio)
                print(f"👤 You said: {text}")

                if text:
                    speak(f"You said: {text}")

                # Reset
                recording = []
                is_listening = False

        # ==========================
        # SILENCE HANDLING
        # ==========================
        if current_time - last_speech_time > SILENCE_TIMEOUT:
            if not is_speaking:
                speak("Are you still there?")
                last_speech_time = current_time