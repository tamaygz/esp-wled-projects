# [Project Name]

> One-line description of the lighting project.

## Quick Facts

| Property | Value |
|---|---|
| **Board** | ESP32-DevKit / WLED-compatible |
| **LED Type** | WS2812B / SK6812 / APA102 / … |
| **LED Count** | — |
| **Power Supply** | — |
| **WLED Version** | — |
| **Usermods** | — |

## Structure

```
[project]/
├── firmware/                 # WLED build: platformio_override.ini, cfg.json, presets.json
├── hardware/
│   ├── wiring/               # Fritzing .fzz, KiCad .kicad_sch, PDFs, PNGs
│   ├── pcb/                  # KiCad .kicad_pcb, Gerbers, drill files
│   └── bom/                  # BOM CSV / Excel, LCSC part IDs
├── mechanical/
│   ├── 3d-models/            # STL / STEP / F3D source files
│   ├── enclosure/            # Housing STLs, print settings (.3mf)
│   └── mounting/             # Brackets, clips, diffusers
├── design/
│   ├── led-map/              # 2D pixel maps, LED layout sketches
│   ├── effects/              # Effect ideas, palette exports, preset JSON
│   └── references/           # Mood boards, inspiration images
├── docs/
│   ├── photos/               # Build progress photos
│   ├── videos/               # Demo links or local .mp4
│   └── notes.md              # Lessons learned, quirks, config notes
└── specs.md                  # This project's spec sheet
```

## Wiring Notes

- Data line: **470Ω resistor** in series, ≤ 50 cm from controller to strip.
- Power injection: every **~50 LEDs** (WS2812B @ 5V, full white = ~60 mA/LED).
- Decoupling: **1000 µF** cap across PSU rails on controller board.
- Ground the ESP and LED strip together.

## Build

```bash
# Flash WLED binary
pio run -e esp32dev --target upload

# or use WLED web installer
# https://install.wled.me
```

## Resources

- [WLED Docs](https://kno.wled.ge)
- [WLED GitHub](https://github.com/wled/WLED)
- [WLED Discord](https://discord.gg/QAh7wJHrRM)
