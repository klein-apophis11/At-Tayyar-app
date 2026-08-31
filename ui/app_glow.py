import tkinter as tk

class PrayerAmbientGlow(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg="#000000", highlightthickness=0)
        
        # Create the inner container frame for app widgets
        self.container = tk.Frame(self, bg="#000000")
        self.window_id = self.create_window(0, 0, window=self.container, anchor="nw")
        
        self.bind("<Configure>", self._on_resize)
        self.current_prayer = None

    def _on_resize(self, event):
        w, h = event.width, event.height
        self.delete("border_glow")

        # Choose border color based on state or active fade
        color = getattr(self, 'dynamic_color', None)
        if not color:
            color = "#ff4500" if self.current_prayer else "#1e7e34"

        # Draw ambient border
        self.create_rectangle(
            4, 4, w - 4, h - 4,
            outline=color, width=3, tags="border_glow"
        )

        # Resize container inside the canvas
        padding = 15
        self.coords(self.window_id, padding, padding)
        self.itemconfigure(self.window_id, width=w - (padding * 2), height=h - (padding * 2))

    def start_glow(self, prayer_name):
        """Triggers the gentle red-orange alert glow that fades out over time."""
        self.current_prayer = prayer_name
        
        # Starting color: vibrant red-orange (#FF4500) -> RGB (255, 69, 0)
        # Target/Resting color: dark green (#1e7e34) -> RGB (30, 126, 52)
        self.fade_start_rgb = (255, 69, 0)
        self.fade_end_rgb = (30, 126, 52)
        
        # 10-second duration with steps every 100ms = 100 total steps
        self.fade_steps_total = 100
        self.fade_step_current = 0
        
        self._step_fade()

    def _step_fade(self):
        """Interpolates color step-by-step and schedules the next frame."""
        if self.fade_step_current <= self.fade_steps_total:
            progress = self.fade_step_current / self.fade_steps_total
            
            # Linear interpolation formula for RGB components
            r = int(self.fade_start_rgb[0] + (self.fade_end_rgb[0] - self.fade_start_rgb[0]) * progress)
            g = int(self.fade_start_rgb[1] + (self.fade_end_rgb[1] - self.fade_start_rgb[1]) * progress)
            b = int(self.fade_start_rgb[2] + (self.fade_end_rgb[2] - self.fade_start_rgb[2]) * progress)
            
            # Format back to a hex color string
            self.dynamic_color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Trigger a redraw via resize event
            self.event_generate("<Configure>", width=self.winfo_width(), height=self.winfo_height())
            
            self.fade_step_current += 1
            # Schedule next step in 100 milliseconds
            self.after(100, self._step_fade)
        else:
            # Clear dynamic color to return to standard resting state
            self.dynamic_color = None
            self.event_generate("<Configure>", width=self.winfo_width(), height=self.winfo_height())
