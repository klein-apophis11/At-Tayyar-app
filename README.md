# At-Tayyar (الطَّيَّار): Offline Seated Prayer Guide 📿♿

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

### Prerequisites

- Python 3.10+
- Tkinter, which is included with most standard Windows Python installations

### Run the app

```bash
python jafari_app.py
```

### Optional Windows launcher

```bat
@echo off
cd /d "%~dp0"
start "" pythonw "jafari_app.py"
```

---

## Project structure

The main files in this project are:

- jafari_app.py — main app interface and prayer flow logic
- data_library.py — step data and tasbih configuration
- prayer_text.json — transliteration, meanings, and prayer text content
- audio.py — adhan playback logic
- salat_history.txt — generated local daily tracking file

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
