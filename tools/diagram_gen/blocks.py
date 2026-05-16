"""
blocks.py — System block diagrams using matplotlib.

Public API
----------
draw_system_blocks(config, out_path)
    Generates a project system block diagram.

    config  dict with keys:
        title       str   diagram title
        psu         str   PSU label (e.g. "Honeywell 5V / 10A")
        controller  str   controller label (e.g. "ESP32\nWLED firmware")
        shifter     str   level shifter label or None to omit
        outputs     list  of {"name": "LAMP 1", "strip": "SK6812 RGBW\n60 LEDs"}
        integration str   smart-home label (e.g. "Home\nAssistant") or None
"""

from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from . import style

# ─── Primitives ───────────────────────────────────────────────────────────────

def _block(ax, x, y, w, h, title, subtitle="",
           face=None, border=None, title_color=None, sub_color=None):
    face        = face        or style.BOX_BLUE
    border      = border      or style.ACCENT
    title_color = title_color or style.TXT
    sub_color   = sub_color   or style.DIM

    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.12",
                          linewidth=1.8, edgecolor=border,
                          facecolor=face, zorder=3)
    ax.add_patch(rect)
    ty = y + h / 2 + (0.12 if subtitle else 0)
    ax.text(x + w / 2, ty, title,
            color=title_color, fontsize=9, ha="center", va="center",
            fontfamily="monospace", fontweight="bold", zorder=4)
    if subtitle:
        ax.text(x + w / 2, y + h / 2 - 0.28, subtitle,
                color=sub_color, fontsize=7.5, ha="center", va="center",
                fontfamily="monospace", zorder=4)


def _arrow(ax, x1, y1, x2, y2, label="", color=None, lw=1.5):
    color = color or style.TXT
    ax.annotate("",
                xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw),
                zorder=3)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.2, label,
                color=color, fontsize=7.5, ha="center",
                fontfamily="monospace", zorder=4)


def _dashed(ax, points, color=None, lw=1.5):
    color = color or style.WIRE_GRN
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=color, linewidth=lw,
            linestyle="--", dashes=(5, 3), zorder=3)


# ─── Main function ─────────────────────────────────────────────────────────────

