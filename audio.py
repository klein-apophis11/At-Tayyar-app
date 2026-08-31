import os
import threading
import pygame

# Initialize the mixer engine explicitly, but fail gracefully if audio isn't available.
try:
    pygame.mixer.init()
    MIXER_READY = True
except Exception:
    MIXER_READY = False

# Use absolute paths dynamically so it works anywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = os.path.join(BASE_DIR, "audio", "6f509ec934a4.mp3")

def _run_audio():
    """Internal helper function to load and play the file."""
    if not MIXER_READY:
        print("❌ Audio unavailable: pygame mixer could not initialize.")
        return

    try:
        if os.path.exists(AUDIO_PATH):
            pygame.mixer.music.load(AUDIO_PATH)
            pygame.mixer.music.play()
            print("🔊 Athan started playing successfully...")
        else:
            print("❌ ERROR: Audio file missing.")
    except Exception as e:
        print(f"❌ Failed to play audio asset: {e}")

def play_athan():
    """Starts the Athan on a separate thread so the GUI doesn't freeze."""
    if not MIXER_READY:
        return

    # If audio is already playing, don't start a duplicate stream
    if not pygame.mixer.music.get_busy():
        audio_thread = threading.Thread(target=_run_audio, daemon=True)
        audio_thread.start()

def stop_athan():
    """Stops the audio immediately if it is currently playing."""
    if MIXER_READY and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("🛑 Athan stopped by user.")
