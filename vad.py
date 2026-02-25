import numpy as np

ENERGY_VAD_THRESHOLD = 0.01  # adjust if needed

def is_speech(audio_bytes):
    """
    Simple energy-based VAD.
    Returns True if speech detected.
    """

    audio_np = np.frombuffer(audio_bytes, np.int16).astype(np.float32) / 32768.0
    energy = np.mean(np.abs(audio_np))

    return energy > ENERGY_VAD_THRESHOLD