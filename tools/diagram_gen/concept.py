"""
concept.py — Real-world concept illustrations using matplotlib.

Public API
----------
draw_side_view(config, out_path)
    Cross-section showing wall / light-wash / driftwood / room.

draw_top_view(config, out_path)
    Top-down floor-plan showing lamp positions, cable runs, control box.
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


# ─── Side-view cross-section ──────────────────────────────────────────────────

def draw_side_view(config: dict, out_path: str) -> None:
    """
    Side-view cross-section of a single wall-wash lamp.

    config keys (all optional, fall back to sensible defaults):
        title       str   figure title
        wood_label  str   label inside the wood silhouette
        led_count   int   number of LED dots to draw on the strip
        wall_color  str   hex colour for the wall surface
    """
    style.apply_dark_theme()

    title      = config.get("title", "CROSS-SECTION  —  Side View  (not to scale)")
    wood_label = config.get("wood_label", "DRIFTWOOD")
    led_count  = config.get("led_count", 7)
    wall_c     = config.get("wall_color", style.WALL)

    fig, ax = plt.subplots(figsize=(11, 6), facecolor=style.BG)
    ax.set_facecolor(style.BG)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Wall
    wall = patches.Rectangle((0, 0), 0.6, 6, linewidth=0, facecolor=wall_c)
    ax.add_patch(wall)
    ax.text(0.3, 5.75, "WALL", color=style.DIM, fontsize=7,
            ha="center", va="top", fontfamily="monospace")

    # Glow on wall (gradient from many overlapping transparent rects)
    for alpha, h in zip(np.linspace(0.32, 0.0, 20), np.linspace(0.6, 4.0, 20)):
        g = patches.FancyBboxPatch(
            (0.0, 3.0 - h * 0.5), 0.02, h,
            boxstyle="round,pad=0",
            linewidth=0, facecolor=style.GLOW, alpha=alpha)
        ax.add_patch(g)

    # Light rays
    strip_x, strip_y_lo, strip_y_hi = 1.6, 2.1, 3.9
    for y_s in np.linspace(strip_y_lo, strip_y_hi, 10):
        for (xe, ye, a) in [(0.62, y_s, 0.08),
                            (0.62, y_s + (y_s - 3.0) * 0.45, 0.04)]:
            ax.plot([strip_x, xe], [y_s, ye],
                    color=style.LED_DOT, alpha=a, linewidth=0.8)

    # Aluminium channel
    alum = patches.Rectangle((1.5, 1.9), 0.18, 2.2,
                              linewidth=1, edgecolor=style.ALUM,
                              facecolor="#5a5a6e", zorder=4)
    ax.add_patch(alum)
    ax.text(1.59, 3.0, "Al\nchan.", color=style.ALUM, fontsize=6.5,
            ha="center", va="center", fontfamily="monospace", zorder=5)

    # LED dots
    for y in np.linspace(strip_y_lo, strip_y_hi, led_count):
        glow_c = plt.Circle((strip_x, y), 0.14, color=style.LED_DOT,
                             alpha=0.18, zorder=3)
        ax.add_patch(glow_c)
        dot = plt.Circle((strip_x, y), 0.055, color=style.LED_DOT, zorder=5)
        ax.add_patch(dot)

    # Driftwood body
    wood = FancyBboxPatch((1.68, 1.6), 2.1, 2.8,
                          boxstyle="round,pad=0.12",
                          linewidth=1.5, edgecolor=style.WOOD_DARK,
                          facecolor=style.WOOD, zorder=3)
    ax.add_patch(wood)

    rng = np.random.default_rng(42)
    for y_g in np.linspace(1.85, 4.1, 8):
        noise = rng.uniform(-0.05, 0.05, 12)
        xs = np.linspace(1.75, 3.70, 12)
        ax.plot(xs, y_g + noise, color=style.WOOD_DARK,
                alpha=0.55, linewidth=0.7, zorder=4)

    ax.text(2.73, 3.05, wood_label, color=style.TXT_WD, fontsize=8.5,
            ha="center", va="center", fontfamily="monospace",
            fontweight="bold", zorder=6)
    ax.text(2.73, 2.60, "(rear face = wall side)", color=style.DIM, fontsize=6.5,
            ha="center", va="center", fontfamily="monospace", zorder=6)

    # Annotations
    ax.annotate("", xy=(strip_x, 4.3), xytext=(2.0, 4.85),
                arrowprops=dict(arrowstyle="->", color=style.LED_DOT, lw=1.3))
    ax.text(2.05, 4.9, "SK6812 RGBW strip\n(60 LEDs, 1 m)",
            color=style.LED_DOT, fontsize=7.5, va="center",
            fontfamily="monospace")

    ax.annotate("", xy=(0.62, 3.6), xytext=(1.1, 4.75),
                arrowprops=dict(arrowstyle="->", color=style.GLOW, lw=1.3))
    ax.text(1.15, 4.78, "wall-wash glow", color=style.GLOW,
            fontsize=7.5, va="center", fontfamily="monospace")

    ax.text(8.5, 3.0, "← ROOM SIDE →\n(wood faces viewer)", color=style.DIM,
            fontsize=8, ha="center", va="center", fontfamily="monospace")
    ax.annotate("", xy=(3.85, 3.0), xytext=(7.0, 3.0),
                arrowprops=dict(arrowstyle="<-", color=style.DIM, lw=1.0))

    ax.annotate("", xy=(0.62, 0.5), xytext=(1.5, 0.5),
                arrowprops=dict(arrowstyle="<->", color=style.DIM, lw=1.0))
    ax.text(1.06, 0.28, "≈ 20 mm gap\n(air + channel)", color=style.DIM,
            fontsize=6.5, ha="center", fontfamily="monospace")

    ax.text(5.5, 5.65, title, color=style.TXT, fontsize=10,
            ha="center", fontfamily="monospace", fontweight="bold")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    plt.savefig(out_path, facecolor=style.BG, bbox_inches="tight")
    plt.close(fig)
    print(f"  concept:   {os.path.basename(out_path)} ✓")


# ─── Top-down floor plan ───────────────────────────────────────────────────────

def draw_top_view(config: dict, out_path: str) -> None:
    """
    Top-down floor-plan with multiple lamps, control box, and cable runs.

    config keys:
        title       str
        lamps       list of {"label": "LAMP 1", "cx": float, "cy": float}
                    — cy should be close to top wall (y ~ 6.8)
        box_pos     (x, y)  bottom-left of control box
        wall_y      float   y coordinate of top wall lower edge (default 6.8)
    """
    style.apply_dark_theme()

    title   = config.get("title", "TOP-DOWN FLOOR PLAN  (not to scale)")
    lamps   = config.get("lamps", [
        {"label": "LAMP 1", "cx": 2.8},
        {"label": "LAMP 2", "cx": 7.8},
    ])
    box_pos = config.get("box_pos", (9.5, 0.8))
    wall_y  = config.get("wall_y", 6.8)

    fig, ax = plt.subplots(figsize=(12, 8), facecolor=style.BG)
    ax.set_facecolor(style.BG)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Room outline
    ax.add_patch(patches.Rectangle((0.4, 0.4), 11.2, 7.2,
                                   linewidth=2, edgecolor="#3a3a5c",
                                   facecolor="none"))
    ax.text(6.0, 7.85, title, color=style.TXT, fontsize=10,
            ha="center", fontfamily="monospace", fontweight="bold")

    # Top wall
    ax.add_patch(patches.Rectangle((0.4, wall_y), 11.2, 0.4,
                                   linewidth=0, facecolor=style.WALL))
    ax.text(6.0, wall_y + 0.22, "WALL", color=style.DIM, fontsize=7.5,
            ha="center", va="center", fontfamily="monospace")

    # Lamp glow overlays and bodies
    for lamp in lamps:
        cx = lamp["cx"]
        cy = lamp.get("cy", wall_y - 0.1)

        for radius, alpha in zip(np.linspace(0.5, 3.5, 14),
                                 np.linspace(0.28, 0.0, 14)):
            ax.add_patch(patches.Ellipse(
                (cx, cy), radius * 2.2, radius * 0.8,
                linewidth=0, facecolor=style.GLOW, alpha=alpha))

        # Wood body (top view: horizontal rectangle)
        ax.add_patch(FancyBboxPatch(
            (cx - 0.6, cy - 0.25), 1.2, 0.45,
            boxstyle="round,pad=0.07",
            linewidth=1.5, edgecolor=style.WOOD_DARK, facecolor=style.WOOD, zorder=4))

        # LED strip (thin line on wall-facing edge)
        ax.plot([cx - 0.55, cx + 0.55], [cy + 0.17, cy + 0.17],
                color=style.LED_DOT, linewidth=3.5, zorder=5, solid_capstyle="round")

        ax.text(cx, cy - 0.02, lamp["label"], color=style.TXT_WD, fontsize=8,
                ha="center", va="center", fontfamily="monospace",
                fontweight="bold", zorder=6)

    # Control box
    bx, by = box_pos
    ax.add_patch(FancyBboxPatch((bx, by), 1.8, 1.2,
                                boxstyle="round,pad=0.08",
                                linewidth=1.5, edgecolor=style.ACCENT,
                                facecolor=style.BOX_BLUE, zorder=4))
    ax.text(bx + 0.9, by + 0.6, "CONTROL\nBOX", color=style.ACCENT, fontsize=8,
            ha="center", va="center", fontfamily="monospace",
            fontweight="bold", zorder=5)

    # Cable runs (dashed)
    box_cx = bx + 0.9
    for lamp in lamps:
        cx = lamp["cx"]
        cy = lamp.get("cy", wall_y - 0.1)
        pts = [(box_cx, by), (box_cx, 0.4), (cx, 0.4), (cx, cy - 0.25)]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.plot(xs, ys, color=style.WIRE_GRN, linewidth=1.8,
                linestyle="--", dashes=(5, 3), zorder=3)

    ax.text(6.0, 0.25, "2 m cable runs  (5 V + GND + DATA) ×2",
            color=style.WIRE_GRN, fontsize=7.5, ha="center",
            fontfamily="monospace")

    # Mains into box
    ax.annotate("", xy=(bx + 1.8, by + 0.6), xytext=(12.0 - 0.1, by + 0.6),
                arrowprops=dict(arrowstyle="<-", color="#ff6b6b", lw=1.5))
    ax.text(12.05, by + 0.6, "230 V\nmains", color="#ff6b6b",
            fontsize=7, va="center", fontfamily="monospace")

    # Wi-Fi cloud
    ax.text(box_cx, by + 1.5, "☁ Wi-Fi → HA", color=style.ACCENT,
            fontsize=8, ha="center", fontfamily="monospace")
    ax.plot([box_cx, box_cx], [by + 1.2, by + 1.35],
            color=style.ACCENT, linewidth=1.2, linestyle="dotted")

    # Legend
    for yi, (c, lbl) in enumerate([
        (style.WIRE_GRN, "power + data cable"),
        (style.LED_DOT,  "SK6812 RGBW strip"),
        (style.GLOW,     "wall-wash glow"),
    ]):
        y_leg = 0.5 + yi * 0.35
        ax.plot([0.7, 1.2], [y_leg, y_leg], color=c, linewidth=2.5)
        ax.text(1.3, y_leg, lbl, color=style.DIM, fontsize=7.5,
                va="center", fontfamily="monospace")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    plt.savefig(out_path, facecolor=style.BG, bbox_inches="tight")
    plt.close(fig)
    print(f"  concept:   {os.path.basename(out_path)} ✓")
