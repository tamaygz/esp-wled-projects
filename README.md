# esp-wled-projects

> DIY LED lighting projects powered by **WLED** on ESP32 / ESP8266 — fully integrated with Home Assistant.

Each subfolder is a self-contained project with firmware config, wiring docs, power budget, 3D models, and generated diagrams.

---

## Projects

| Project | Status | LEDs | Controller | Description |
|---------|--------|------|------------|-------------|
| [reefs](./reefs/) | wip | SK6812 RGBW 60/m × 2 | ESP32-WROOM-32 | Driftwood ambient lamps, Home Assistant integrated |

---

## Ideal Workflow — New Project

### 1 · Plan

Use the **ESP/WLED Project Planner** agent in Copilot chat, or work through these steps manually:

| Step | What to do |
|------|-----------|
| Concept | Decide installation type, LED run length, colour capability, sound-reactive? |
| LED strip | Pick chipset (SK6812 RGBW, WS2812B RGB, WS2811 12 V) based on colour needs and run length |
| Power budget | `N_leds × 20 mA × channels` + 20 % headroom → select PSU |
| ESP32 | ESP32-WROOM-32 for most projects; ESP32-S3 for native USB / >3 buses |
| GPIO plan | Assign data lines to GPIO 16 / 17 / 18; level shifter required (3.3 V → 5 V) |
| HA effects | Decide if [hacs-wledext-effects](https://github.com/tamaygz/hacs-wledext-effects) is needed for state-driven effects |

### 2 · Scaffold

```bash
cp -r _template/ my-project/
```

Then fill in order:

1. `specs.md` — concept, requirements, acceptance criteria, **Home Assistant** section
2. `hardware/bom/bom.md` — parts list + current budget
3. `hardware/wiring/WIRING.md` — GPIO assignments, power rails, injection points
4. `gen_diagrams_config.py` — copy from `reefs/`, update values
5. `firmware/cfg.json` — set unique mDNS hostname: `"id": {"mdns": "my-project"}`

Or use the **`/new-project`** prompt in Copilot chat to scaffold automatically.

### 3 · Generate Diagrams

```bash
python tools/gen_diagrams.py my-project       # all 4 types
python tools/gen_diagrams.py my-project --type concept   # real-world views only
```

Four diagram types are produced:

| Type | Output | What it shows |
|------|--------|---------------|
| `blocks` | `concept-system.png` | System block: PSU → ESP32 → level shifter → LED strips → HA |
| `concept` | `concept-side-view.png` · `concept-top-view.png` | Real-world: wall cross-section + floor-plan with lamp positions |
| `wiring` | `wiring-physical.svg` | Color-coded physical wiring with pin labels |
| `schematic` | `schematic-*.png` | Electrical schematics (level shifter + power) |

All outputs land in `my-project/docs/` — never hand-edit them. Or use the **`/gen-diagrams`** prompt in Copilot chat.

### 4 · Generate Enclosure

Use the **`/gen-enclosure`** prompt in Copilot chat, or run the helper directly after the SCAD is in place:

```powershell
pwsh tools/render_enclosure.ps1 -Project my-project -ScadName my-project-enclosure
```

Produces `my-project/mechanical/enclosure/`:

- `my-project-base.stl`, `my-project-lid.stl` — print-ready
- `my-project-{base,lid}-{iso,top}.png` — 4 preview PNGs, committed alongside the STLs

Lid closure defaults to **snap-on** (no screws). Source of truth: [.github/skills/enclosure-gen/SKILL.md](.github/skills/enclosure-gen/SKILL.md).

### 5 · Build & Flash

```bash
# Inside the WLED repo, with firmware/platformio_override.ini alongside platformio.ini:
pio run -e esp32dev_my-project -t upload
```

First boot → connect to `wled-ap` hotspot → configure WiFi credentials via Captive Portal.

### 6 · Connect to Home Assistant

1. Enable native WLED integration: **Settings → Devices & Services → Add → WLED**
2. Device auto-discovers via mDNS (`my-project.local`)
3. Verify light entities appear and on/off / brightness / colour work
4. (Optional) Install [hacs-wledext-effects](https://github.com/tamaygz/hacs-wledext-effects) for state-driven effects

### 7 · Export & Commit

```bash
# Export config from WLED web UI → backup
# Place files in firmware/cfg.json and design/effects/presets.json
git add .
git commit -m "feat(my-project): initial project setup"
```

---

## Project Folder Convention

```
[project]/
├── firmware/               # platformio_override.ini, cfg.json, presets.json
├── hardware/
│   ├── wiring/             # KiCad schematics, wiring notes, PDFs
│   ├── pcb/                # KiCad PCB files, Gerbers
│   └── bom/                # bom.md — parts list + power budget
├── mechanical/
│   └── enclosure/          # YAPP_Box SCAD + STLs + preview PNGs + print settings
├── design/
│   ├── led-map/            # 2D pixel maps, segment plans
│   └── effects/            # WLED presets.json, palettes, ha-automations.yaml
├── docs/                   # Auto-generated diagrams (PNG/SVG) — do not hand-edit
├── gen_diagrams.py         # Diagram script — imports from tools/diagram_gen
├── gen_diagrams_config.py  # DIAGRAM_CONFIG dict for this project
└── specs.md                # Project PRD / spec sheet
```

See [_template/](./_template/) for a ready-to-copy skeleton.

---

## AI Agent Support

This repo is configured for GitHub Copilot (VS Code Insiders) and GitHub cloud agents.

| Primitive | What it does |
|-----------|-------------|
| Always-on instructions | `.github/copilot-instructions.md` — full project conventions |
| `AGENTS.md` | GitHub Copilot Coding Agent guidance (cloud) |
| `firmware.instructions.md` | Auto-loaded when editing `platformio_override.ini`, `cfg.json` |
| `hardware.instructions.md` | Auto-loaded when editing wiring / BOM / PCB files |
| `new-project.instructions.md` | Auto-loaded when editing `specs.md` or `_template/` |
| `diagram-gen.instructions.md` | Auto-loaded when editing diagram generators or `docs/` |
| `/new-project` prompt | Scaffolds a full project folder from `_template/` |
| `/gen-diagrams` prompt | Runs `tools/gen_diagrams.py` with validation |
| `/gen-enclosure` prompt | Generates YAPP_Box SCAD + renders STLs and preview PNGs |
| ESP/WLED Project Planner agent | 7-phase guided planning: LED → power → GPIO → HA → scaffold |

---

## Common Tools

| Tool | Purpose | Link |
|------|---------|------|
| WLED web installer | Flash pre-built firmware | https://install.wled.me |
| WLED custom build | Online build with usermods | https://wled-compile.github.io |
| KiCad | Schematic / PCB | https://kicad.org |
| OpenSCAD | Parametric 3D models (enclosure rendering) | https://openscad.org |
| YAPP_Box v3 | Parametric box generator (shared at `tools/yapp/`) | https://github.com/mrWheel/YAPP_Box |
| PlatformIO | Build & flash from source | https://platformio.org |
| hacs-wledext-effects | State-driven HA effects | https://github.com/tamaygz/hacs-wledext-effects |
| WLED-MM (MoonModules) | Sound-reactive fork | https://github.com/MoonModules/WLED-MM |
| LedFX | PC-based audio reactive | https://ledfx.app |

---

## Resources

- [WLED Docs](https://kno.wled.ge) — official documentation
- [WLED GitHub](https://github.com/wled/WLED)
- [r/WLED](https://reddit.com/r/WLED)
- [WLED Discord](https://discord.gg/QAh7wJHrRM)
- [QuinLED](https://quinled.info) — WLED-dedicated hardware
