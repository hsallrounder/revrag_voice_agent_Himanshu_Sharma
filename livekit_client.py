import asyncio

class LiveKitClient:
    def __init__(self):
        self.audio_callback = None

    async def connect(self):
        print("Connected to LiveKit (mock)")

    def on_audio_received(self, callback):
        self.audio_callback = callback

    async def publish_audio(self, audio_file):
        print(f"Playing audio: {audio_file}")

    async def run(self):
        # Mock loop (replace with real LiveKit track handling)
        while True:
            await asyncio.sleep(1)