def draw_system_blocks(config: dict, out_path: str) -> None:
    """Render a system block diagram and save as PNG to *out_path*."""
    style.apply_dark_theme()

    title       = config.get("title", "System Block Diagram")
    psu_label   = config.get("psu", "PSU\n5 V")
    ctrl_label  = config.get("controller", "ESP32\nWLED")
    shifter     = config.get("shifter", None)
    outputs     = config.get("outputs", [])
    integration = config.get("integration", None)

    # Dynamic sizing
    n_out = max(len(outputs), 1)
    fig_h = max(5.5, 2.5 + n_out * 1.8)
    fig, ax = plt.subplots(figsize=(13, fig_h), facecolor=style.BG)
    ax.set_facecolor(style.BG)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    ax.text(6.5, fig_h - 0.35, title,
            color=style.TXT, fontsize=11, ha="center",
            fontfamily="monospace", fontweight="bold")

    mid_y = fig_h / 2

    # Mains block
    _block(ax, 0.3, mid_y - 0.7, 1.6, 1.4,
           "230 V AC\nMains", face="#2a1a1a", border=style.SCH_RED,
           title_color="#ff9999")

    # PSU block
    _block(ax, 2.4, mid_y - 0.9, 2.0, 1.8,
           psu_label.split("\n")[0],
           "\n".join(psu_label.split("\n")[1:]) if "\n" in psu_label else "",
           face=style.BOX_GREEN, border=style.ACCENT_GRN,
           title_color="#a5d6a7")
    _arrow(ax, 1.9, mid_y, 2.4, mid_y, "L / N / PE", color=style.SCH_RED)

    # Controller block
    ctrl_x = 5.2
    _block(ax, ctrl_x, mid_y - 0.9, 2.4, 1.8,
           ctrl_label.split("\n")[0],
           "\n".join(ctrl_label.split("\n")[1:]) if "\n" in ctrl_label else "",
           face=style.BOX_BLUE, border=style.ACCENT,
           title_color=style.ACCENT)
    _arrow(ax, 4.4, mid_y, ctrl_x, mid_y, "5 V / GND", color=style.ACCENT_GRN)

    # Level shifter (optional)
    if shifter:
        sh_x = ctrl_x
        sh_y = mid_y + 1.5
        _block(ax, sh_x, sh_y, 2.4, 0.9,
               shifter.split("\n")[0],
               "\n".join(shifter.split("\n")[1:]) if "\n" in shifter else "",
               face="#1a1a2e", border=style.ACCENT2,
               title_color=style.ACCENT2)
        ax.annotate("",
                    xy=(sh_x + 1.2, sh_y),
                    xytext=(sh_x + 1.2, mid_y + 0.9),
                    arrowprops=dict(arrowstyle="->", color=style.ACCENT2, lw=1.2),
                    zorder=3)
        ax.text(sh_x + 1.6, mid_y + 1.25, "GPIO signals",
                color=style.ACCENT2, fontsize=7.5, fontfamily="monospace")
        out_start_x = sh_x + 2.4
        out_start_y = sh_y + 0.45
    else:
        out_start_x = ctrl_x + 2.4
        out_start_y = mid_y

    # Output blocks (lamps / strips)
    lamp_x = 9.8
    n = len(outputs)
    total_h = n * 1.6 + (n - 1) * 0.3
    base_y = mid_y - total_h / 2

    for i, out in enumerate(outputs):
        ly = base_y + i * 1.9
        _block(ax, lamp_x, ly, 2.2, 1.6,
               out.get("name", f"Output {i+1}"),
               out.get("strip", ""),
               face=style.BOX_DARK, border=style.LED_DOT,
               title_color=style.LED_DOT)

        # Data line (from shifter or controller)
        target_y = ly + 0.8
        if shifter:
            ax.annotate("",
                        xy=(lamp_x, target_y),
                        xytext=(out_start_x, out_start_y),
                        arrowprops=dict(arrowstyle="->",
                                        color=style.ACCENT2,
                                        lw=1.3,
                                        connectionstyle="arc3,rad=0.0"),
                        zorder=3)
        else:
            _arrow(ax, out_start_x, out_start_y, lamp_x, target_y,
                   f"GPIO {16 + i}" if i < 2 else "",
                   color=style.ACCENT2)

        # Power line from PSU
        _dashed(ax, [(4.4, mid_y - 0.5), (4.4, ly + 0.4), (lamp_x, ly + 0.4)],
                color=style.ACCENT_YLW)

    # Fuses annotation
    ax.text(4.5, mid_y - 1.2, "5A fuse\n×each lamp",
            color=style.ACCENT_YLW, fontsize=7.5,
            ha="center", fontfamily="monospace")

    # Smart-home integration
    if integration:
        int_x, int_y = lamp_x, fig_h - 1.6
        _block(ax, int_x, int_y, 2.2, 1.1,
               integration.split("\n")[0],
               "\n".join(integration.split("\n")[1:]) if "\n" in integration else "",
               face="#1a1a2e", border=style.ACCENT_HA,
               title_color="#80cbc4")
        ax.plot([ctrl_x + 1.2, ctrl_x + 1.2, int_x + 1.1],
                [mid_y + 0.9, int_y + 0.6, int_y + 0.6],
                color=style.ACCENT_HA, linewidth=1.5, linestyle="dotted", zorder=3)
        ax.text((ctrl_x + int_x) / 2 + 0.5, int_y + 0.8,
                "Wi-Fi (WLED native)", color=style.ACCENT_HA,
                fontsize=7.5, ha="center", fontfamily="monospace")

    # Enclosure boundary
    enc = patches.Rectangle((4.8, 0.25), 5.5, fig_h - 0.5,
                             linewidth=1.5, edgecolor="#3a3a5c",
                             facecolor="none", linestyle="--", zorder=1)
    ax.add_patch(enc)
    ax.text(7.55, fig_h - 0.55, "3D-printed control box",
            color=style.DIM, fontsize=7.5, ha="center", fontfamily="monospace")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    plt.savefig(out_path, facecolor=style.BG, bbox_inches="tight")
    plt.close(fig)
    print(f"  blocks:    {os.path.basename(out_path)} ✓")
