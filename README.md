# esp-wled-projects

> DIY LED lighting projects powered by **WLED** on ESP32 / ESP8266 — fully integrated with Home Assistant.

This repository has two layers:

- the **meta main folder**, which contains the reusable project system
- the **project folders**, which contain individual lighting builds

The meta main folder is there to make new project creation repeatable instead of ad-hoc. It contains the shared `_template/` skeleton, Copilot agents and instructions under `.github/` and `AGENTS.md`, the parts register in [tools/parts-register/parts.json](./tools/parts-register/parts.json), shared generators in [tools/](./tools/), and the integration conventions for WLED, Home Assistant, diagrams, and enclosures. Together, those pieces are meant to help a project consumer move from idea to implementation faster: reuse known parts and pinouts, scaffold the right files, generate diagrams and enclosures consistently, and keep firmware, hardware, and Home Assistant artifacts aligned.

Each actual project folder is then a self-contained build with its own firmware config, wiring docs, power budget, 3D models, and generated diagrams.

## Meta Layer At A Glance

If you want to create a new project from this repo, the root-level meta layer is the part that helps you.

| Meta asset | What it contains | How it helps when creating a new project |
|------------|------------------|------------------------------------------|
| [_template/](./_template/) | Base folder skeleton | Gives every new project the same starting structure and required files |
| [tools/parts-register/parts.json](./tools/parts-register/parts.json) | Shared parts registry | Reuses known dimensions, electrical facts, and board pinouts instead of re-researching them |
| [tools/](./tools/) | Shared generators and helpers | Produces diagrams, renders enclosures, and uploads SPIFFS assets consistently |
| [.github/instructions/](./.github/instructions/) | Scoped Copilot rules | Keeps edits to firmware, hardware, diagrams, and new-project docs aligned with repo conventions |
| [.github/prompts/](./.github/prompts/) | Reusable slash-command workflows | Speeds up scaffolding, diagram generation, and enclosure generation |
| [.github/agents/](./.github/agents/) | Planner, reviewer, and hardware-debug agents | Guides planning, real-build debugging, and final coherence checks |
| [AGENTS.md](./AGENTS.md) and [.github/copilot-instructions.md](./.github/copilot-instructions.md) | Always-on repo guidance | Explains how the meta layer is supposed to be used and what rules always apply |

### How The Meta Layer Helps

1. Start from `_template/` instead of inventing a structure from scratch.
2. Use the parts register before looking up dimensions, pinouts, or PSU data again.
3. Let the planner prompt or agent drive the first pass when requirements are still forming.
4. Generate diagrams and enclosure artifacts from shared tools so outputs stay consistent across projects.
5. Use the hardware-debug agent when a physical build fails and the fault is still unclear.
6. Run the reviewer step before considering a new project scaffold or meta change complete.

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

Start with [tools/parts-register/parts.json](./tools/parts-register/parts.json) during planning so you can reuse known board, LED strip, PSU, connector, and cutout data before searching the web again.

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

### 2.5 · Review The Scaffold

When the scaffold or meta-layer update is in place, switch to the **ESP/WLED Project Reviewer** agent or use the planner's review handoff. The review step checks repo-instruction coherence, missing files, register-backed hardware facts, and whether user-facing docs match the current project state.

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

| Customization | What it does |
|-----------|-------------|
| Always-on instructions | `.github/copilot-instructions.md` — full project conventions |
| `AGENTS.md` | Root agent guidance shared across coding agents |
| `firmware.instructions.md` | Auto-loaded when editing `platformio_override.ini`, `cfg.json` |
| `hardware.instructions.md` | Auto-loaded when editing wiring / BOM / PCB files |
| `new-project.instructions.md` | Auto-loaded when editing `specs.md` or `_template/` |
| `diagram-gen.instructions.md` | Auto-loaded when editing diagram generators or `docs/` |
| `/new-project` prompt | Scaffolds a full project folder from `_template/` |
| `/gen-diagrams` prompt | Runs `tools/gen_diagrams.py` with validation |
| `/gen-enclosure` prompt | Generates YAPP_Box SCAD + renders STLs and preview PNGs |
| `ESP/WLED Project Planner` custom agent | Guided planning: requirements → LED → power → GPIO → HA → scaffold |
| `ESP/WLED Project Reviewer` custom agent | Reviews scaffold/meta coherence, upgrades docs, and checks current customization conventions |
| `ESP/WLED Realworld Hardware Debug` custom agent | Step-by-step real build triage: captures actual hardware, checks wiring/power/config assumptions, compares against project definitions, and guides the next diagnostic step |
| `enclosure-gen` skill | Reusable enclosure reference and YAPP_Box workflow support |
| `.github/hooks/README.md` | Documents the repo hook policy and recommended first deterministic hook use cases |

### How To Use The Agents

- Use **ESP/WLED Project Planner** when you are starting a new build or the requirements are still vague. Give it the project idea, LED goals, installation constraints, and Home Assistant expectations.
- Use **ESP/WLED Project Reviewer** after scaffolding or broad meta changes. It is the cleanup and coherence pass that checks missing files, instruction drift, register-backed facts, and doc completeness.
- Use **ESP/WLED Realworld Hardware Debug** when a physical setup is not working and you do not yet know whether the problem is power, wiring, GPIO choice, firmware config, part substitution, or Home Assistant. Start it with the project name and a symptom such as `reefs flickers`, `curtaincinemalights no Wi-Fi`, or `something isn't working`.
- Let the agents hand off where appropriate: planner for build definition, hardware-debug for real-world triage, reviewer for final doc and meta alignment.

### Which Doc To Read

| If you need to understand... | Read this first |
|------------------------------|-----------------|
| what this repo is and how the meta layer helps | [README.md](./README.md) |
| how an agent should behave in this repo | [AGENTS.md](./AGENTS.md) |
| the full always-on repo conventions | [.github/copilot-instructions.md](./.github/copilot-instructions.md) |
| file-specific editing rules | [.github/instructions/](./.github/instructions/) |
| the parts register schema and sourcing rules | [tools/parts-register/README.md](./tools/parts-register/README.md) |
| hook policy and whether a hook should exist at all | [.github/hooks/README.md](./.github/hooks/README.md) |

### Working In VS Code Insiders

- Run `Chat: Open Customizations` to manage prompts, instructions, skills, agents, hooks, and plugins.
- Type `/agents`, `/prompts`, `/instructions`, `/skills`, or `/hooks` in chat for quick entry to the relevant customization UI.
- Use Chat diagnostics to inspect which customizations loaded and to catch metadata issues quickly.
- If you open only a project subfolder instead of the repo root, enable `chat.useCustomizationsInParentRepositories` so these root-level customizations are discovered.
- When an agent needs input for an important choice, it should use the VS Code structured ask-question flow with suggested options and free-form input enabled.
- Prefer planner → reviewer handoffs for guided workflows; use hooks only for deterministic automation such as validation or policy enforcement.

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

---

## Included Projects

I built this repo mostly for myself as a structured workspace for planning, building, documenting, and reusing WLED-based lighting projects. The projects currently included are:

| Project | Status | LEDs | Controller | Description |
|---------|--------|------|------------|-------------|
| [reefs](./reefs/) | wip | SK6812 RGBW 60/m × 2 | ESP32-WROOM-32 | Driftwood ambient lamps, Home Assistant integrated |
| [curtaincinemalights](./curtaincinemalights/) | wip | SK6812 RGBW 60/m, ~180 LEDs · 3 m | ESP8266 D1 Mini | Cinema curtain LED sync — center-fill mirrors curtain position, State Sync + Chase + Breathe via hacs-wledext-effects |
