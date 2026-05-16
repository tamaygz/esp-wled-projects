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
│   └── spiffs/             # Files flashed to WLED LittleFS (e.g. ha-import.html)
├── hardware/
│   ├── wiring/             # KiCad schematics, wiring notes, PDFs
│   ├── pcb/                # KiCad PCB files, Gerbers
│   └── bom/                # bom.md with full power budget
├── homeassistant/          # Home Assistant config artifacts
│   ├── README.md           # Import guide with one-click blueprint badges
│   ├── package.yaml        # HA Package: helpers + scripts + automations
│   ├── lovelace.yaml       # Ready-made dashboard card YAML
│   └── blueprints/         # Project-specific automation blueprints
│       └── *.yaml          # Each blueprint importable from GitHub raw URL
├── mechanical/
│   └── enclosure/          # YAPP_Box SCAD + STLs + preview PNGs + print settings
├── design/
│   ├── led-map/            # 2D pixel maps, segment plans
│   └── effects/            # WLED presets.json, palette exports, ha-automations.yaml
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
5. Add example automations to `homeassistant/package.yaml` or `design/effects/ha-automations.yaml`

## Home Assistant Config Files

Every project must include a `homeassistant/` folder (parallel to `firmware/` and `hardware/`) containing all HA configuration artifacts.

### Required files per project

| File | Required | Purpose |
|------|----------|---------|
| `homeassistant/README.md` | Yes | Import guide with blueprint badge links and step-by-step instructions |
| `homeassistant/package.yaml` | Yes | HA Package: input_boolean/number/select helpers + scripts + automations |
| `homeassistant/lovelace.yaml` | Yes | Ready-made dashboard card YAML (paste into HA manual card editor) |
| `homeassistant/blueprints/*.yaml` | Yes (≥1) | Project-specific blueprints importable from GitHub raw URL |
| `firmware/spiffs/ha-import.html` | Yes | Device-served import assistant (JS reads /json/info, computes entity IDs) |

### Import story (no Python, no terminal required)

Three import paths — from most to least automated:

1. **Device import page** (recommended): Flash firmware + spiffs → visit `http://[wled-ip]/ha-import.html` → JS reads WLED device data, shows entity IDs, offers blueprint import links, and lets user download a pre-filled `package.yaml`.
2. **One-click blueprint import**: Click `my.home-assistant.io` badge links in `homeassistant/README.md` → HA opens its blueprint importer, user picks entities in HA UI.
3. **Manual package**: Copy `package.yaml` → HA `packages/` → edit entity ID substitution block → restart HA.

### Entity ID conventions

- WLED entity IDs in HA follow the pattern `light.{device_slug}` (master) and `light.{device_slug}_{segment_slug}` (per segment).
- `{device_slug}` is the WLED mDNS name lowercased with spaces → underscores (e.g. `reefs`).
- `{segment_slug}` is the WLED segment name lowercased with spaces → underscores (e.g. `lamp_1`).
- `ha-import.html` computes these from the live `/json/info` and `/json/state` responses — no hardcoding needed.
- `package.yaml` must have a commented substitution block at the top (see template).

### ha-import.html rules

- One file per project in `firmware/spiffs/ha-import.html`.
- Copy from `_template/firmware/spiffs/ha-import.html` and update the `PROJECT_CONFIG` block at the top.
- Fields to update: `PROJECT.name`, `PROJECT.repoBase`, `PROJECT.blueprints[]`, `PROJECT.packageFile`.
- The HTML/JS body is otherwise identical across projects — do not diverge.
- The page fetches `/json/info` and `/json/state` from the same origin (WLED device IP); works without internet for the entity ID section; needs internet to fetch `package.yaml` from GitHub.

### Blueprint rules

- One blueprint per automation pattern; file name: `{project}-{pattern}.yaml`.
- Each blueprint must include a `source_url` field pointing to its GitHub raw URL.
- Use `blueprint.input` for all entity IDs — users should never have to hand-edit blueprint YAML.
- Include `domain: automation` at blueprint level.

### package.yaml rules

- Top of file: commented block listing all entity ID substitutions needed.
- Pointer to `ha-import.html` for automatic substitution.
- Sections in order: helpers (`input_boolean`, `input_number`, `input_select`), `script`, `automation`.
- Automation `id` fields must be globally unique: use `{project}_{automation_slug}` pattern.

