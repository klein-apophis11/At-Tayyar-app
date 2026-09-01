# Building At-Tayyar for Windows & Linux

This guide explains how to build a standalone Windows .exe and prepare the app for Linux distribution.

## Windows Standalone Executable (.exe)

### Prerequisites
```powershell
pip install pyinstaller pillow pystray pygame
```

### Standard GUI Version

```powershell
cd "c:\path\to\At-Tayyar"
pyinstaller --onefile --windowed --name "At-Tayyar" jafari_app.py
```

Result: `dist/At-Tayyar.exe` (single executable, ~50-80 MB with dependencies)

Users can download and run without Python installed.

### System Tray Version (Runs in background)

```powershell
pyinstaller --onefile --windowed --name "At-Tayyar-Tray" jafari_app_tray.py
```

Result: `dist/At-Tayyar-Tray.exe` (minimizes to system tray, auto-plays adhan)

### Creating a GitHub Release

1. Build the .exe files (above)
2. Copy `dist/At-Tayyar.exe` to a releases folder
3. Create a GitHub Release:
   - Go to https://github.com/klein-apophis11/At-Tayyar-app/releases
   - Click "Create a new release"
   - Tag: v1.0.0 (or version number)
   - Title: "At-Tayyar v1.0.0 - Standalone Release"
   - Upload the .exe file(s)
   - Publish

Users can now download the .exe directly without knowing about Python.

---

## Linux Installation

### Ubuntu/Debian

```bash
# Install Python and dependencies
sudo apt-get update
sudo apt-get install python3 python3-tk python3-pip libsdl2-mixer-2.0-0

# Clone and run
git clone https://github.com/klein-apophis11/At-Tayyar-app.git
cd At-Tayyar-app
pip3 install -r requirements.txt
python3 jafari_app.py
```

### Fedora/RHEL

```bash
# Install Python and dependencies
sudo dnf install python3 python3-tkinter python3-pip SDL2_mixer

# Clone and run
git clone https://github.com/klein-apophis11/At-Tayyar-app.git
cd At-Tayyar-app
pip3 install -r requirements.txt
python3 jafari_app.py
```

### Arch Linux

```bash
# Install Python and dependencies
sudo pacman -S python tk python-pip sdl2_mixer

# Clone and run
git clone https://github.com/klein-apophis11/At-Tayyar-app.git
cd At-Tayyar-app
pip install -r requirements.txt
python jafari_app.py
```

### Creating a Desktop Shortcut (Linux)

Create `~/.local/share/applications/at-tayyar.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=At-Tayyar
Exec=/usr/bin/python3 /path/to/At-Tayyar-app/jafari_app.py
Icon=application-x-python
Categories=Utility;
Terminal=false
```

Then run:
```bash
chmod +x ~/.local/share/applications/at-tayyar.desktop
```

---

## Features by Platform

### Windows (.exe)
- ✅ Standard GUI version: No Python required
- ✅ System Tray version: Runs in background, auto-plays adhan
- ✅ One-file standalone executable
- ✅ Easy distribution via GitHub Releases

### Linux
- ✅ Full Python installation via apt/dnf/pacman
- ✅ Desktop application shortcuts
- ✅ Background daemon capability
- ✅ Can use same jafari_app_tray.py for system tray (Linux-compatible)

### macOS (Potential)
- ⚠️ Similar to Linux installation
- ⚠️ Tkinter included but may need additional setup
- ⚠️ System tray icon (pystray) works but requires additional macOS permissions

---

## Troubleshooting

### PyInstaller Build Issues
- Ensure all imports can be resolved
- Run `pip install -r requirements.txt` first
- Check Python version: `python --version` (3.8+)

### Linux Audio Issues
- Ensure SDL2_mixer is installed
- Test with: `python3 -c "import pygame; pygame.mixer.init()"`
- If no audio device: app continues to work, just no sound

### Tray Icon Not Appearing
- Windows: Ensure pystray and Pillow are installed
- Linux: Some desktop environments have limited tray support
- Fallback: App still runs as standard window

---

## Distribution Strategy

1. **Windows Users**: Download .exe from GitHub Releases → Run immediately
2. **Linux Users**: Clone repo or use package manager → Follow Linux install guide
3. **macOS Users**: Clone repo → Follow Linux guide (similar steps)

This provides **zero-friction installation** for Windows while maintaining open-source accessibility for Linux/Mac.
