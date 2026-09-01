# jafari_app_tray.py
"""
System tray version of At-Tayyar with background prayer time monitoring.
Runs minimized in the notification area and automatically plays adhan at prayer times.
"""

import tkinter as tk
import os
import time
import threading
import math
import audio
from datetime import datetime
from pathlib import Path

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("⚠️  pystray not installed. Run: pip install pystray pillow")

from data_library import JAFARI_STEPS, TASBIH_PHASES
from ui.ambient_glow import PrayerAmbientGlow


class JafariSeatedAppTray:
    """System tray version with background monitoring and auto-adhan."""

    @staticmethod
    def _format_time_decimal(value):
        total_minutes = int(round(value * 60))
        total_minutes %= 24 * 60
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    @classmethod
    def calculate_qum_prayer_times(cls, date_value=None):
        """Approximate Qum/Leva Institute prayer schedule."""
        if date_value is None:
            date_value = datetime.now().date()

        lat = 34.65
        lon = 50.88
        timezone_hours = 3.5
        day_of_year = date_value.timetuple().tm_yday

        b = 2 * math.pi * (day_of_year - 81) / 364
        equation_of_time = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
        solar_declination = 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))
        lat_rad = math.radians(lat)
        decl_rad = math.radians(solar_declination)

        solar_noon = 12 + ((timezone_hours * 15 - lon) / 15.0) - (equation_of_time / 60.0)

        def time_for_altitude(angle_deg):
            angle_rad = math.radians(angle_deg)
            cos_h = (math.sin(angle_rad) - math.sin(lat_rad) * math.sin(decl_rad)) / (
                math.cos(lat_rad) * math.cos(decl_rad)
            )
            cos_h = max(-1.0, min(1.0, cos_h))
            hour_angle = math.degrees(math.acos(cos_h)) / 15.0
            return solar_noon - hour_angle

        fajr = time_for_altitude(-17)
        dhuhr = solar_noon
        asr = solar_noon + 3.8
        maghrib = time_for_altitude(-0.833)
        isha = time_for_altitude(-15)

        return {
            "Fajr": cls._format_time_decimal(fajr),
            "Dhuhr": cls._format_time_decimal(dhuhr),
            "Asr": cls._format_time_decimal(asr),
            "Maghrib": cls._format_time_decimal(maghrib),
            "Isha": cls._format_time_decimal(isha),
        }

    def __init__(self, root):
        self.root = root
        self.root.title("At-Tayyar: Seated Jafari Salat Guide")
        self.root.geometry("1000x720")
        self.root.configure(bg="#000000")
        self.glow = PrayerAmbientGlow(self.root, bg="#000000")
        self.glow.pack(fill="both", expand=True)
        self.center_panel = tk.Frame(self.glow.container, bg="#000000", width=760)
        self.center_panel.place(relx=0.5, rely=0.5, anchor="center")
        self.prayer_times = self.calculate_qum_prayer_times()

        self.current_step_idx = 0
        self.active_sequence = []
        self.last_triggered_minute = ""
        self.is_cancelled = False
        self.step_library = JAFARI_STEPS
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salat_history.txt")

        # Compact adhan controls
        self.audio_controls = tk.Frame(self.center_panel, bg="#000000")
        self.audio_controls.pack(pady=10)

        self.audio_label = tk.Label(
            self.audio_controls,
            text="Athan Controls",
            font=("Arial", 10, "bold"),
            fg="#FFD54F",
            bg="#000000",
            pady=4
        )
        self.audio_label.pack(anchor="center")

        self.play_button = tk.Button(
            self.audio_controls,
            text="Play Athan",
            command=audio.play_athan,
            bg="#1e7e34",
            fg="white",
            font=("Arial", 12, "bold"),
            width=16,
            relief="flat",
            borderwidth=0,
            pady=6
        )
        self.play_button.pack(side="left", padx=8)

        self.stop_button = tk.Button(
            self.audio_controls,
            text="Stop Athan",
            command=audio.stop_athan,
            bg="#dc3545",
            fg="white",
            font=("Arial", 12, "bold"),
            width=16,
            relief="flat",
            borderwidth=0,
            pady=6
        )
        self.stop_button.pack(side="left", padx=8)

        # Start background monitoring
        self.check_prayer_times()

        self.in_tasbih_mode = False
        self.tasbih_phase_idx = 0
        self.tasbih_current_count = 0
        self.total_rakahs_selected = 2

        # HOME MENU UI
        self.launcher_frame = tk.Frame(self.center_panel, bg="#000000")
        self.launcher_frame.pack(expand=True)

        self.clock_label = tk.Label(self.launcher_frame, text="Time: --:--:--", font=("Arial", 14, "bold"), fg="#A0A0A0", bg="#000000")
        self.clock_label.pack(pady=(0, 8))

        current_streak = self.load_local_streak()
        self.streak_label = tk.Label(self.launcher_frame, text=f"🔥 Daily Habit Streak: {current_streak} Days", font=("Arial", 18, "bold"), fg="#FFD54F", bg="#000000")
        self.streak_label.pack(pady=(0, 12))

        launcher_title = tk.Label(self.launcher_frame, text="Select Your Daily Salat", font=("Arial", 28, "bold"), fg="#FFB300", bg="#000000")
        launcher_title.pack(pady=(0, 10))

        btn_config = {"font": ("Arial", 16, "bold"), "fg": "#FFFFFF", "bg": "#1A1A1A", "activebackground": "#333333", "activeforeground": "#FFFFFF", "width": 28, "pady": 12}
        tk.Button(self.launcher_frame, text="Fajr (2 Rakahs)", command=lambda: self.setup_prayer_flow(2), **btn_config).pack(pady=8)
        tk.Button(self.launcher_frame, text="Maghrib (3 Rakahs)", command=lambda: self.setup_prayer_flow(3), **btn_config).pack(pady=8)
        tk.Button(self.launcher_frame, text="Dhuhr / Asr / Isha (4 Rakahs)", command=lambda: self.setup_prayer_flow(4), **btn_config).pack(pady=8)

        self.alarm_status_label = tk.Label(self.launcher_frame, text="🔒 Secure Private Mode • Habit Tracker Active", font=("Arial", 12, "italic"), fg="#00E676", bg="#000000")
        self.alarm_status_label.pack(pady=(18, 0))

        # ACTIVE PRAYER UI
        self.prayer_frame = tk.Frame(self.center_panel, bg="#000000")

        self.header_frame = tk.Frame(self.prayer_frame, bg="#000000")
        self.header_frame.pack(fill="x", padx=40, pady=20)

        self.title_label = tk.Label(self.header_frame, text="", font=("Arial", 28, "bold"), fg="#FFB300", bg="#000000", anchor="w")
        self.title_label.pack(side="left")

        self.rakah_counter_label = tk.Label(self.header_frame, text="", font=("Arial", 26, "bold"), fg="#FF3333", bg="#000000", anchor="e")
        self.rakah_counter_label.pack(side="right")

        self.arabic_label = tk.Label(self.prayer_frame, text="", font=("Arial", 48, "bold"), fg="#FFFFFF", bg="#000000", justify="center")
        self.arabic_label.pack(pady=18)

        self.action_label = tk.Label(self.prayer_frame, text="", font=("Arial", 20), fg="#B0BEC5", bg="#000000", justify="center")
        self.action_label.pack(pady=16)

        self.footer_label = tk.Label(self.prayer_frame, text="[ SPACEBAR: Next  •  BACKSPACE: Previous ]", font=("Arial", 14, "italic"), fg="#555555", bg="#000000")
        self.footer_label.pack(side="bottom", pady=40)

        self.root.bind("<space>", self.next_step)
        self.root.bind("<BackSpace>", self.prev_step)
        self.root.bind("<Escape>", self.cancel_step)

        threading.Thread(target=self.start_clock_loop, daemon=True).start()

    def load_local_streak(self):
        if not os.path.exists(self.history_file):
            return 0
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                dates = [line.strip() for line in f.readlines() if line.strip()]
            if not dates:
                return 0
            return len(sorted(list(set(dates)), reverse=True))
        except Exception:
            return 0

    def record_completed_salat(self):
        today_str = time.strftime("%Y-%m-%d")
        try:
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(today_str + "\n")
        except Exception:
            pass

    def start_clock_loop(self):
        current_time_str = time.strftime("%H:%M:%S")
        try:
            if hasattr(self, 'clock_label'):
                self.clock_label.config(text=f"Time: {current_time_str}")
        except Exception:
            pass
        self.root.after(1000, self.start_clock_loop)

    def reset_to_launcher(self):
        self.in_tasbih_mode = False
        self.active_sequence = []
        self.current_step_idx = 0
        self.prayer_frame.pack_forget()
        self.streak_label.config(text=f"🔥 Daily Habit Streak: {self.load_local_streak()} Days")
        self.launcher_frame.pack(expand=True)

    def setup_prayer_flow(self, rakahs):
        self.in_tasbih_mode = False
        self.total_rakahs_selected = rakahs

        def tag_flow(steps, r_num):
            return [{**step, "rakah_num": r_num} for step in steps]

        r1 = tag_flow([self.step_library["qiyam_1"], self.step_library["ruku"], self.step_library["sujud_1"], self.step_library["jalsah"], self.step_library["sujud_2"]], 1)
        r2 = tag_flow([self.step_library["qiyam_2"], self.step_library["qunoot"], self.step_library["ruku"], self.step_library["sujud_1"], self.step_library["jalsah"], self.step_library["sujud_2"]], 2)
        r3 = tag_flow([self.step_library["qiyam_generic"], self.step_library["ruku"], self.step_library["sujud_1"], self.step_library["jalsah"], self.step_library["sujud_2"]], 3)
        r4 = tag_flow([self.step_library["qiyam_generic"], self.step_library["ruku"], self.step_library["sujud_1"], self.step_library["jalsah"], self.step_library["sujud_2"]], 4)

        tk_step = [{**self.step_library["takbeer"], "rakah_num": 1}]
        t_mid = [{**self.step_library["tashahhud_mid"], "rakah_num": 0}]
        t_final = [{**self.step_library["tashahhud_final"], "rakah_num": 0}]

        self.active_sequence = tk_step + r1
        if rakahs == 2: self.active_sequence += r2 + t_final
        elif rakahs == 3: self.active_sequence += r2 + t_mid + r3 + t_final
        elif rakahs == 4: self.active_sequence += r2 + t_mid + r3 + t_mid + r4 + t_final

        self.current_step_idx = 0
        self.launcher_frame.pack_forget()
        self.prayer_frame.pack(fill="both", expand=True)
        self.update_ui()

    def update_ui(self):
        if getattr(self, 'in_tasbih_mode', False):
            self.update_tasbih_display()
            return

        if self.current_step_idx < len(self.active_sequence):
            current_data = self.active_sequence[self.current_step_idx]
            self.title_label.config(text=current_data.get("title", ""))
            self.arabic_label.config(text=current_data.get("arabic", ""))

            translit_text = current_data.get("transliteration", "")
            action_text = current_data.get("action", "")

            combined_text = f"Translit: {translit_text}\n\nInstructions: {action_text}"
            self.action_label.config(text=combined_text)

            r_val = current_data.get("rakah_num", 0)
            if r_val > 0:
                self.rakah_counter_label.config(text=f"Rakah: {r_val} / {self.total_rakahs_selected}")
            else:
                self.rakah_counter_label.config(text="Pause")
        else:
            if getattr(self, 'is_cancelled', False):
                self.is_cancelled = False
                self.reset_to_launcher()
                return

            if not self.in_tasbih_mode:
                self.in_tasbih_mode = True
                self.tasbih_phase_idx = 0
                self.tasbih_current_count = 0
                self.rakah_counter_label.config(text="Ta'qibat")
                self.record_completed_salat()
                self.update_tasbih_display()
                return

    def update_tasbih_display(self):
        if self.tasbih_phase_idx < len(TASBIH_PHASES):
            phase = TASBIH_PHASES[self.tasbih_phase_idx]
            self.title_label.config(text=f"📿 Tasbih of Lady Fatima (sa) • Phase {self.tasbih_phase_idx + 1}/{len(TASBIH_PHASES)}")

            if isinstance(phase, dict):
                arabic_val = phase.get("arabic", "")
                count_val = phase.get("count", 34)
                translit_val = phase.get("transliteration", phase.get("transit", ""))
                meaning_val = phase.get("meaning", "")
            else:
                arabic_val = ""
                count_val = 34
                translit_val = str(phase)
                meaning_val = ""

            self.arabic_label.config(text=arabic_val)

            parts = [f"Count: {self.tasbih_current_count} / {count_val}"]
            if translit_val:
                parts.append(f"Translit: {translit_val}")
            if meaning_val:
                parts.append(f"Meaning: {meaning_val}")

            self.action_label.config(text="\n".join(parts))
            self.footer_label.config(text="[ Tap SPACEBAR to increment the counter count ]")

        else:
            self.title_label.config(text="Salat & Ta'qibat Complete")
            self.arabic_label.config(text="🌿")
            self.action_label.config(text="May Allah accept your daily devotion and grant you ease.")
            self.footer_label.config(text="[ Press SPACEBAR to safely return to the selection menu ]")

    def prev_step(self, event=None):
        if not self.active_sequence or self.in_tasbih_mode:
            return
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.update_ui()

    def cancel_step(self, event=None):
        self.active_sequence = []
        self.in_tasbih_mode = False
        self.current_step_idx = 0
        self.is_cancelled = True
        self.reset_to_launcher()

    def next_step(self, event=None):
        if not self.active_sequence:
            return

        if not self.in_tasbih_mode:
            self.current_step_idx += 1
            self.update_ui()
            return

        if self.tasbih_phase_idx < len(TASBIH_PHASES):
            phase = TASBIH_PHASES[self.tasbih_phase_idx]
            self.tasbih_current_count += 1

            target_count = phase.get("count", 34) if isinstance(phase, dict) else 34

            if self.tasbih_current_count >= target_count:
                self.tasbih_phase_idx += 1
                self.tasbih_current_count = 0
            self.update_tasbih_display()

        else:
            self.reset_to_launcher()

    def check_prayer_times(self):
        """Background prayer time monitor that runs every minute."""
        current_time_str = datetime.now().strftime("%H:%M")

        if current_time_str != self.last_triggered_minute:
            if hasattr(self, 'prayer_times') and self.prayer_times:
                for prayer_name, prayer_time_val in self.prayer_times.items():
                    formatted_prayer_time = str(prayer_time_val).strip()
                    if current_time_str == formatted_prayer_time:
                        self.last_triggered_minute = current_time_str
                        audio.play_athan()
                        self.glow.start_glow(prayer_name)
                        print(f"⏰ Automated Athan Event: {prayer_name} triggered")
                        break

        self.root.after(10000, self.check_prayer_times)