## Parts Register

`tools/parts-register/parts.json` is the authoritative source for component dimensions, technical metadata, and board pinout definitions used across all projects in this repo.

**Always check the register before specifying dimensions, ratings, or pin mappings in:**
- `hardware/bom/bom.md` — component footprint sizes and current budgets
- `mechanical/enclosure/*-enclosure.scad` — cutout sizes, board height, standoff positions
- `hardware/wiring/WIRING.md` — connector body dimensions and panel-mount pocket sizes

**Workflow:** check register → if not found, web-search the datasheet/product page → add a new `parts.json` entry with the relevant mechanical and technical fields (set `"verified": false` if estimated) → for boards, also add `software_identifiers` and `board_pinout` when sources exist → use register data in project files.

For boards and devkits, prefer collecting both:

- a human-facing pinout source such as an official pinout PDF/image or board page
- a machine-facing source such as a PlatformIO board manifest or Arduino/framework variant pin map

Board entries should include a structured pin definition when possible so future agents can reuse pin metadata instead of rebuilding it from scratch. Existing geometry-only entries should be backfilled when they are touched for new work.

**Key parts in the register:**

| PART_ID | Part | L × W × H (mm) | Verified |
|---------|------|-----------------|----------|
| `D1_MINI_V4` | Wemos LOLIN D1 Mini v4 | 34.2 × 25.6 × 10.0 | ✅ |
| `HLK_30M05` | Hi-Link HLK-30M05 30W 5V 6A | 57.5 × 33.6 × 22.5 | ⚠️ |
| `HLK_20M05` | Hi-Link HLK-20M05 20W 5V 4A | 56.0 × 32.0 × 22.5 | ✅ |
| `HLK_5M05` | Hi-Link HLK-5M05 5W 5V 1A | 38.0 × 23.0 × 18.0 | ✅ |
| `IC_74AHCT125_DIP14` | 74AHCT125 Quad Buffer DIP-14 | 19.05 × 6.35 × 4.57 | ✅ |
| `JST_SM_2P5_3PIN` | JST SM 2.5mm 3-pin Connector | 9.5 × 6.0 × 6.0 | ⚠️ |
| `SK6812_RGBW_60` | SK6812 RGBW LED strip 60 LED/m | 1000 × 10 × 1.5 per m | ✅ |

⚠️ = `verified: false` — dimensions estimated; confirm from datasheet before manufacturing.

See `tools/parts-register/README.md` for field definitions and instructions for adding new parts.

## Adding a New Project

1. Copy `_template/` → `<project-name>/`
2. Fill in `specs.md` first (concept, requirements, **Home Assistant** section, mechanical constraints, acceptance criteria, open questions)
3. Calculate power budget and fill `hardware/bom/bom.md`
4. Document wiring in `hardware/wiring/WIRING.md`
5. Create `gen_diagrams_config.py` from the `reefs/` example, then run `python tools/gen_diagrams.py <project-name>`
6. Generate the enclosure with the `/gen-enclosure` slash command (writes SCAD + STLs + 4 preview PNGs into `mechanical/enclosure/`)
7. Set a unique mDNS hostname in `firmware/cfg.json` (`"id": {"mdns": "<project-name>"}`, `"nw": {"mdns": 1}`) so HA auto-discovers the device
8. Create `homeassistant/` artifacts:
   - `homeassistant/package.yaml` — helpers, scripts, automations (see rules above)
   - `homeassistant/blueprints/*.yaml` — one blueprint per automation pattern
   - `homeassistant/lovelace.yaml` — dashboard card
   - `homeassistant/README.md` — import guide with badge links
   - `firmware/spiffs/ha-import.html` — update `PROJECT_CONFIG` block from template
9. Push spiffs files to the device over WiFi (works after web installer, no USB needed):
   ```
   python tools/upload_spiffs.py --project <project-name>
   ```
   Alternative (PlatformIO + USB): `pio run -t uploadfs`
10. Add a row to the Projects table in `README.md`

## Commit Convention

Use conventional commits scoped to the project or tool:

```
feat(reefs): add second lamp segment config
fix(tools): correct level-shifter pin labels in wiring.py
docs(reefs): regenerate wiring diagram after GPIO change
chore(_template): update platformio_override template
```
