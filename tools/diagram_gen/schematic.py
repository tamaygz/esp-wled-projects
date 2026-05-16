"""
schematic.py — Electrical circuit schematics using schemdraw.

Provides ready-made schematic generators for common WLED project circuits:

    draw_level_shifter_circuit(out_path)
        74AHCT125 level-shifter schematic (3.3V → 5V, 2-channel)
        Suitable for any ESP32 + SK6812/WS2812B project that needs level shifting.

    draw_power_circuit(out_path)
        5V PSU → terminal block → fuses → LED strip power injection points.
"""

from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")
import schemdraw
import schemdraw.elements as elm
from . import style


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _dark_drawing(w: float = 12, h: float = 7, title: str = "") -> schemdraw.Drawing:
    """Return a schemdraw Drawing pre-configured for the dark theme."""
    import matplotlib.pyplot as plt
    style.apply_dark_theme()
    fig, ax = plt.subplots(figsize=(w, h), facecolor=style.SCH_BG)
    ax.set_facecolor(style.SCH_BG)
    if title:
        ax.set_title(title, color=style.TXT, fontsize=11, pad=10,
                     fontfamily="monospace", fontweight="bold")
    return schemdraw.Drawing(canvas=ax)


# ─── Level Shifter ────────────────────────────────────────────────────────────

def draw_level_shifter_circuit(out_path: str) -> None:
    """
    Generate a 2-channel 74AHCT125 level-shifter schematic.

    Layout
    ------
    ESP32 GPIO16 ──[330Ω]──► 74AHCT125-1A ──► 1Y ──► LED1 DATA (5V)
    ESP32 GPIO17 ──[330Ω]──► 74AHCT125-2A ──► 2Y ──► LED2 DATA (5V)
    1OE, 2OE → GND  (active-low, always enabled)
    VCC → 5V,  GND → GND

    Saves a PNG to *out_path*.
    """
    import matplotlib.pyplot as plt
    style.apply_dark_theme()

    fig, ax = plt.subplots(figsize=(14, 9), facecolor=style.SCH_BG)
    ax.set_facecolor(style.SCH_BG)
    ax.set_title("Level-Shifter Circuit  –  74AHCT125  (3.3 V → 5 V, 2 ch)",
                 color=style.TXT, fontsize=11, pad=8,
                 fontfamily="monospace", fontweight="bold")

    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(fontsize=10, color=style.SCH_WIRE, lw=1.6)

        # ── IC box ────────────────────────────────────────────────────────────
        ic = d.add(elm.Ic(
            pins=[
                elm.IcPin(name="1~OE",  side="left",   pin="1",  anchorname="oe1"),
                elm.IcPin(name="1A",    side="left",   pin="2",  anchorname="a1"),
                elm.IcPin(name="2~OE",  side="left",   pin="4",  anchorname="oe2"),
                elm.IcPin(name="2A",    side="left",   pin="5",  anchorname="a2"),
                elm.IcPin(name="GND",   side="bot",    pin="7",  anchorname="gnd"),
                elm.IcPin(name="VCC",   side="top",    pin="14", anchorname="vcc"),
                elm.IcPin(name="1Y",    side="right",  pin="3",  anchorname="y1"),
                elm.IcPin(name="2Y",    side="right",  pin="6",  anchorname="y2"),
            ],
            edgepadW=1.0,
            edgepadH=1.2,
            pinspacing=1.5,
            label="74AHCT125\nLevel Shifter",
            lblcolor=style.SCH_LABEL,
        ).at((5, 3)))

        # ── Channel 1: GPIO16 → R1 → 1A ───────────────────────────────────────
        d.add(elm.Line().left(2.0).at(ic.oe1).color(style.SCH_WIRE))
        d.add(elm.Ground().color(style.SCH_WIRE))

        r1 = d.add(elm.Resistor().left(3.5).at(ic.a1)
                   .label("R1\n330 Ω", loc="top").color(style.SCH_YLW))
        d.add(elm.Dot(radius=0.06).color(style.SCH_YLW))
        d.add(elm.Label().at(r1.end).label("GPIO 16\n(ESP32)", loc="left")
              .color(style.SCH_CYAN))

        # ── Channel 2: GPIO17 → R2 → 2A ───────────────────────────────────────
        d.add(elm.Line().left(2.0).at(ic.oe2).color(style.SCH_WIRE))
        d.add(elm.Ground().color(style.SCH_WIRE))

        r2 = d.add(elm.Resistor().left(3.5).at(ic.a2)
                   .label("R2\n330 Ω", loc="top").color(style.SCH_YLW))
        d.add(elm.Dot(radius=0.06).color(style.SCH_YLW))
        d.add(elm.Label().at(r2.end).label("GPIO 17\n(ESP32)", loc="left")
              .color(style.SCH_CYAN))

        # ── Channel 1 output: 1Y → LED1 DATA ─────────────────────────────────
        d.add(elm.Line().right(3.0).at(ic.y1).color(style.SCH_GRN))
        d.add(elm.Dot(radius=0.06).color(style.SCH_GRN))
        d.add(elm.Label().label("LAMP 1\nDATA (5V)", loc="right")
              .color(style.SCH_GRN))

        # ── Channel 2 output: 2Y → LED2 DATA ─────────────────────────────────
        d.add(elm.Line().right(3.0).at(ic.y2).color(style.SCH_GRN))
        d.add(elm.Dot(radius=0.06).color(style.SCH_GRN))
        d.add(elm.Label().label("LAMP 2\nDATA (5V)", loc="right")
              .color(style.SCH_GRN))

        # ── Power rails ────────────────────────────────────────────────────────
        d.add(elm.Line().up(1.0).at(ic.vcc).color(style.SCH_RED))
        d.add(elm.Label().label("+5 V", loc="top").color(style.SCH_RED))

        d.add(elm.Line().down(1.0).at(ic.gnd).color(style.SCH_WIRE))
        d.add(elm.Ground().color(style.SCH_WIRE))

    # Annotations outside schemdraw drawing
    ax.text(0.02, 0.04,
            "Notes: 330 Ω series resistors protect ESP32 GPIOs.\n"
            "nOE pins tied LOW — buffers always active.\n"
            "V_IH(SK6812) = 3.5 V min; ESP32 outputs 3.3 V — level shift required.",
            transform=ax.transAxes,
            color=style.DIM, fontsize=8, fontfamily="monospace",
            verticalalignment="bottom")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig.savefig(out_path, facecolor=style.SCH_BG, bbox_inches="tight")
    plt.close(fig)
    print(f"  schematic: {os.path.basename(out_path)} ✓")


