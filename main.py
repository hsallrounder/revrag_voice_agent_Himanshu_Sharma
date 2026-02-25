import asyncio
import numpy as np
from livekit_client import LiveKitClient
from state_manager import StateManager
from stt import transcribe_audio
from vad import is_speech
import soundfile as sf
from tts import text_to_audio_bytes

SAMPLE_RATE = 16000
is_processing = False
silence_frames = 0
is_listening = False

state = StateManager()

def is_silence(audio_bytes, threshold=500):
    audio_np = np.frombuffer(audio_bytes, np.int16)
    return np.abs(audio_np).mean() < threshold


def audio_handler(audio_bytes, client):
    global silence_frames, is_listening

    if state.is_speaking():
        return

    audio_np = np.frombuffer(audio_bytes, np.int16).astype(np.float32) / 32768.0
    energy = np.mean(np.abs(audio_np))

    SPEECH_THRESHOLD = 0.01  # adjust if needed

    if energy > SPEECH_THRESHOLD:
        silence_frames = 0
        is_listening = True
        state.add_audio(audio_bytes)
    else:
        silence_frames += 1

        # if user stopped speaking
        if is_listening and silence_frames > 10:
            is_listening = False
            silence_frames = 0
            asyncio.create_task(process_audio(client))

async def process_audio(client):
    try:
        state.set_speaking()

        audio_data = state.get_audio()
        state.clear_audio()

        if len(audio_data) < 16000:
            return

        loop = asyncio.get_event_loop()

        # 🔥 Run Whisper in background thread
        text = await loop.run_in_executor(
            None,
            transcribe_audio,
            audio_data
        )

        if not text:
            return

        print("\n🧠 Transcribing...")
        print("👤 User:", text)

        response = f"You said: {text}"
        print("🤖 Agent:", response)

        # 🔥 Run TTS in background thread
        tts_audio = await loop.run_in_executor(
            None,
            text_to_audio_bytes,
            response
        )

        print("Publishing bytes:", len(tts_audio))

        await client.publish_audio(tts_audio)

    except Exception as e:
        print("Error:", e)

    finally:
        await asyncio.sleep(0.5)
        state.set_idle()


async def main():
    client = LiveKitClient()   # ← create inside event loop
    client.on_audio_received(lambda audio: audio_handler(audio, client))
    await client.connect()
    await client.run()


if __name__ == "__main__":
    asyncio.run(main())