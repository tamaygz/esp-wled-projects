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
│   └── enclosure/          # YAPP_Box SCAD + STLs + preview PNGs + print settings
├── design/
│   ├── led-map/            # 2D pixel maps, segment plans
│   └── effects/            # WLED presets.json, palette exports
├── docs/                   # Auto-generated diagrams (PNG/SVG) — never hand-edit
├── gen_diagrams.py         # Project diagram script — imports from tools/diagram_gen
├── gen_diagrams_config.py  # DIAGRAM_CONFIG dict for this project
└── specs.md                # Project PRD / spec sheet
```

## Tech Stack

- **Firmware**: WLED v16.0+ on ESP32-WROOM-32 (primary target); ESP8266 (legacy, v0.15 branch)
- **LED strips**: SK6812 RGBW 5 V (preferred), WS2812B RGB 5 V, WS2811 12 V
- **Build system**: PlatformIO — each project provides `firmware/platformio_override.ini`
- **Diagrams**: Python 3 via `tools/diagram_gen/` (schemdraw ≥ 0.22, matplotlib, drawsvg ≥ 2.4)
- **Enclosures**: OpenSCAD + [YAPP_Box v3](https://github.com/mrWheel/YAPP_Box) (MIT) at `tools/yapp/YAPPgenerator_v3.scad`, rendered via `tools/render_enclosure.ps1`
- **Schematics / PCB**: KiCad
- **3D printing**: PETG / ASA enclosures — STLs and 4 preview PNGs committed per project
- **Smart home**: Home Assistant via native WLED integration (no MQTT required) — **mandatory for every project**
- **Extended HA effects**: [hacs-wledext-effects](https://github.com/tamaygz/hacs-wledext-effects) — context-aware LED effects driven by HA state (use when applicable, see rules below)

## Shared Tooling Rules

- All diagram generation logic lives in `tools/diagram_gen/`. **Never copy modules into project folders.**
- The YAPP_Box library lives at `tools/yapp/YAPPgenerator_v3.scad`. **Never copy it into a project folder** — project SCAD files include it via the relative path `../../../tools/yapp/YAPPgenerator_v3.scad`.
- The enclosure render helper is `tools/render_enclosure.ps1` — it produces both shells and 4 preview PNGs. Use the [`enclosure-gen` skill](skills/enclosure-gen/SKILL.md) as the API reference and invoke it via the `/gen-enclosure` slash command.
- Project-level `gen_diagrams.py` scripts import the shared package via a `sys.path` insert — follow the exact pattern in `reefs/gen_diagrams.py`.
- `gen_diagrams_config.py` in each project exports a single `DIAGRAM_CONFIG` dict. Copy `reefs/gen_diagrams_config.py` as the starting point.
- `docs/` in each project is output-only; the sources are the Python scripts.

Run diagrams from repo root:
```bash
python tools/gen_diagrams.py <project>                  # all 4 types
python tools/gen_diagrams.py <project> --type concept   # real-world visualisation only
python tools/gen_diagrams.py <project> --type wiring    # physical wiring only
python tools/gen_diagrams.py <project> --type blocks    # system block diagram only
python tools/gen_diagrams.py <project> --type schematic # electrical schematics only
```

Four diagram types and their outputs:

| `--type` | Output files | What it shows |
|----------|-------------|---------------|
| `blocks` | `concept-system.png` | PSU → ESP32 → level shifter → LED strips → HA block diagram |
| `concept` | `concept-side-view.png`, `concept-top-view.png` | Real-world visualisation: wall cross-section and top-down floor plan |
| `wiring` | `wiring-physical.svg` (+ `.png`) | Color-coded physical wiring with pin labels |
| `schematic` | `schematic-level-shifter.png`, `schematic-power.png` | Electrical schematics |

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

## Home Assistant Integration Rules

Every WLED project in this repo **must** be controllable from Home Assistant.

- Enable the **native WLED integration** in HA (Settings → Devices & Services → Add → WLED). Auto-discovers via mDNS — ensure mDNS is enabled in WLED (`cfg.json: "nw": {"mdns": 1}`).
- No MQTT required. Do not configure MQTT unless there is an explicit reason.
- Each project's `firmware/cfg.json` must have a human-readable device name (`"id": {"mdns": "<project-name>"}`) so HA auto-discovers the correct device.
- Document the expected HA entity IDs (light, switch, sensor) in the project's `specs.md` under a **"Home Assistant"** section.
- Test HA control (on/off, brightness, color) before a project is considered complete.

## hacs-wledext-effects

[hacs-wledext-effects](https://github.com/tamaygz/hacs-wledext-effects) is a HACS custom integration that adds context-aware, HA-state-driven LED effects on top of the native WLED integration.

### What it provides

| Effect | Use case |
|--------|----------|
| Rainbow Wave | Decoration, ambient lighting |
| Segment Fade | Mood lighting, transitions |
| Loading | Progress indicators |
| State Sync | Map any sensor value → LED color/fill |
| Breathe | Notifications, soft alerts |
| Meter | CPU, battery, temperature gauges |
| Sparkle | Activity indicators |
| Chase | Processing, retro scanner |
| Alert | Security / multi-severity warnings |

Each effect creates Switch, Number, Select, Sensor, and Button entities in HA and can be driven by automations.

### When to use it

**Use hacs-wledext-effects when:**
- A LED strip should visualize a HA sensor value (temperature, CPU, humidity, energy) in real-time.
- You need notification-style alerts triggered by HA events (motion, door open, security alarm).
- You want HA automations to control the *behaviour* of an effect (e.g. pulse rate driven by notification priority).
- Multi-zone display of independent data channels on a single strip.
- Any effect logic that would otherwise require a complex WLED preset + HA script combination.

**Do NOT use it when:**
- A static WLED preset or palette is sufficient.
- The effect is purely decorative with no relationship to HA state.
- The device is deployed without a Home Assistant instance.

### Requirements
- Home Assistant ≥ 2024.1.0
- Native WLED integration already installed and device discovered in HA
- WLED firmware ≥ 0.14.0 (WLED v16+ used in this repo satisfies this)

### Installation checklist (per project)
1. Add HACS custom repository `https://github.com/tamaygz/hacs-wledext-effects` (category: Integration)
2. Install "WLED Effects" from HACS, restart HA
3. Add Integration: Settings → Devices & Services → Add → "WLED Effects", select your WLED device
4. Document installed effects and their entity IDs in `specs.md` → **"Home Assistant"** section
5. Add example automations to a `design/effects/ha-automations.yaml` file in the project

## Adding a New Project

1. Copy `_template/` → `<project-name>/`
2. Fill in `specs.md` first (concept, requirements, **Home Assistant** section, mechanical constraints, acceptance criteria, open questions)
3. Calculate power budget and fill `hardware/bom/bom.md`
4. Document wiring in `hardware/wiring/WIRING.md`
5. Create `gen_diagrams_config.py` from the `reefs/` example, then run `python tools/gen_diagrams.py <project-name>`
6. Generate the enclosure with the `/gen-enclosure` slash command (writes SCAD + STLs + 4 preview PNGs into `mechanical/enclosure/`)
7. Set a unique mDNS hostname in `firmware/cfg.json` (`"id": {"mdns": "<project-name>"}`, `"nw": {"mdns": 1}`) so HA auto-discovers the device
8. Add a row to the Projects table in `README.md`

## Commit Convention

Use conventional commits scoped to the project or tool:

```
feat(reefs): add second lamp segment config
fix(tools): correct level-shifter pin labels in wiring.py
docs(reefs): regenerate wiring diagram after GPIO change
chore(_template): update platformio_override template
```
