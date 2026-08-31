import tkinter as tk
from PIL import Image, ImageDraw, ImageFilter, ImageTk


def _hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def _adjust_color(hex_color, amount):
    r, g, b = _hex_to_rgb(hex_color)
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    return _rgb_to_hex((r, g, b))


class PrayerAmbientGlow(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg="#000000", highlightthickness=0)

        self.container = tk.Frame(self, bg="#000000")
        self.window_id = self.create_window(0, 0, window=self.container, anchor="center")
        self.glow_image_id = None
        self.glow_photo = None

        self.bind("<Configure>", self._on_resize)
        self.current_prayer = None
        self._fade_job = None
        self.dynamic_color = None

    def _build_glow_image(self, color, width, height):
        background = Image.new("RGBA", (max(1, int(width)), max(1, int(height))), (0, 0, 0, 0))
        glow = Image.new("RGBA", (max(1, int(width)), max(1, int(height))), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow)

        r, g, b = _hex_to_rgb(color)
        inset = 18
        radius = 18
        glow_stops = [
            (26, 60),
            (18, 45),
            (12, 30),
            (8, 18),
            (4, 10),
        ]

        for spread, alpha in glow_stops:
            box = [spread + inset, spread + inset, width - spread - inset, height - spread - inset]
            if hasattr(draw, "rounded_rectangle"):
                draw.rounded_rectangle(
                    box,
                    radius=radius,
                    outline=(r, g, b, alpha),
                    width=max(2, spread // 2),
                )
            else:
                draw.rectangle(box, outline=(r, g, b, alpha), width=max(2, spread // 2))

        blurred = glow.filter(ImageFilter.GaussianBlur(15))
        background.alpha_composite(blurred)

        edge = ImageDraw.Draw(background)
        if hasattr(edge, "rounded_rectangle"):
            edge.rounded_rectangle(
                [inset, inset, width - inset, height - inset],
                radius=radius,
                outline=(r, g, b, 180),
                width=2,
            )
        else:
            edge.rectangle(
                [inset, inset, width - inset, height - inset],
                outline=(r, g, b, 180),
                width=2,
            )

        return ImageTk.PhotoImage(background)

    def _on_resize(self, event):
        w, h = event.width, event.height
        self.delete("glow_image")
        self.delete("border_glow")

        color = getattr(self, 'dynamic_color', None)
        if not color:
            color = "#f2b36b" if self.current_prayer else "#7cae8a"

        glow_photo = self._build_glow_image(color, w, h)
        self.glow_photo = glow_photo
        self.glow_image_id = self.create_image(w / 2, h / 2, image=glow_photo, anchor="center", tags="glow_image")
        self.tag_lower(self.glow_image_id)

        self.container.configure(width=w, height=h)
        self.create_rectangle(
            4, 4, w - 4, h - 4,
            outline=color, width=1, tags="border_glow"
        )

        padding = 40
        content_width = max(200, w - (padding * 2))
        content_height = max(200, h - (padding * 2))
        x_pos = w / 2
        y_pos = h / 2

        self.coords(self.window_id, x_pos, y_pos)
        self.itemconfigure(self.window_id, width=content_width, height=content_height)

    def start_glow(self, prayer_name):
        """Triggers the gentle red-orange alert glow that fades out over time."""
        self.current_prayer = prayer_name

        if self._fade_job is not None:
            self.after_cancel(self._fade_job)
            self._fade_job = None

        self.fade_start_rgb = (227, 171, 121)
        self.fade_end_rgb = (124, 174, 138)
        self.fade_steps_total = 100
        self.fade_step_current = 0

        self._step_fade()

    def _step_fade(self):
        """Interpolates color step-by-step and schedules the next frame."""
        if self.fade_step_current <= self.fade_steps_total:
            progress = self.fade_step_current / self.fade_steps_total

            r = int(self.fade_start_rgb[0] + (self.fade_end_rgb[0] - self.fade_start_rgb[0]) * progress)
            g = int(self.fade_start_rgb[1] + (self.fade_end_rgb[1] - self.fade_start_rgb[1]) * progress)
            b = int(self.fade_start_rgb[2] + (self.fade_end_rgb[2] - self.fade_start_rgb[2]) * progress)

            self.dynamic_color = f"#{r:02x}{g:02x}{b:02x}"

            self.event_generate("<Configure>", width=self.winfo_width(), height=self.winfo_height())

            self.fade_step_current += 1
            self._fade_job = self.after(100, self._step_fade)
        else:
            self.current_prayer = None
            self.dynamic_color = None
            self._fade_job = None
            self.event_generate("<Configure>", width=self.winfo_width(), height=self.winfo_height())