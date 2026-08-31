# At-Tayyar (الطَّيَّار): Offline Seated Prayer Guide 📿♿

At-Tayyar is a private, offline desktop app that helps Muslims perform daily prayers from a seated position with clear visual guidance, Jafari prayer flow support, and built-in tasbih tracking.

Designed for accessibility and ease of use, the project offers a calm, no-network prayer companion for users who need a simple, guided approach to worship.

---

## Highlights

- Offline-first design with no internet dependency
- Guided prayer flow for Fajr, Dhuhr, Asr, Maghrib, and Isha
- Seated prayer support aligned to Jafari practice
- Built-in tasbih tracking for the Tasbih of Lady Fatima Zahra (sa)
- High-visibility rakah counter for easy tracking
- Manual keyboard controls for a calm, private, no-camera/no-microphone experience

---

## Key Features

- Jafari Multi-Rakah Layouts: Supports the correct structure for Fajr (2 rakahs), Maghrib (3 rakahs), and Dhuhr/Asr/Isha (4 rakahs), with automated transitions during mid-prayer tashahhud intervals.
- Seated Sujud Guidance: Includes guidance on the rukhsah of using the thumb or the back of the hand as a valid turbah/mohr substitute when physical prostration aids are unavailable.
- Integrated Tasbih Counter: Automatically transitions into a dedicated tasbih tracking board after the final tasleem.
- High-Visibility Corner Counter: Displays a bright red rakah indicator in the interface for quick readability while praying.
- Privacy and Security: Runs fully offline. There is no tracking, no database login, no internet connection, and no microphone or camera access.

---

## Controls

The application is intentionally designed around simple manual controls to maintain privacy and ease of use:

- Spacebar: move to the next step
- Backspace: go back to the previous step
- Escape: exit or cancel the current flow

This keeps the experience simple and accessible without relying on voice or camera input.

---

## Installation and Usage

### Prerequisites

- Python 3.10+
- Tkinter (included with standard Python installations on Windows)
- No external package installation required for the current version

### Quick Start

```bash
python jafari_app.py
```

### Windows shortcut option

You can also launch it via a batch file:

```bat
@echo off
cd /d "%~dp0"
start "" pythonw "jafari_app.py"
```

### Repository Structure

Ensure the following files remain in the same folder:

- `jafari_app.py` — main app logic and interface
- `data_library.py` — prayer text, action flow, and transliteration data
- `prayer_text.json` — prayer content and tasbih instructions
- `audio.py` — athan playback logic
- `salat_history.txt` — generated local history file for daily habit tracking

---

## Screenshot

A screenshot can be added here to showcase the main interface and prayer flow.

---

## Troubleshooting

- If the app does not launch, confirm Python 3.10+ is installed and that `tkinter` is available.
- If audio playback fails, the app should continue without crashing, but the sound output may be unavailable on the current machine.
- If the app cannot find data files, verify that all project files remain in the same directory.

---

## Project Status

This project is currently a functional desktop application and a strong personal project with a clear accessibility-focused use case. It is designed for practical use on Windows 10 and is intended as a helpful offline tool rather than a large-scale commercial product.

---

## Roadmap

- Improve packaging for easier Windows distribution
- Add more robust startup validation
- Expand automated tests for prayer flow logic and UI edge cases
- Refine layout and visual polish for a more polished desktop experience
- Continue improving accessibility and usability for seated prayer practice

---

## Fiqh Foundation

This project aims to support seated worship and ease of prayer for individuals following Jafari practice, with careful attention to the rukhsah and practical guidance that makes prayer more manageable in real-life circumstances.

---

## License

This software is shared as open-source code for the spiritual and practical benefit of the global Ummah. It may be copied, adapted, and distributed freely for personal and educational use.

Designed and developed by klein-apophis11.
