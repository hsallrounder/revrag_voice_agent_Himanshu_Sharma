import whisper
import numpy as np
import librosa

model = whisper.load_model("base")

def transcribe_audio(audio_bytes):
    audio_np = np.frombuffer(audio_bytes, np.int16).astype(np.float32) / 32768.0
    
    # Resample 48kHz → 16kHz
    audio_np = librosa.resample(audio_np, orig_sr=48000, target_sr=16000)

    result = model.transcribe(audio_np)
    return result["text"].strip()