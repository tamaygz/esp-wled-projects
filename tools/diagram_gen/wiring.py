"""
wiring.py — High-fidelity physical wiring diagrams using drawsvg.

Generates a color-coded, labelled wiring diagram showing the physical
build: ESP32 dev board, level-shifter IC, JST connectors, and
color-coded wires with pin labels.

Public API
----------
draw_physical_wiring(config, out_path)
    config keys:
        title           str
        gpio_map        list of {"gpio": 16, "label": "LAMP 1 DATA", "color": "#43a047"}
        power_label     str   e.g. "5V / 10A PSU"
        controller      str   e.g. "ESP32-WROOM-32"
        shifter         bool  include 74AHCT125 level shifter
        outputs         list  of {"name": "LAMP 1"}
"""

from __future__ import annotations
import os
import drawsvg as draw
from . import style


# ─── SVG helpers ──────────────────────────────────────────────────────────────

def _rect(group, x, y, w, h, fill, stroke=None, rx=6, stroke_w=1.5):
    stroke = stroke or fill
    group.append(draw.Rectangle(x, y, w, h, fill=fill,
                                stroke=stroke, stroke_width=stroke_w, rx=rx))


def _text(group, x, y, text, color=style.TXT,
          size=11, weight="normal", family="monospace", anchor="middle"):
    group.append(draw.Text(text, size, x, y,
                           fill=color, font_family=family,
                           font_weight=weight, text_anchor=anchor,
                           dominant_baseline="central"))


def _line(group, x1, y1, x2, y2, color=style.WIRE_GRN, w=3):
    group.append(draw.Line(x1, y1, x2, y2,
                           stroke=color, stroke_width=w,
                           stroke_linecap="round"))


def _wire_path(group, points, color=style.WIRE_GRN, w=3):
    """Draw a multi-segment wire with right-angle bends."""
    if len(points) < 2:
        return
    pts = points
    path = draw.Path(stroke=color, stroke_width=w,
                     stroke_linecap="round", stroke_linejoin="round",
                     fill="none")
    path.M(*pts[0])
    for p in pts[1:]:
        path.L(*p)
    group.append(path)


def _chip(group, x, y, w, h, label, pin_labels_left, pin_labels_right,
          fill=style.BOX_PURPLE, stroke=style.ACCENT2,
          pin_h=22, pin_w=8):
    """Draw an IC package with pin labels on left and right sides."""
    _rect(group, x, y, w, h, fill, stroke, rx=4)
    _text(group, x + w / 2, y + h / 2, label,
          color=style.ACCENT2, size=11, weight="bold")

    n_left  = len(pin_labels_left)
    n_right = len(pin_labels_right)
    step_l  = h / (n_left + 1) if n_left  else 0
    step_r  = h / (n_right + 1) if n_right else 0

    for i, lbl in enumerate(pin_labels_left):
        py = y + (i + 1) * step_l
        group.append(draw.Circle(x - 3, py, 3, fill=stroke))
        _text(group, x + 6, py, lbl, color=style.DIM, size=9, anchor="start")

    for i, lbl in enumerate(pin_labels_right):
        py = y + (i + 1) * step_r
        group.append(draw.Circle(x + w + 3, py, 3, fill=stroke))
        _text(group, x + w - 6, py, lbl, color=style.DIM, size=9, anchor="end")


def _board(group, x, y, w, h, label, fill=style.BOX_BLUE,
           stroke=style.ACCENT):
    _rect(group, x, y, w, h, fill, stroke, rx=8)
    _text(group, x + w / 2, y + 18, label,
          color=style.ACCENT, size=12, weight="bold")


def _pin_row(group, x, y, pins, spacing=22, direction="right",
             dot_color=style.ACCENT):
    """Draw a labelled row of pin circles."""
    for i, (pin_num, pin_name) in enumerate(pins):
        if direction == "right":
            px, py = x + i * spacing, y
        else:
            px, py = x, y + i * spacing
        group.append(draw.Circle(px, py, 4, fill=dot_color,
                                 stroke="#111", stroke_width=1))
        _text(group, px, py + 12, str(pin_num),
              color=style.DIM, size=8)


# ─── Main function ─────────────────────────────────────────────────────────────