# ─── Power Circuit ────────────────────────────────────────────────────────────

def draw_power_circuit(out_path: str) -> None:
    """
    Generate a power distribution schematic:
    IEC C14 → fuse → terminal block → PSU → per-lamp fuse → LED strip.
    """
    import matplotlib.pyplot as plt
    style.apply_dark_theme()

    fig, ax = plt.subplots(figsize=(14, 6), facecolor=style.SCH_BG)
    ax.set_facecolor(style.SCH_BG)
    ax.set_title("Power Distribution  –  230 V AC → 5 V DC → LED Strips",
                 color=style.TXT, fontsize=11, pad=8,
                 fontfamily="monospace", fontweight="bold")

    with schemdraw.Drawing(canvas=ax, show=False) as d:
        d.config(fontsize=10, color=style.SCH_WIRE, lw=1.6)

        # AC mains source
        src = d.add(elm.SourceV().up(3)
                    .label("230 V AC\nMains", loc="left")
                    .color(style.SCH_RED))

        # Slow-blow fuse on live rail
        d.add(elm.Fuse().right(3)
              .label("F1  2A\nSlow-blow", loc="top")
              .color(style.SCH_YLW))

        # IEC C14 inlet (represented as a labelled line segment)
        d.add(elm.Line().right(1.5)
              .label("IEC C14\nInlet", loc="top")
              .color(style.SCH_WIRE))

        # PSU block (placed at current drawing position via .at())
        cur = d.here
        psu = d.add(elm.Ic(
            pins=[
                elm.IcPin(name="L/N",  side="left",  pin="1", anchorname="ac_in"),
                elm.IcPin(name="+5V",  side="right", pin="2", anchorname="vout"),
                elm.IcPin(name="GND",  side="right", pin="3", anchorname="gnd_out"),
            ],
            edgepadW=0.8, edgepadH=0.6, pinspacing=1.2,
            label="Honeywell PSU\n5V / 10A",
            lblcolor=style.SCH_LABEL,
        ).at(cur))

        # +5V rail → fuse junction
        d.add(elm.Line().right(1.5).at(psu.vout).color(style.SCH_RED))
        jct = d.add(elm.Dot().color(style.SCH_RED))

        # Lamp 1 branch
        d.add(elm.Fuse().right(2.5).at(jct.end)
              .label("F2  5A", loc="top")
              .color(style.SCH_YLW))
        d.add(elm.Label().label("LAMP 1\n+5 V rail", loc="right")
              .color(style.SCH_GRN))

        # Lamp 2 branch (drops down then right)
        d.add(elm.Line().down(2.0).at(jct.end).color(style.SCH_RED))
        d.add(elm.Fuse().right(2.5)
              .label("F3  5A", loc="top")
              .color(style.SCH_YLW))
        d.add(elm.Label().label("LAMP 2\n+5 V rail", loc="right")
              .color(style.SCH_GRN))

        # GND return path
        d.add(elm.Line().down(2.0).at(psu.gnd_out).color(style.WIRE_BLK))
        d.add(elm.Ground().color(style.SCH_WIRE))

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig.savefig(out_path, facecolor=style.SCH_BG, bbox_inches="tight")
    plt.close(fig)
    print(f"  schematic: {os.path.basename(out_path)} ✓")
