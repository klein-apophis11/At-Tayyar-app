import os
import threading
from pathlib import Path

import pygame

# Initialize the mixer engine explicitly, but fail gracefully if audio isn't available.
try:
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    MIXER_READY = True
except Exception:
    MIXER_READY = False

# Use absolute paths dynamically so it works anywhere.
BASE_DIR = Path(__file__).resolve().parent
CANDIDATE_DIRS = [BASE_DIR / "audio", BASE_DIR.parent / "audio"]


def resolve_audio_path():
    """Return the first valid athan audio file found in the common project layouts."""
    for directory in CANDIDATE_DIRS:
        candidate = directory / "6f509ec934a4.mp3"
        if candidate.exists():
            return str(candidate)

    # Fallback to the standard project-local path for clearer error reporting.
    return str(BASE_DIR / "audio" / "6f509ec934a4.mp3")


AUDIO_PATH = resolve_audio_path()


def _run_audio():
    """Internal helper function to load and play the file."""
    if not MIXER_READY:
        print("❌ Audio unavailable: pygame mixer could not initialize.")
        return

    try:
        if os.path.exists(AUDIO_PATH):
            pygame.mixer.music.load(AUDIO_PATH)
            pygame.mixer.music.set_volume(0.75)
            pygame.mixer.music.play()
            print(f"🔊 Athan started playing successfully from: {AUDIO_PATH}")
        else:
            print(f"❌ ERROR: Audio file missing. Checked: {AUDIO_PATH}")
    except Exception as e:
        print(f"❌ Failed to play audio asset: {e}")


def play_athan():
    """Starts the Athan on a separate thread so the GUI doesn't freeze."""
    if not MIXER_READY:
        print("❌ Audio not available because the mixer could not initialize.")
        return

    # If audio is already playing, don't start a duplicate stream.
    if not pygame.mixer.music.get_busy():
        audio_thread = threading.Thread(target=_run_audio, daemon=True)
        audio_thread.start()

def stop_athan():
    """Stops the audio immediately if it is currently playing."""
    if MIXER_READY and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("🛑 Athan stopped by user.")
