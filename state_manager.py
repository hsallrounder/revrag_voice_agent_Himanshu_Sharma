class StateManager:
    def __init__(self):
        self.state = "IDLE"
        self.audio_buffer = b""

    def set_listening(self):
        self.state = "LISTENING"

    def set_speaking(self):
        self.state = "SPEAKING"

    def set_idle(self):
        self.state = "IDLE"

    def is_listening(self):
        return self.state == "LISTENING"

    def is_speaking(self):
        return self.state == "SPEAKING"

    def add_audio(self, chunk):
        self.audio_buffer += chunk

    def get_audio(self):
        return self.audio_buffer

    def clear_audio(self):
        self.audio_buffer = b""