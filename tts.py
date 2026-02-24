from gtts import gTTS
import tempfile

def synthesize_speech(text):
    tts = gTTS(text=text)
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(file.name)
    return file.name