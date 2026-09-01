# At-Tayyar (الطَّيَّار): Offline Seated Prayer Guide 📿♿

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform: Windows | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)](https://github.com/klein-apophis11/At-Tayyar-app)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-yellow)](README.md)

At-Tayyar is a private, offline desktop app designed to support Muslims who pray from a seated position. It provides a simple, guided prayer experience with clear instructions, Jafari prayer structure, and tasbih tracking in a calm, privacy-first interface.

This project was developed through repeated personal use and iterative improvement. The goal was not to build a broad commercial product, but to create a practical and respectful tool for daily prayer support, accessibility, and focused worship.

---

## About this project

The app is built for Windows 10 and is intended to run locally without any internet dependency, login requirement, or microphone/camera access. It is designed to keep the experience simple, secure, and easy to use during routine prayer practice.

It includes:

- guided step-by-step prayer flow
- support for seated worship and practical prayer adjustments
- local tasbih tracking
- clear visual progress counters
- keyboard-based controls for a private, low-distraction experience

### Available Versions

**Standard GUI Version** (`jafari_app.py`)
- Full-screen interface with prayer flow guidance
- Manual keyboard controls
- Best for: Interactive prayer practice

**System Tray Version** (`jafari_app_tray.py`)
- Runs minimized in system tray (Windows 10+)
- Automatic adhan playback at prayer times
- Right-click tray menu for quick access
- Best for: Hands-free automatic prayer alerts

---

## Key features

- Prayer flow support for Fajr, Dhuhr, Asr, Maghrib, and Isha
- Jafari-aligned multi-rakah layouts for common prayer structures
- Seated prayer guidance designed for comfort and practical use
- Tasbih tracking for the Tasbih of Lady Fatima Zahra (sa)
- Bright, high-contrast rakah indicator for readability during prayer
- Fully offline operation with no tracking or external services

---

## Controls

The interface is intentionally lightweight and manual for privacy and simplicity:

- Spacebar: move to the next step
- Backspace: go back to the previous step
- Escape: cancel the current flow

This keeps the app focused on the prayer experience without requiring voice control, camera input, or a database.

---

## Quick start

### Installation Options

#### Windows (Recommended for Non-Developers)

**Option 1: Standalone Executable** (No Python required)
- Download `At-Tayyar.exe` from [Releases](https://github.com/klein-apophis11/At-Tayyar-app/releases)
- Run the .exe directly
- No installation needed

**Option 2: System Tray Version** (Runs in background)
- Download `At-Tayyar-Tray.exe` from Releases
- App minimizes to system tray
- Automatically plays adhan at prayer times
- Right-click tray icon for menu

**Option 3: From Source**
```bash
git clone https://github.com/klein-apophis11/At-Tayyar-app.git
cd At-Tayyar-app
pip install -r requirements.txt
python jafari_app.py
```

#### Linux / macOS

```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-tk python3-pip libsdl2-mixer-2.0-0

# Fedora
sudo dnf install python3 python3-tkinter python3-pip SDL2_mixer

# Arch
sudo pacman -S python tk python-pip sdl2_mixer

# Then clone and run
git clone https://github.com/klein-apophis11/At-Tayyar-app.git
cd At-Tayyar-app
pip3 install -r requirements.txt
python3 jafari_app.py
```

For detailed build and deployment instructions, see [BUILD.md](BUILD.md).

---

## Project structure

The main files in this project are:

- jafari_app.py — main app interface and prayer flow logic
- jafari_app_tray.py — system tray version with background prayer monitoring
- data_library.py — step data and tasbih configuration
- prayer_text.json — transliteration, meanings, and prayer text content
- audio.py — adhan playback logic
- salat_history.txt — generated local daily tracking file
- [BUILD.md](BUILD.md) — comprehensive build and deployment guide

---

## Screenshots

To see At-Tayyar in action:

1. **From Source**: Run `python jafari_app.py` and capture the main screen
2. **From .exe**: Download the Windows release and run it
3. **Recording**: Use OBS Studio or Windows' built-in Game Bar (Win+G) to create a demo video

Key screens to capture:
- Main menu with prayer selection (Fajr, Maghrib, Dhuhr/Asr/Isha)
- Prayer flow example (showing step-by-step guidance)
- Tasbih counter display
- System tray version in taskbar

Contributors are welcome to submit screenshots via pull requests or issues.

---

## Validation

This application has been exercised through real prayer sessions and checked for stable use in daily flow. The app was validated for:

- successful launch
- prayer selection and flow progression
- keyboard navigation and backtracking
- escape/cancel behavior
- stable manual use during a complete prayer session

---

## Roadmap

Planned improvements include:

- easier Windows packaging for distribution
- stronger startup validation and error handling
- broader automated tests for UI and prayer logic
- further accessibility and visual refinements

---

## Fiqh and purpose

The project aims to support seated worship and practical prayer access in a respectful and mindful manner. It reflects a desire to make daily prayer guidance more accessible without sacrificing clarity, privacy, or usability.

---

## License

This project is shared as open-source code for personal, educational, and spiritual benefit. It may be adapted and redistributed freely for non-commercial use.

Designed and developed by klein-apophis11.