def draw_physical_wiring(config: dict, out_path: str) -> None:
    """
    Render a physical wiring diagram (color-coded) to *out_path* as SVG + PNG.

    Saves both <basename>.svg and <basename>.png.
    """
    W, H = 1100, 700
    title       = config.get("title", "Physical Wiring Diagram")
    ctrl_label  = config.get("controller", "ESP32-WROOM-32")
    shifter     = config.get("shifter", True)
    outputs     = config.get("outputs", [{"name": "LAMP 1"}, {"name": "LAMP 2"}])
    gpio_map    = config.get("gpio_map", [
        {"gpio": 16, "label": "DATA 1", "color": style.WIRE_GRN},
        {"gpio": 17, "label": "DATA 2", "color": "#26c6da"},
    ])
    psu_label   = config.get("power_label", "5V / 10A PSU")

    d = draw.Drawing(W, H)

    # Background
    d.append(draw.Rectangle(0, 0, W, H, fill=style.BG))

    # Title
    d.append(draw.Text(title, 16, W / 2, 28,
                       fill=style.TXT, font_family="monospace",
                       font_weight="bold", text_anchor="middle",
                       dominant_baseline="central"))

    # ── PSU ─────────────────────────────────────────────────────────────────
    psu_g = draw.Group()
    _board(psu_g, 30, 80, 130, 90, psu_label,
           fill=style.BOX_GREEN, stroke=style.ACCENT_GRN)
    _text(psu_g, 95, 130, "+5 V / GND out →",
          color=style.ACCENT_GRN, size=9)
    d.append(psu_g)

    # ── ESP32 board ──────────────────────────────────────────────────────────
    esp_x, esp_y, esp_w, esp_h = 240, 60, 200, 250
    esp_g = draw.Group()
    _board(esp_g, esp_x, esp_y, esp_w, esp_h, ctrl_label)

    # GPIO pin dots on the right edge of the ESP32 board
    gpio_colors = [g["color"] for g in gpio_map]
    for i, gm in enumerate(gpio_map):
        py = esp_y + 80 + i * 40
        esp_g.append(draw.Circle(esp_x + esp_w, py, 5,
                                 fill=gm["color"], stroke="#111", stroke_width=1))
        _text(esp_g, esp_x + esp_w - 10, py, f"GPIO {gm['gpio']}",
              color=gm["color"], size=9, anchor="end")

    # 5V + GND pins on board
    esp_g.append(draw.Circle(esp_x + esp_w, esp_y + 200, 5,
                             fill=style.WIRE_RED, stroke="#111", stroke_width=1))
    _text(esp_g, esp_x + esp_w - 10, esp_y + 200, "5V",
          color=style.WIRE_RED, size=9, anchor="end")
    esp_g.append(draw.Circle(esp_x + esp_w, esp_y + 225, 5,
                             fill=style.WIRE_BLK, stroke="#555", stroke_width=1))
    _text(esp_g, esp_x + esp_w - 10, esp_y + 225, "GND",
          color=style.DIM, size=9, anchor="end")
    d.append(esp_g)

    # ── 74AHCT125 level shifter ───────────────────────────────────────────────
    if shifter:
        sh_x, sh_y, sh_w, sh_h = 510, 90, 130, 170
        sh_g = draw.Group()
        _chip(sh_g, sh_x, sh_y, sh_w, sh_h, "74AHCT125",
              ["1A", "2A", "nOE1", "nOE2"],
              ["1Y", "2Y", "VCC", "GND"])
        _text(sh_g, sh_x + sh_w / 2, sh_y + sh_h + 14, "Level Shifter",
              color=style.ACCENT2, size=9)
        d.append(sh_g)

        # Wires: ESP32 GPIO → 330Ω resistor label → level shifter inputs
        for i, gm in enumerate(gpio_map[:2]):
            esp_pin_y   = esp_y + 80 + i * 40
            sh_pin_y    = sh_y + (i + 1) * (sh_h / 5)
            mid_x       = (esp_x + esp_w + sh_x) / 2

            # ESP32 out → mid → resistor annotation → shifter in
            _wire_path(d,
                       [(esp_x + esp_w, esp_pin_y),
                        (mid_x - 20, esp_pin_y),
                        (mid_x - 20, sh_pin_y),
                        (sh_x, sh_pin_y)],
                       color=gm["color"], w=2.5)

            # 330Ω label on wire
            rx, ry = mid_x - 20, (esp_pin_y + sh_pin_y) / 2
            d.append(draw.Rectangle(rx - 18, ry - 9, 36, 18,
                                    fill=style.BOX_BLUE, stroke=gm["color"],
                                    stroke_width=1, rx=3))
            d.append(draw.Text("330Ω", 8, rx, ry,
                                fill=gm["color"], font_family="monospace",
                                text_anchor="middle", dominant_baseline="central"))

        # Wires: shifter outputs → JST connectors
        for i, (out, gm) in enumerate(zip(outputs[:2], gpio_map[:2])):
            sh_out_y = sh_y + (i + 1) * (sh_h / 5)
            _wire_path(d,
                       [(sh_x + sh_w, sh_out_y),
                        (sh_x + sh_w + 80, sh_out_y)],
                       color=gm["color"], w=2.5)
            # JST label
            jst_x = sh_x + sh_w + 80
            d.append(draw.Rectangle(jst_x, sh_out_y - 14, 80, 28,
                                    fill="#1a1a2e", stroke=gm["color"],
                                    stroke_width=1, rx=4))
            d.append(draw.Text(f"JST → {out['name']}", 9,
                                jst_x + 40, sh_out_y,
                                fill=gm["color"], font_family="monospace",
                                text_anchor="middle", dominant_baseline="central"))

        # VCC to shifter
        _wire_path(d,
                   [(esp_x + esp_w, esp_y + 200),
                    (sh_x + sh_w / 2, esp_y + 200),
                    (sh_x + sh_w / 2, sh_y - 5),
                    (sh_x + sh_w - 20, sh_y - 5)],
                   color=style.WIRE_RED, w=2.0)

        # GND to shifter
        _wire_path(d,
                   [(esp_x + esp_w, esp_y + 225),
                    (sh_x + sh_w / 2 + 10, esp_y + 225),
                    (sh_x + sh_w / 2 + 10, sh_y + sh_h + 5),
                    (sh_x + sh_w - 20, sh_y + sh_h + 5)],
                   color=style.WIRE_BLK, w=2.0)

    # ── PSU power wires ──────────────────────────────────────────────────────
    # PSU → ESP32 5V
    _wire_path(d,
               [(160, 105), (240, 105), (240, esp_y + 200), (esp_x, esp_y + 200)],
               color=style.WIRE_RED, w=2.5)
    # PSU → ESP32 GND
    _wire_path(d,
               [(160, 140), (220, 140), (220, esp_y + 225), (esp_x, esp_y + 225)],
               color=style.WIRE_BLK, w=2.5)

    # ── Legend ───────────────────────────────────────────────────────────────
    legend_g = draw.Group()
    legend_items = [
        (style.WIRE_RED,  "+5 V power rail"),
        (style.WIRE_BLK,  "GND"),
        (style.WIRE_GRN,  "DATA (Lamp 1)"),
        ("#26c6da",        "DATA (Lamp 2)"),
        (style.ACCENT2,   "3.3→5V level-shifted"),
    ]
    for i, (c, lbl) in enumerate(legend_items):
        ly = H - 110 + i * 20
        legend_g.append(draw.Line(30, ly, 60, ly,
                                  stroke=c, stroke_width=3,
                                  stroke_linecap="round"))
        legend_g.append(draw.Text(lbl, 9, 68, ly,
                                  fill=style.DIM, font_family="monospace",
                                  dominant_baseline="central"))
    d.append(legend_g)

    # ── Save SVG + PNG ────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    base = os.path.splitext(out_path)[0]

    d.save_svg(base + ".svg")
    print(f"  wiring:    {os.path.basename(base)}.svg ✓")

    # Try raster export (requires cairosvg or similar; skip gracefully if missing)
    try:
        d.save_png(base + ".png")
        print(f"  wiring:    {os.path.basename(base)}.png ✓")
    except Exception:
        # Fallback: use matplotlib to render the SVG as PNG via cairosvg
        try:
            import cairosvg
            cairosvg.svg2png(url=base + ".svg", write_to=base + ".png", scale=2)
            print(f"  wiring:    {os.path.basename(base)}.png ✓ (via cairosvg)")
        except ImportError:
            print(f"  wiring:    SVG saved; install cairosvg to also get PNG")
