"""
Generate concept visualisation PNGs for the Reefs README.
Run: python gen_diagrams.py
Outputs: concept-side-view.png, concept-top-view.png, concept-system.png
"""

import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Arc
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
os.makedirs(OUT, exist_ok=True)

BG   = "#0d0d12"
WALL = "#1a1a2e"
WOOD = "#5c3d1e"
WOOD_GRAIN = "#4a3018"
ALUM = "#8a8a9a"
LED  = "#ffe066"
GLOW = "#ffb347"
WIRE = "#2ecc71"
BOX  = "#1e3a5f"
BOX2 = "#2a4f80"
TXT  = "#e8e8f0"
DIM  = "#888899"
ACCENT = "#4fc3f7"

# ─────────────────────────────────────────────
# 1. SIDE-VIEW CROSS-SECTION
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 11)
ax.set_ylim(0, 6)
ax.axis("off")

# Wall
wall = patches.Rectangle((0, 0), 0.6, 6, linewidth=0, facecolor=WALL)
ax.add_patch(wall)
ax.text(0.3, 5.7, "WALL", color=DIM, fontsize=7, ha="center", va="top",
        fontfamily="monospace")

# Glow gradient on wall  (simulate with overlapping transparent wedges)
for i, (alpha, width) in enumerate(zip(
        np.linspace(0.35, 0.0, 18),
        np.linspace(0.6, 3.5, 18))):
    glow_rect = patches.FancyBboxPatch(
        (0.0, 1.5 - width * 0.3),
        0.02,
        width * 1.0 + 0.6,
        boxstyle="round,pad=0",
        linewidth=0, facecolor=GLOW, alpha=alpha)
    ax.add_patch(glow_rect)

# Fan of light rays from LED strip (at x≈1.6, y=2..4)
for y_start in np.linspace(2.1, 3.9, 10):
    for x_end, y_end, a in [
        (0.62, y_start, 0.08),
        (0.62, y_start + (y_start - 3.0) * 0.5, 0.04),
    ]:
        ax.plot([1.6, x_end], [y_start, y_end],
                color=LED, alpha=a, linewidth=0.8)

# Aluminium channel (rear of wood, facing wall)
alum_chan = patches.Rectangle((1.5, 1.9), 0.18, 2.2,
                               linewidth=1, edgecolor=ALUM,
                               facecolor="#5a5a6e", zorder=4)
ax.add_patch(alum_chan)
ax.text(1.59, 3.0, "Al\nchan.", color=ALUM, fontsize=6.5,
        ha="center", va="center", fontfamily="monospace", zorder=5)

# LED strip glow dots
for y in np.linspace(2.05, 3.95, 7):
    glow = plt.Circle((1.59, y), 0.14, color=LED, alpha=0.18, zorder=3)
    ax.add_patch(glow)
    dot = plt.Circle((1.59, y), 0.055, color=LED, zorder=5)
    ax.add_patch(dot)

# Driftwood body
wood = FancyBboxPatch((1.68, 1.6), 2.1, 2.8,
                       boxstyle="round,pad=0.12",
                       linewidth=1.5, edgecolor=WOOD_GRAIN,
                       facecolor=WOOD, zorder=3)
ax.add_patch(wood)

# wood grain lines
for y_g in np.linspace(1.85, 4.1, 8):
    noise = np.random.default_rng(int(y_g * 100)).uniform(-0.05, 0.05, 12)
    xs = np.linspace(1.75, 3.7, 12)
    ys = y_g + noise
    ax.plot(xs, ys, color=WOOD_GRAIN, alpha=0.55, linewidth=0.7, zorder=4)

ax.text(2.73, 3.0, "DRIFTWOOD", color="#c8a070", fontsize=8.5,
        ha="center", va="center", fontfamily="monospace",
        fontweight="bold", zorder=6)
ax.text(2.73, 2.6, "(rear face = wall side)", color=DIM, fontsize=6.5,
        ha="center", va="center", fontfamily="monospace", zorder=6)

# Arrow labels
def ann(ax, x1, y1, x2, y2, label, color=TXT):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.2))
    ax.text(x1, y1, label, color=color, fontsize=7.5,
            ha="left", va="center", fontfamily="monospace")

ax.annotate("", xy=(1.6, 4.3), xytext=(2.0, 4.8),
            arrowprops=dict(arrowstyle="->", color=LED, lw=1.3))
