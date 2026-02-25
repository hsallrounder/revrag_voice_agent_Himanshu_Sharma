import asyncio
import os
from livekit import rtc
from livekit.rtc import AudioStream
from dotenv import load_dotenv

load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_TOKEN = os.getenv("LIVEKIT_TOKEN")


class LiveKitClient:
    def __init__(self):
        self.room = None
        self.audio_callback = None
        self.audio_source = None
        self.audio_track = None

    async def connect(self):
        # ✅ Create room properly
        self.room = rtc.Room()

        # ✅ Connect
        await self.room.connect(LIVEKIT_URL, LIVEKIT_TOKEN)
        print("✅ Connected to LiveKit")

        # ✅ Create audio source (for speaking)
        self.audio_source = rtc.AudioSource(16000, 1)
        self.audio_track = rtc.LocalAudioTrack.create_audio_track(
            "agent-voice",
            self.audio_source
        )

        await self.room.local_participant.publish_track(self.audio_track)

        # ✅ Subscribe to remote audio
        @self.room.on("track_subscribed")
        def on_track_subscribed(track, publication, participant):
            print(f"🎧 Subscribed to audio from {participant.identity}")
            print("Track kind:", track.kind)

            if track.kind == rtc.TrackKind.KIND_AUDIO:
                print("Starting audio stream...")
                asyncio.create_task(self.handle_audio(track))

    def on_audio_received(self, callback):
        self.audio_callback = callback

    async def handle_audio(self, track):
        print("Audio handler started")

        stream = AudioStream(track)

        async for event in stream:
            # print("Frame received")

            audio_frame = event.frame  # ✅ extract actual frame

            if self.audio_callback:
                audio_bytes = bytes(audio_frame.data)
                self.audio_callback(audio_bytes)

    async def publish_audio(self, audio_bytes):
        # 🔥 Recreate audio source each time (CRITICAL FIX)
        self.audio_source = rtc.AudioSource(16000, 1)
        self.audio_track = rtc.LocalAudioTrack.create_audio_track(
            "agent-voice",
            self.audio_source
        )

        await self.room.local_participant.publish_track(self.audio_track)

        print("Publishing bytes:", len(audio_bytes))

        frame_samples = 320  # 20ms @ 16kHz
        bytes_per_sample = 2
        frame_size = frame_samples * bytes_per_sample

        for i in range(0, len(audio_bytes), frame_size):
            chunk = audio_bytes[i:i + frame_size]

            if len(chunk) < frame_size:
                chunk += b"\x00" * (frame_size - len(chunk))

            frame = rtc.AudioFrame(
                data=chunk,
                sample_rate=16000,
                num_channels=1,
                samples_per_channel=frame_samples,
            )

            await self.audio_source.capture_frame(frame)
            await asyncio.sleep(0.02)

    async def run(self):
        await asyncio.Future()