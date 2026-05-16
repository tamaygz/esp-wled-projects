"""
Shared colour palette, typography, and dimension constants.

All diagram modules import from here so the visual language stays consistent
across every project in the repo.
"""

# ─── Background / surface colours ────────────────────────────────────────────
BG        = "#0d0d12"   # Page / figure background
SURFACE   = "#13131c"   # Elevated surface (panels, cards)
WALL      = "#1a1a2e"   # Wall colour for side/top-view illustrations
BORDER    = "#2a2a40"   # Subtle border lines

# ─── Component colours ────────────────────────────────────────────────────────
WOOD      = "#5c3d1e"
WOOD_DARK = "#4a3018"
ALUM      = "#8a8a9a"   # Aluminium channel

# ─── Wire / signal colours (IEC-ish) ─────────────────────────────────────────
WIRE_RED   = "#e53935"   # +5 V / positive rail
WIRE_BLK   = "#424242"   # GND / negative rail
WIRE_GRN   = "#43a047"   # Data / signal
WIRE_WHT   = "#e0e0e0"   # 3.3 V
WIRE_YLW   = "#fdd835"   # Clock / SPI SCK

# ─── LED / glow colours ───────────────────────────────────────────────────────
LED_DOT   = "#ffe066"   # Individual LED dot
GLOW      = "#ffb347"   # Warm wall-wash halo

# ─── Block diagram palette ────────────────────────────────────────────────────
BOX_BLUE   = "#1e3a5f"
BOX_BLUE2  = "#2a4f80"
BOX_GREEN  = "#1a2a1a"
BOX_DARK   = "#1f1a10"
BOX_PURPLE = "#2a1a3e"

ACCENT     = "#4fc3f7"   # Primary accent (ESP32, titles)
ACCENT2    = "#ce93d8"   # Secondary accent (data signals)
ACCENT_GRN = "#66bb6a"
ACCENT_YLW = "#ffd54f"
ACCENT_HA  = "#4db6ac"   # Home Assistant teal

# ─── Text colours ─────────────────────────────────────────────────────────────
TXT    = "#e8e8f0"
DIM    = "#888899"
TXT_WD = "#c8a070"   # Driftwood warm label

# ─── Schemdraw / schematic colours ───────────────────────────────────────────
SCH_BG     = "#111118"
SCH_WIRE   = "#c8d8f0"
SCH_LABEL  = "#e0e8ff"
SCH_RED    = "#ef5350"
SCH_GRN    = "#66bb6a"
SCH_YLW    = "#ffd54f"
SCH_PURPLE = "#ce93d8"
SCH_CYAN   = "#4fc3f7"

# ─── Matplotlib rcParams preset ───────────────────────────────────────────────
def apply_dark_theme():
    """Apply the project dark theme to matplotlib globally."""
    import matplotlib as mpl
    mpl.rcParams.update({
        "figure.facecolor":  BG,
        "axes.facecolor":    BG,
        "text.color":        TXT,
        "axes.labelcolor":   TXT,
        "xtick.color":       DIM,
        "ytick.color":       DIM,
        "axes.edgecolor":    BORDER,
        "grid.color":        BORDER,
        "font.family":       "monospace",
        "savefig.dpi":       160,
        "savefig.facecolor": BG,
        "savefig.bbox":      "tight",
    })