ax.text(2.05, 4.85, "SK6812 RGBW strip\n(60 LEDs, 1 m)", color=LED,
        fontsize=7.5, va="center", fontfamily="monospace")

ax.annotate("", xy=(0.62, 3.5), xytext=(1.0, 4.7),
            arrowprops=dict(arrowstyle="->", color=GLOW, lw=1.3))
ax.text(1.05, 4.72, "wall-wash glow", color=GLOW,
        fontsize=7.5, va="center", fontfamily="monospace")

# Room side annotation
ax.text(9.0, 3.0, "← ROOM SIDE →\n(wood faces viewer)", color=DIM,
        fontsize=8, ha="center", va="center", fontfamily="monospace")
ax.annotate("", xy=(3.85, 3.0), xytext=(7.5, 3.0),
            arrowprops=dict(arrowstyle="<-", color=DIM, lw=1.0))

# Cross-section label
ax.text(5.5, 5.6, "CROSS-SECTION  —  Side View  (not to scale)",
        color=TXT, fontsize=10, ha="center", fontfamily="monospace",
        fontweight="bold")

# Dimension bracket: wall → rear face of wood
ax.annotate("", xy=(0.62, 0.5), xytext=(1.5, 0.5),
            arrowprops=dict(arrowstyle="<->", color=DIM, lw=1.0))
ax.text(1.06, 0.28, "≈ 20 mm gap\n(air + channel)", color=DIM,
        fontsize=6.5, ha="center", fontfamily="monospace")

plt.tight_layout()
plt.savefig(os.path.join(OUT, "concept-side-view.png"),
            dpi=160, facecolor=BG, bbox_inches="tight")
plt.close()
print("concept-side-view.png ✓")


# ─────────────────────────────────────────────
# 2. TOP-DOWN ROOM LAYOUT
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 8), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

# Room walls
room = patches.Rectangle((0.4, 0.4), 11.2, 7.2,
                           linewidth=2, edgecolor="#3a3a5c",
                           facecolor="none")
ax.add_patch(room)
ax.text(6.0, 7.8, "TOP-DOWN FLOOR PLAN  (not to scale)",
        color=TXT, fontsize=10, ha="center", fontfamily="monospace",
        fontweight="bold")

# Top wall (where lamps are mounted)
top_wall = patches.Rectangle((0.4, 6.8), 11.2, 0.4,
                               linewidth=0, facecolor=WALL)
ax.add_patch(top_wall)
ax.text(6.0, 7.02, "WALL", color=DIM, fontsize=7.5,
        ha="center", va="center", fontfamily="monospace")

# Glow from each lamp onto top wall (top-down: glow spreads downward)
for lamp_cx in [2.8, 7.8]:
    for radius, alpha in zip(np.linspace(0.5, 3.5, 14),
                              np.linspace(0.28, 0.0, 14)):
        ellipse = patches.Ellipse((lamp_cx, 6.3), radius * 2.2, radius * 0.8,
                                   linewidth=0, facecolor=GLOW, alpha=alpha)
        ax.add_patch(ellipse)

# Lamp 1 — driftwood (top view: long horizontal rectangle)
for lamp_cx, label in [(2.8, "LAMP 1"), (7.8, "LAMP 2")]:
    # wood body (top view)
    wood_tv = FancyBboxPatch((lamp_cx - 0.6, 6.25), 1.2, 0.45,
                              boxstyle="round,pad=0.07",
                              linewidth=1.5, edgecolor=WOOD_GRAIN,
                              facecolor=WOOD, zorder=4)
    ax.add_patch(wood_tv)
    # LED strip (thin line on rear/wall-facing edge)
    ax.plot([lamp_cx - 0.55, lamp_cx + 0.55], [6.68, 6.68],
            color=LED, linewidth=3.5, zorder=5, solid_capstyle="round")
    ax.text(lamp_cx, 6.47, label, color="#c8a070", fontsize=8,
            ha="center", va="center", fontfamily="monospace",
            fontweight="bold", zorder=6)

# Control box (bottom-right corner area)
box_rect = FancyBboxPatch((9.5, 0.8), 1.8, 1.2,
                           boxstyle="round,pad=0.08",
                           linewidth=1.5, edgecolor=ACCENT,
                           facecolor=BOX, zorder=4)
