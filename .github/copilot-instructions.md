# esp-wled-projects — Copilot Instructions

## Repository Overview

Mono-repo for DIY LED lighting projects powered by **WLED** on ESP32/ESP8266.
Each subdirectory (except `_template/` and `tools/`) is a self-contained project.

The repo root is also a meta layer: shared scaffolding, instructions, agents, prompts, tooling, and register-backed data live there so new project creation follows one repeatable workflow instead of becoming project-by-project improvisation.

## Active Projects

| Project | LED Strip | Controller | Description |
|---------|-----------|------------|-------------|
| `reefs/` | SK6812 RGBW 60 LED/m × 2 | ESP32-WROOM-32 | Driftwood ambient lamps, Home Assistant integrated |
| `curtaincinemalights/` | SK6812 RGBW 60 LED/m, ~180 LEDs · 3 m | ESP8266 D1 Mini | Curtain-synced cinema lighting with Home Assistant effects |

## Documentation Ownership

- `README.md` is the public-facing overview. Keep it focused on the repo concept, the meta layer, the project list, and the consumer workflow.
- `AGENTS.md` is the concise operational guide for coding agents.
- `.github/copilot-instructions.md` is the canonical always-on rule set for repo-wide behavior.
- `tools/parts-register/README.md` owns the register schema, field semantics, and sourcing workflow.
- `.github/hooks/README.md` owns hook policy and should stay focused on deterministic automation decisions.

When a workflow change affects several of these layers, update them together so the public explanation, agent behavior, and detailed policy remain coherent.

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

## VS Code Insiders Customization Guidance

- Use `.github/copilot-instructions.md` and `AGENTS.md` for always-on repo guidance.
- Use `.github/instructions/*.instructions.md` for file- or task-scoped rules with `applyTo` patterns.
- Use `.github/prompts/*.prompt.md` for repeatable slash-command workflows.
- Use `.github/agents/*.agent.md` for specialized personas with tool restrictions and optional handoffs.
- Use `.github/skills/*/SKILL.md` for reusable capabilities that may include scripts, examples, and resources.
- Use `.github/hooks/README.md` as the repo hook policy reference until concrete workspace hooks are added.
- Prefer prompts for lightweight one-shot workflows, skills for portable multi-step capabilities, and custom agents for persistent personas or constrained-tool workflows.
- In prompt and agent frontmatter, prefer current VS Code tool identifiers and tool sets such as `read`, `search`, `edit`, `terminal`, and `agent` instead of environment-specific helper names.
- Prefer handoffs for guided, user-controlled phase changes such as planning → review. Use them to suggest the next best step without forcing the workflow forward automatically.
- Prefer subagents only when isolated research, parallel analysis, or multi-perspective review genuinely improves focus. Keep coordinator instructions explicit about when delegation is allowed.
- Use hooks only for deterministic automation or guardrails, such as validation, formatting, or blocking unsafe tool usage. Do not use hooks for fuzzy decision-making or to replace user collaboration.
- Keep customizations concise, use Markdown links instead of duplicating rules, and align file metadata with current VS Code Insiders conventions.
- Use the Agent Customizations editor (`Chat: Open Customizations`) to manage these files and the Chat diagnostics view to troubleshoot loading problems.
- If a contributor opens only a subfolder of this repo, enable `chat.useCustomizationsInParentRepositories` so the root customizations are discovered.

## Workflow Design

- Keep the main repo workflow intuitive: plan with the planner agent, then hand off to a reviewer agent before considering the scaffold or meta-layer update complete.
- For public-facing repo changes, make sure `README.md` explains the user-visible story while `AGENTS.md` and this file carry the operational detail.
- When adding future agents, prefer a coordinator-and-reviewer structure over many overlapping general-purpose agents.
- If a future agent should only be used internally, mark it `user-invocable: false`. If it should not be auto-selected as a subagent, use `disable-model-invocation: true` unless an explicit coordinator needs it.
- If future prompt files need isolated research or parallel checks, include agent/subagent tooling intentionally rather than assuming broad delegation.

## Hooks Guidance

- Workspace hooks belong in `.github/hooks/*.json`.
- Start with low-risk events such as `SessionStart`, `PreToolUse`, or `PostToolUse` only when there is a clear deterministic benefit.
- Keep hook commands cross-platform where possible, or provide OS-specific commands.
- Validate and sanitize all hook inputs, avoid secrets in hook configs, and do not let the agent freely rewrite hook scripts without user review.
- Good future candidates in this repo are policy checks that protect generated outputs or block unsafe edits; poor candidates are interactive planning choices, prose generation, or anything that should stay user-directed.

