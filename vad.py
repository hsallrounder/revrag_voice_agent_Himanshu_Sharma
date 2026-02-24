import numpy as np

def is_speech(audio_chunk, threshold=0.01):
    energy = np.mean(np.abs(audio_chunk))
    return energy > threshold