ax.add_patch(box_rect)
ax.text(10.4, 1.4, "CONTROL\nBOX", color=ACCENT, fontsize=8,
        ha="center", va="center", fontfamily="monospace",
        fontweight="bold", zorder=5)

# Cable runs: control box → under floor → up to lamps
# Use dashed lines with corner bends
def cable_path(ax, points, color=WIRE, lw=1.8):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=color, linewidth=lw, linestyle="--",
            dashes=(5, 3), zorder=3)

# Lamp 1 cable
cable_path(ax, [(10.4, 0.8), (10.4, 0.4), (2.8, 0.4), (2.8, 6.25)])
ax.text(6.6, 0.25, "2 m cable run  (5V + GND + DATA)  ×2",
        color=WIRE, fontsize=7.5, ha="center", fontfamily="monospace")

# Lamp 2 cable
cable_path(ax, [(10.4, 0.8), (10.4, 0.4), (7.8, 0.4), (7.8, 6.25)])

# Mains arrow into control box
ax.annotate("", xy=(11.3, 1.4), xytext=(11.6, 1.4),
            arrowprops=dict(arrowstyle="<-", color="#ff6b6b", lw=1.5))
ax.text(11.65, 1.4, "230 V\nmains", color="#ff6b6b", fontsize=7,
        va="center", fontfamily="monospace")

# Wi-Fi cloud
ax.text(10.4, 2.4, "☁ Wi-Fi → HA", color=ACCENT, fontsize=8,
        ha="center", fontfamily="monospace")
ax.plot([10.4, 10.4], [2.0, 2.2], color=ACCENT,
        linewidth=1.2, linestyle="dotted")

# Legend
for y, color, label in [(1.2, WIRE, "power + data cable"),
                         (0.9, LED, "SK6812 RGBW strip"),
                         (0.6, GLOW, "wall-wash glow")]:
    ax.plot([0.7, 1.2], [y, y], color=color, linewidth=2.5)
    ax.text(1.3, y, label, color=DIM, fontsize=7.5,
            va="center", fontfamily="monospace")

plt.tight_layout()
plt.savefig(os.path.join(OUT, "concept-top-view.png"),
            dpi=160, facecolor=BG, bbox_inches="tight")
plt.close()
print("concept-top-view.png ✓")


# ─────────────────────────────────────────────
# 3. SYSTEM BLOCK DIAGRAM
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 5.5), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 13)
ax.set_ylim(0, 5.5)
ax.axis("off")

def block(ax, x, y, w, h, title, subtitle="", color=BOX, border=ACCENT,
          title_color=TXT, sub_color=DIM):
    rect = FancyBboxPatch((x, y), w, h,
                           boxstyle="round,pad=0.12",
                           linewidth=1.8, edgecolor=border,
                           facecolor=color, zorder=3)
    ax.add_patch(rect)
    ty = y + h / 2 + (0.12 if subtitle else 0)
    ax.text(x + w / 2, ty, title, color=title_color,
            fontsize=9, ha="center", va="center",
            fontfamily="monospace", fontweight="bold", zorder=4)
    if subtitle:
        ax.text(x + w / 2, y + h / 2 - 0.25, subtitle, color=sub_color,
                fontsize=7.5, ha="center", va="center",
                fontfamily="monospace", zorder=4)

def arrow(ax, x1, y1, x2, y2, label="", color=TXT, lw=1.5, ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color,
                                lw=lw, linestyle=ls))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.18, label, color=color, fontsize=7.5,
                ha="center", fontfamily="monospace")

ax.text(6.5, 5.2, "SYSTEM BLOCK DIAGRAM",
        color=TXT, fontsize=11, ha="center", fontfamily="monospace",
        fontweight="bold")

# Mains
block(ax, 0.3, 1.8, 1.6, 1.4, "230 V AC\nMains", color="#2a1a1a",
      border="#ff6b6b", title_color="#ff9999")

# PSU
block(ax, 2.4, 1.6, 2.0, 1.8, "Honeywell PSU", "5 V / 10 A (50 W)",
      color="#1a2a1a", border="#66bb6a", title_color="#a5d6a7")

# Arrow: mains → PSU
arrow(ax, 1.9, 2.5, 2.4, 2.5, "L / N / PE", color="#ff6b6b")