## User Collaboration

- When key requirements or tradeoffs are unclear, use the VS Code ask-question tool instead of asking only in free-form chat.
- Always provide a short list of sensible options and keep free-form input enabled so the user can choose or supply a different answer.
- Use structured questions especially for project planning choices such as LED family, controller board, PSU strategy, Home Assistant integration level, enclosure style, and whether to scaffold files immediately.
- When the task is a meta-layer documentation update, check whether the same change also affects `README.md`, `AGENTS.md`, `.github/hooks/README.md`, or `tools/parts-register/README.md` before stopping.

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

Use it during planning as well as implementation. It should be the first stop for recurring part questions about controller boards, LED strips, PSUs, level shifters, connectors, and cutout-driving components.

**Always check the register before specifying dimensions, ratings, or pin mappings in:**
- `hardware/bom/bom.md` — component footprint sizes and current budgets
- `mechanical/enclosure/*-enclosure.scad` — cutout sizes, board height, standoff positions
- `hardware/wiring/WIRING.md` — connector body dimensions and panel-mount pocket sizes

**Workflow:** check register → if not found, web-search the datasheet/product page → add a new `parts.json` entry with the relevant mechanical and technical fields (set `"verified": false` if estimated) → for boards, also add `software_identifiers` and `board_pinout` when sources exist → use register data in project files.

For boards and devkits, prefer collecting both:

- a human-facing pinout source such as an official pinout PDF/image or board page
- a machine-facing source such as a PlatformIO board manifest or Arduino/framework variant pin map

Board entries should include a structured pin definition when possible so future agents can reuse pin metadata instead of rebuilding it from scratch. Existing geometry-only entries should be backfilled when they are touched for new work.

When creating or updating user-facing project docs:

- prefer register-backed facts over freehand summaries in `README.md`, `specs.md`, `hardware/bom/bom.md`, and `hardware/wiring/WIRING.md`
- link to a part's `source_url` when the register provides one and the part appears in a summary table or hardware overview
- if a board entry provides `board_pinout.image_url` or `board_pinout.image_path`, include a preview or direct link in the project README or spec when it materially improves comprehension
- cite `PART_ID`s in tables or prose when that helps future maintenance

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
2. Check `tools/parts-register/parts.json` for the selected controller, LED strip, PSU, level shifter, connectors, and enclosure-driving parts; add missing entries before those parts appear in project docs
3. Fill in `specs.md` first (concept, requirements, **Home Assistant** section, mechanical constraints, acceptance criteria, open questions)
4. Calculate power budget and fill `hardware/bom/bom.md`
5. Document wiring in `hardware/wiring/WIRING.md`
6. Create `gen_diagrams_config.py` from the `reefs/` example, then run `python tools/gen_diagrams.py <project-name>`
7. Generate the enclosure with the `/gen-enclosure` slash command (writes SCAD + STLs + 4 preview PNGs into `mechanical/enclosure/`)
8. Set a unique mDNS hostname in `firmware/cfg.json` (`"id": {"mdns": "<project-name>"}`, `"nw": {"mdns": 1}`) so HA auto-discovers the device
9. Create `homeassistant/` artifacts:
   - `homeassistant/package.yaml` — helpers, scripts, automations (see rules above)
   - `homeassistant/blueprints/*.yaml` — one blueprint per automation pattern
   - `homeassistant/lovelace.yaml` — dashboard card
   - `homeassistant/README.md` — import guide with badge links
   - `firmware/spiffs/ha-import.html` — update `PROJECT_CONFIG` block from template
10. In project-facing docs, include a compact hardware summary sourced from the parts register, with `source_url` links and board pinout previews when available
11. Push spiffs files to the device over WiFi (works after web installer, no USB needed):
   ```
   python tools/upload_spiffs.py --project <project-name>
   ```
   Alternative (PlatformIO + USB): `pio run -t uploadfs`
12. Add a row to the Projects table in `README.md`

## Commit Convention

Use conventional commits scoped to the project or tool:

```
feat(reefs): add second lamp segment config
fix(tools): correct level-shifter pin labels in wiring.py
docs(reefs): regenerate wiring diagram after GPIO change
chore(_template): update platformio_override template
```
