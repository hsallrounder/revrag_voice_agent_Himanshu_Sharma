def text_to_audio_bytes(text):
    import pyttsx3
    import tempfile
    import soundfile as sf
    import numpy as np
    import librosa
    import os

    engine = pyttsx3.init()  # 🔥 create fresh engine every call

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        temp_path = f.name

    engine.save_to_file(text, temp_path)
    engine.runAndWait()
    engine.stop()
    del engine  # 🔥 force cleanup

    audio, sr = sf.read(temp_path)
    os.remove(temp_path)

    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    if sr != 16000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)

    audio = audio / np.max(np.abs(audio))
    audio_int16 = (audio * 32767).astype(np.int16)

    return audio_int16.tobytes()