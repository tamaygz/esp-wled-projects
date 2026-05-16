# esp-wled-projects — Copilot Instructions

## Repository Overview

Mono-repo for DIY LED lighting projects powered by **WLED** on ESP32/ESP8266.
Each subdirectory (except `_template/` and `tools/`) is a self-contained project.

## Active Projects

| Project | LED Strip | Controller | Description |
|---------|-----------|------------|-------------|
| `reefs/` | SK6812 RGBW 60 LED/m × 2 | ESP32-WROOM-32 | Driftwood ambient lamps, Home Assistant integrated |

## Project Folder Convention

Every project mirrors the `_template/` skeleton:

```
[project]/
├── firmware/               # platformio_override.ini, cfg.json, presets.json
├── hardware/
│   ├── wiring/             # KiCad schematics, wiring notes, PDFs
│   ├── pcb/                # KiCad PCB files, Gerbers
│   └── bom/                # bom.md with full power budget
├── mechanical/
│   ├── 3d-models/          # STL / STEP / .3mf files
│   └── enclosure/          # Housing files, print settings
├── design/
│   ├── led-map/            # 2D pixel maps, segment plans
│   └── effects/            # WLED presets.json, palette exports
├── docs/                   # Auto-generated diagrams (PNG/SVG) — never hand-edit
├── gen_diagrams.py         # Project diagram script — imports from tools/diagram_gen
├── gen_diagrams_config.py  # DIAGRAM_CONFIG dict for this project
└── specs.md                # Project PRD / spec sheet
```

## Tech Stack

- **Firmware**: WLED v0.15+ on ESP32-WROOM-32 (primary target); ESP8266 (legacy)
- **LED strips**: SK6812 RGBW 5 V (preferred), WS2812B RGB 5 V, WS2811 12 V
- **Build system**: PlatformIO — each project provides `firmware/platformio_override.ini`
- **Diagrams**: Python 3 via `tools/diagram_gen/` (schemdraw ≥ 0.22, matplotlib, drawsvg ≥ 2.4)
- **Schematics / PCB**: KiCad
- **3D printing**: PETG / ASA enclosures in `.3mf`, `.stl`, `.step`
- **Smart home**: Home Assistant via native WLED integration (no MQTT required)

## Shared Tooling Rules

- All diagram generation logic lives in `tools/diagram_gen/`. **Never copy modules into project folders.**
- Project-level `gen_diagrams.py` scripts import the shared package via a `sys.path` insert — follow the exact pattern in `reefs/gen_diagrams.py`.
- `gen_diagrams_config.py` in each project exports a single `DIAGRAM_CONFIG` dict. Copy `reefs/gen_diagrams_config.py` as the starting point.
- `docs/` in each project is output-only; the sources are the Python scripts.

Run diagrams from repo root:
```bash
python tools/gen_diagrams.py <project>               # all diagram types
python tools/gen_diagrams.py <project> --type wiring # single type
```

## Hardware Rules

- ESP32 GPIO outputs are 3.3 V. Always use a **level shifter** (74AHCT125 or SN74HCT245) before any 5 V LED data line.
- Inject power every ≤ 50 LEDs on strips longer than 1 m (prevents voltage drop sag).
- Common GND between the PSU 5 V rail and ESP32 GND — must be wired explicitly.
- Calculate full current budget in `hardware/bom/bom.md` before ordering parts.
  Formula: `N_leds × mA_per_channel × channels` (use 20 mA/channel for RGBW at full white).

## Firmware Rules

- **Never commit WiFi credentials.** Configure station SSID/password via WLED Captive Portal or web UI after first flash.
- All persistent WLED runtime config goes in `firmware/cfg.json` and `firmware/presets.json` (export from WLED UI).
- Build-time overrides go in `platformio_override.ini` only — do not modify WLED upstream source files.
- Usermods are declared in `custom_usermods` inside `platformio_override.ini`.

## Adding a New Project

1. Copy `_template/` → `<project-name>/`
2. Fill in `specs.md` first (concept, requirements, acceptance criteria, open questions)
3. Calculate power budget and fill `hardware/bom/bom.md`
4. Document wiring in `hardware/wiring/WIRING.md`
5. Create `gen_diagrams_config.py` from the `reefs/` example
6. Add a row to the Projects table in `README.md`

## Commit Convention

Use conventional commits scoped to the project or tool:

```
feat(reefs): add second lamp segment config
fix(tools): correct level-shifter pin labels in wiring.py
docs(reefs): regenerate wiring diagram after GPIO change
chore(_template): update platformio_override template
```
