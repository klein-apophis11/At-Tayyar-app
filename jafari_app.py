# jafari_app.py
import tkinter as tk
import os
import time
import threading

# Import step library and the tasbih counter dictionary parameters cleanly
from data_library import JAFARI_STEPS, TASBIH_PHASES

class JafariSeatedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("At-Tayyar: Seated Jafari Salat Guide")
        self.root.geometry("1000x720")
        self.root.configure(bg="#000000")

        # ⚙️ SET YOUR LOCAL PRAYER TIMES HERE (24-Hour Format "HH:MM")
        self.prayer_times = {
            "Fajr": "05:15", "Dhuhr": "12:30", "Asr": "16:00", "Maghrib": "19:45", "Isha": "21:00"
        }

        self.current_step_idx = 0
        self.active_sequence = []
        self.last_triggered_minute = ""
        self.step_library = JAFARI_STEPS
        
        # Tracking parameters
        self.in_tasbih_mode = False
        self.tasbih_phase_idx = 0
        self.tasbih_current_count = 0
        self.total_rakahs_selected = 2

        # --- HOME MENU UI ---
        self.launcher_frame = tk.Frame(root, bg="#000000")
        self.launcher_frame.pack(expand=True)

        self.clock_label = tk.Label(self.launcher_frame, text="Time: --:--:--", font=("Arial", 16), fg="#555555", bg="#000000")
        self.clock_label.pack(pady=5)

        current_streak = self.load_local_streak()
        self.streak_label = tk.Label(self.launcher_frame, text=f"🔥 Daily Habit Streak: {current_streak} Days", font=("Arial", 18, "bold"), fg="#FFD54F", bg="#000000")
        self.streak_label.pack(pady=10)

        launcher_title = tk.Label(self.launcher_frame, text="Select Your Daily Salat", font=("Arial", 28, "bold"), fg="#FFB300", bg="#000000")
        launcher_title.pack(pady=15)

        btn_config = {"font": ("Arial", 18, "bold"), "fg": "#FFFFFF", "bg": "#1A1A1A", "activebackground": "#333333", "activeforeground": "#FFFFFF", "width": 25, "pady": 12}
        tk.Button(self.launcher_frame, text="Fajr (2 Rakahs)", command=lambda: self.setup_prayer_flow(2), **btn_config).pack(pady=8)
        tk.Button(self.launcher_frame, text="Maghrib (3 Rakahs)", command=lambda: self.setup_prayer_flow(3), **btn_config).pack(pady=8)
        tk.Button(self.launcher_frame, text="Dhuhr / Asr / Isha (4 Rakahs)", command=lambda: self.setup_prayer_flow(4), **btn_config).pack(pady=8)

        self.alarm_status_label = tk.Label(self.launcher_frame, text="🔒 100% Secure Private Mode • Habit Tracker Active", font=("Arial", 12, "italic"), fg="#00E676", bg="#000000")
        self.alarm_status_label.pack(pady=20)

        # --- ACTIVE PRAYER UI ---
        self.prayer_frame = tk.Frame(root, bg="#000000")
        
        # Sub-frame at the top for headers and the new corner counter
        self.header_frame = tk.Frame(self.prayer_frame, bg="#000000")
        self.header_frame.pack(fill="x", padx=40, pady=20)
        
        self.title_label = tk.Label(self.header_frame, text="", font=("Arial", 26, "bold"), fg="#FFB300", bg="#000000", anchor="w")
        self.title_label.pack(side="left")
        
        # 🔴 THE VISUAL RAKAH COUNTER LABEL (Set to solid, high-contrast Bright Red)
        self.rakah_counter_label = tk.Label(self.header_frame, text="", font=("Arial", 24, "bold"), fg="#FF3333", bg="#000000", anchor="e")
        self.rakah_counter_label.pack(side="right")

        self.arabic_label = tk.Label(self.prayer_frame, text="", font=("Arial", 42, "bold"), fg="#FFFFFF", bg="#000000", justify="center")
        self.arabic_label.pack(pady=20)
        
        self.action_label = tk.Label(self.prayer_frame, text="", font=("Arial", 18), fg="#B0BEC5", bg="#000000", justify="center")
        self.action_label.pack(pady=20)
        
        self.footer_label = tk.Label(self.prayer_frame, text="[ SPACEBAR: Next  •  BACKSPACE: Previous ]", font=("Arial", 14, "italic"), fg="#555555", bg="#000000")
        self.footer_label.pack(side="bottom", pady=40)

        # Precise key event configurations mapped natively to functions
        self.root.bind("<space>", self.next_step)
        self.root.bind("<BackSpace>", self.prev_step)
        self.root.bind("<Escape>", self.cancel_step)

        
        threading.Thread(target=self.start_clock_loop, daemon=True).start()

    def load_local_streak(self):
        history_file = "salat_history.txt"
        if not os.path.exists(history_file): return 0
        try:
            with open(history_file, "r") as f:
                dates = [line.strip() for line in f.readlines() if line.strip()]
            if not dates: return 0
            return len(sorted(list(set(dates)), reverse=True))
        except: return 0

    def record_completed_salat(self):
        history_file = "salat_history.txt"
        today_str = time.strftime("%Y-%m-%d")
        try:
            with open(history_file, "a") as f: f.write(today_str + "\n")
        except: pass

    def start_clock_loop(self):
        while True:
            current_time_str = time.strftime("%H:%M:%S")
            try: self.clock_label.config(text=f"Time: {current_time_str}")
            except: pass 
            time.sleep(1)

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
        if self.current_step_idx < len(self.active_sequence):
            current_data = self.active_sequence[self.current_step_idx]
            self.title_label.config(text=current_data["title"])
            self.arabic_label.config(text=current_data["arabic"])
            self.action_label.config(text=current_data["action"])
            
            r_val = current_data.get("rakah_num", 0)
            if r_val > 0:
                self.rakah_counter_label.config(text=f"Rakah: {r_val} / {self.total_rakahs_selected}")
            else:
                self.rakah_counter_label.config(text="Pause")
        else:
            if getattr(self, 'is_cancelled', False):
                    self.is_cancelled = False; self.prayer_frame.pack_forget(); self.launcher_frame.pack(expand=True); return


            
            if not self.in_tasbih_mode:
                self.in_tasbih_mode = True
                self.tasbih_phase_idx = 0
                self.tasbih_current_count = 0
                self.rakah_counter_label.config(text="Ta'qibat")
                self.record_completed_salat()
            self.update_tasbih_display()

    def update_tasbih_display(self):
        if self.tasbih_phase_idx < len(TASBIH_PHASES):
            phase = TASBIH_PHASES[self.tasbih_phase_idx]
            self.title_label.config(text=f"📿 Tasbih of Lady Fatima (sa) • Phase {self.tasbih_phase_idx + 1}/3")
            self.arabic_label.config(text=phase["arabic"])
            counter_text = f"Count: {self.tasbih_current_count} / {phase['count']}\n\nTranslit: {phase['translit']}\nMeaning: {phase['meaning']}"
            self.action_label.config(text=counter_text)
            self.footer_label.config(text="[ Tap SPACEBAR to increment the counter count ]")
        else:
            self.title_label.config(text="Salat & Ta'qibat Complete")
            self.arabic_label.config(text="🌿")
            self.action_label.config(text="May Allah accept your daily devotion, blessings, and grant you ease.")
            self.footer_label.config(text="[ Press SPACEBAR to safely return to the selection menu ]")

    def prev_step(self, event=None):
        """Goes back one step cleanly if you press BackSpace."""
        if not self.active_sequence or self.in_tasbih_mode: return
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.update_ui()
    def cancel_step(self, event=None):
             """Cancels the current prayer session and returns to the main menu."""
             self.active_sequence = []
             self.in_tasbih_mode = False
             self.current_step_idx = 0
             self.is_cancelled = True
             self.update_ui()


    def next_step(self, event=None):
        if not self.active_sequence: return
        if not self.in_tasbih_mode:
            self.current_step_idx += 1
            self.update_ui()
            return
        if self.tasbih_phase_idx < len(TASBIH_PHASES):
            phase = TASBIH_PHASES[self.tasbih_phase_idx]
            self.tasbih_current_count += 1
            if self.tasbih_current_count >= phase["count"]:
                self.tasbih_phase_idx += 1
                self.tasbih_current_count = 0
            self.update_tasbih_display()
        else:
            self.in_tasbih_mode = False
            self.active_sequence = []
            self.prayer_frame.pack_forget()
            self.streak_label.config(text=f"🔥 Daily Habit Streak: {self.load_local_streak()} Days")
            self.launcher_frame.pack(expand=True)

if __name__ == "__main__":
    window = tk.Tk()
    app = JafariSeatedApp(window)
    window.mainloop()