def create_tray_icon():
    """Create a simple icon for the system tray."""
    if not TRAY_AVAILABLE:
        return None

    # Create a simple icon image
    size = (64, 64)
    image = Image.new('RGB', size, color='black')
    draw = ImageDraw.Draw(image)
    # Draw a simple prayer icon (vertical bar)
    draw.rectangle([30, 10, 34, 54], fill='gold')
    return image


def run_tray_version():
    """Run the app in system tray mode."""
    if not TRAY_AVAILABLE:
        print("⚠️  Pystray not available. Running standard GUI version instead.")
        window = tk.Tk()
        app = JafariSeatedAppTray(window)
        window.mainloop()
        return

    # Create the Tkinter window
    window = tk.Tk()
    app = JafariSeatedAppTray(window)

    # Create system tray icon
    icon_image = create_tray_icon()

    def show_window():
        window.deiconify()
        window.lift()

    def hide_window():
        window.withdraw()

    def setup_tray():
        menu = pystray.Menu(
            pystray.MenuItem("Show", show_window),
            pystray.MenuItem("Prayer Times", lambda: print(app.prayer_times)),
            pystray.MenuItem("Test Adhan", audio.play_athan),
            pystray.MenuItem("Exit", lambda: on_exit(icon)),
        )
        icon = pystray.Icon("At-Tayyar", icon_image, menu=menu)

        def on_exit(icon):
            icon.stop()
            window.quit()

        icon.run()

    # Start tray in background thread
    tray_thread = threading.Thread(target=setup_tray, daemon=True)
    tray_thread.start()

    # Run main window
    window.mainloop()


if __name__ == "__main__":
    run_tray_version()
