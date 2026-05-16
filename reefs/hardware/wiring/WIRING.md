# Wiring Notes — Reefs

> Source of truth: `specs.md` §8.4 and the generated diagrams in `docs/`.

## Generated Diagrams

| Diagram | File | Description |
|---------|------|-------------|
| Physical wiring | [`docs/wiring-physical.svg`](../../docs/wiring-physical.svg) | ESP32 → level shifter → JST → strips |
| Level shifter circuit | [`docs/schematic-level-shifter.png`](../../docs/schematic-level-shifter.png) | 74AHCT125 2-channel schematic |
| Power circuit | [`docs/schematic-power.png`](../../docs/schematic-power.png) | Mains → fuse → PSU → per-lamp fuses |
| System block | [`docs/concept-system.png`](../../docs/concept-system.png) | High-level signal and power flow |

Regenerate all diagrams: `python tools/gen_diagrams.py reefs` (from repo root).

---

## Control Box Internal Wiring

```
Schuko captive lead (H05VV-F 3×0.75 mm², CEE 7/7 plug)
  enters via Ø8 mm back-wall hole; outer jacket clamped
  by 3D-printed 2× M3 cable clamp immediately inside.
  ├── Live (brown)    ──▶ PSU L screw terminal
  ├── Neutral (blue)  ──▶ PSU N screw terminal
  └── Earth (gn/yel)  ──▶ PSU PE screw terminal

PSU +5V ──▶ Pluggable terminal V+ pin
PSU GND ──▶ Pluggable terminal GND pin
             (3-pos Phoenix-style; 5.08 mm pitch; screw-clamp plug)

V+ bus  ──[5A fuse]──▶ JST Lamp 1 Pin 1 (+5V)
GND bus ────────────▶ JST Lamp 1 Pin 2 (GND)
V+ bus  ──[5A fuse]──▶ JST Lamp 2 Pin 1 (+5V)
GND bus ────────────▶ JST Lamp 2 Pin 2 (GND)

ESP32 GPIO16 ──[330Ω]──▶ 74AHCT125 Channel A IN
                         74AHCT125 Channel A OUT ──▶ JST Lamp 1 Pin 3 (DATA)

ESP32 GPIO17 ──[330Ω]──▶ 74AHCT125 Channel B IN
                         74AHCT125 Channel B OUT ──▶ JST Lamp 2 Pin 3 (DATA)

74AHCT125 VCC ──▶ V+ bus (5V)
74AHCT125 GND ──▶ GND bus
74AHCT125 nOE ──▶ GND (always enabled)

ESP32 5V (Vin) ──▶ V+ bus
ESP32 GND      ──▶ GND bus
```

### Connector / Cable Entry Detail

| Penetration | Wall | Hole | Strain relief |
|---|---|---|---|
| Mains AC | Back | Ø8 mm round | 3D-printed 2-screw cable clamp (M3 inserts) on jacket |
| Lamp 1 output | Left | Rectangular pocket ~9.5 × 6 mm + internal shoulder | Female JST SM body trapped by pocket; zip-tie on cable inside |
| Lamp 2 output | Right | Rectangular pocket ~9.5 × 6 mm + internal shoulder | Female JST SM body trapped by pocket; zip-tie on cable inside |
| USB-C OTA | Front | 12 × 8 mm slot | n/a (passive cable access) |

## Lamp Cable (per lamp, 2 m run)

```
Male JST Pin 1 (18 AWG red)   ──▶ LED strip +5V pad
Male JST Pin 2 (18 AWG black) ──▶ LED strip GND pad
Male JST Pin 3 (26 AWG white) ──▶ LED strip DIN pad
```

Male plug on lamp end; mates with **panel-mounted female JST SM** on the box wall.
JST SM rated 3 A/contact — set WLED ABL to **2800 mA per output** to stay within spec at worst-case full white.

> Keep data wire physically separate from the power pair (space ≥ 5 mm or twist) to minimise EMI coupling.

---

## GPIO Assignments

| GPIO | Function | Notes |
|------|----------|-------|
| 16 | LED Data — Lamp 1 | Via 330 Ω series + 74AHCT125 level shifter |
| 17 | LED Data — Lamp 2 | Via 330 Ω series + 74AHCT125 level shifter |
| 0 | Boot mode strapping | Do not connect to LED data |
| 2 | Onboard LED (status) | Leave free |
| EN | Reset | Accessible via enclosure reset hole |

> Avoid GPIO 0, 2, 12, 15 for LED data — these are strapping pins affecting boot mode.

---

## WLED Top 5 Wiring Mistakes

1. **No 300–500 Ω resistor** on data line → signal reflections / flickering.
2. **Missing common GND** between ESP and strip → erratic/no data.
3. **3.3 V data direct** to 5 V SK6812 strip → marginal logic level; always use level shifter.
4. **No 1000 µF cap** on PSU rail → voltage dip on colour change (consider adding near strip).
5. **Long data line** > 50 cm before level shifter → bit errors at high update rates.

---

## Schematic Source Files

> KiCad project files are not yet created for this project. Generated diagrams (SVG/PNG) are in `docs/` and are the primary visual reference.
>
> If a KiCad schematic is added later, place it here as:
> - `hardware/wiring/reefs.kicad_sch`
> - `hardware/wiring/reefs-wiring.pdf` (exported)