# ESP32
block(ax, 5.1, 1.6, 2.4, 1.8, "ESP32", "WLED firmware",
      color=BOX, border=ACCENT, title_color=ACCENT)

# Arrow: PSU → ESP32
arrow(ax, 4.4, 2.5, 5.1, 2.5, "5 V / GND", color="#66bb6a")

# Level shifter (small, above/between)
block(ax, 5.3, 3.7, 1.9, 0.85, "74AHCT125", "3.3→5V level shift",
      color="#1a1a2e", border="#ce93d8", title_color="#ce93d8")
ax.annotate("", xy=(6.2, 3.7), xytext=(6.2, 3.4),
            arrowprops=dict(arrowstyle="->", color="#ce93d8", lw=1.2))
ax.text(6.55, 3.55, "GPIO 16/17", color="#ce93d8",
        fontsize=7, fontfamily="monospace")

# Fuse boxes
block(ax, 5.3, 0.35, 0.9, 0.85, "5A\nFuse", color="#2a2a1a",
      border="#ffd54f", title_color="#ffd54f")
block(ax, 6.4, 0.35, 0.9, 0.85, "5A\nFuse", color="#2a2a1a",
      border="#ffd54f", title_color="#ffd54f")
arrow(ax, 4.4, 1.8, 5.7, 1.2, "", color="#ffd54f")
arrow(ax, 4.4, 1.8, 6.85, 1.2, "", color="#ffd54f")
ax.text(5.7, 1.32, "5 V\nrails", color="#ffd54f", fontsize=7,
        ha="center", fontfamily="monospace")

# Lamp 1
block(ax, 8.2, 3.1, 2.2, 1.6, "LAMP 1", "SK6812 RGBW\n60 LEDs · 1 m",
      color="#1f1a10", border=LED, title_color=LED)
# Lamp 2
block(ax, 8.2, 0.9, 2.2, 1.6, "LAMP 2", "SK6812 RGBW\n60 LEDs · 1 m",
      color="#1f1a10", border=LED, title_color=LED)

# Level shifter → Lamp 1 data
arrow(ax, 7.2, 4.1, 8.2, 3.9, "DATA 1", color="#ce93d8")
# Level shifter → Lamp 2 data
ax.plot([6.2, 7.5, 7.5, 8.2], [3.7, 3.7, 1.7, 1.7],
        color="#ce93d8", linewidth=1.5, linestyle="--", dashes=(5, 3), zorder=3)
ax.annotate("", xy=(8.2, 1.7), xytext=(7.7, 1.7),
            arrowprops=dict(arrowstyle="->", color="#ce93d8", lw=1.5))
ax.text(7.85, 2.1, "DATA 2", color="#ce93d8", fontsize=7.5,
        ha="center", fontfamily="monospace")

# Fuse → Lamp power
arrow(ax, 6.2, 1.2, 8.2, 3.2, "", color="#ffd54f")
arrow(ax, 6.85, 1.2, 8.2, 1.1, "", color="#ffd54f")
ax.text(7.7, 2.3, "5V/GND\n(×2)", color="#ffd54f", fontsize=7.5,
        ha="center", fontfamily="monospace")

# Wi-Fi / HA
block(ax, 10.9, 3.5, 1.8, 1.1, "Home\nAssistant", color="#1a1a2e",
      border="#4db6ac", title_color="#80cbc4")
ax.plot([6.3, 6.3, 10.5, 10.5, 10.9], [3.4, 4.6, 4.6, 4.1, 4.1],
        color="#4db6ac", linewidth=1.5, linestyle="dotted", zorder=3)
ax.text(8.6, 4.72, "Wi-Fi (WLED native integration)",
        color="#4db6ac", fontsize=7.5, ha="center", fontfamily="monospace")

# Enclosure boundary
enc = patches.Rectangle((4.8, 0.2), 5.5, 5.0,
                          linewidth=1.5, edgecolor="#3a3a5c",
                          facecolor="none", linestyle="--", zorder=1)
ax.add_patch(enc)
ax.text(7.55, 5.25, "3D-printed control box", color=DIM,
        fontsize=7.5, ha="center", fontfamily="monospace")

plt.tight_layout()
plt.savefig(os.path.join(OUT, "concept-system.png"),
            dpi=160, facecolor=BG, bbox_inches="tight")
plt.close()
print("concept-system.png ✓")
