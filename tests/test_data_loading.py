from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import os

from data_library import JAFARI_STEPS, TASBIH_PHASES


def test_steps_loaded():
    assert isinstance(JAFARI_STEPS, dict)
    assert len(JAFARI_STEPS) > 0


def test_tasbih_phases_loaded():
    assert isinstance(TASBIH_PHASES, list)
    assert len(TASBIH_PHASES) > 0


def test_athan_audio_file_exists():
    import audio

    assert os.path.exists(audio.AUDIO_PATH), f"Expected audio file at {audio.AUDIO_PATH}"
