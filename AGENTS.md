# AGENTS.md — esp-wled-projects

This file provides guidance for GitHub Copilot Coding Agent and other AI agents operating on this repository. See `.github/copilot-instructions.md` for full project conventions.

## Repository Purpose

Mono-repo for DIY LED lighting projects powered by **WLED** on ESP32/ESP8266. Each subdirectory is a self-contained project with firmware, hardware docs, mechanical designs, and generated diagrams.

## Repository Map

| Path | Purpose |
|------|---------|
| `_template/` | Copy-paste skeleton for every new project |
| `tools/diagram_gen/` | Shared Python library for generating all project diagrams |
| `tools/gen_diagrams.py` | CLI runner: `python tools/gen_diagrams.py <project>` |
| `tools/yapp/YAPPgenerator_v3.scad` | Shared YAPP_Box library (MIT) — included by every project SCAD |
| `tools/render_enclosure.ps1` | One-shot helper: renders base + lid STLs + 4 preview PNGs |
| `tools/upload_spiffs.py` | WiFi file push: uploads `firmware/spiffs/` files to a live WLED device over HTTP (no USB needed) |
| `reefs/` | Active project — driftwood ambient lamps (SK6812 RGBW, ESP32, Home Assistant) |
| `reefs/homeassistant/` | HA package, blueprints, lovelace card, import guide |
| `reefs/firmware/spiffs/ha-import.html` | Device-served HA import assistant page |
| `.github/instructions/` | Scoped Copilot instruction files |
| `.github/prompts/` | Reusable prompt templates (incl. `/gen-enclosure`, `/gen-diagrams`, `/new-project`) |
| `.github/skills/enclosure-gen/` | API reference for YAPP_Box / OpenSCAD enclosure generation |
| `.github/agents/` | Custom agent mode definitions |

## Common Agent Tasks

### Adding a New Project

1. Copy `_template/` → `<project-name>/`
2. Use `tools/parts-register/parts.json` during planning to quickly identify known controller, LED strip, PSU, level shifter, and connector facts before re-researching them
3. Edit `<project-name>/specs.md` (concept, requirements, **Home Assistant** section, mechanical constraints, acceptance criteria)
4. Fill `<project-name>/hardware/bom/bom.md` with LED current budget
5. Create `<project-name>/gen_diagrams_config.py` following `reefs/gen_diagrams_config.py`
6. Create `<project-name>/gen_diagrams.py` following `reefs/gen_diagrams.py`; run `python tools/gen_diagrams.py <project-name>`
7. Run `/gen-enclosure` to write the SCAD and render shells + preview PNGs into `mechanical/enclosure/` (helper: `pwsh tools/render_enclosure.ps1 -Project <project-name> -ScadName <project-name>-enclosure`)
8. Set a unique mDNS hostname in `firmware/cfg.json` (`"id": {"mdns": "<project-name>"}`, `"nw": {"mdns": 1}`)
9. Create `homeassistant/` artifacts (see "Home Assistant Config Files" section below)
10. Upload spiffs to the device over WiFi (no USB required):
   ```
   python tools/upload_spiffs.py --project <project-name>
   # or with explicit IP:
   python tools/upload_spiffs.py --project <project-name> --device 192.168.x.x
   ```
   Alternative (PlatformIO / USB): `pio run -t uploadfs`
11. Add a row to the Projects table in `README.md`
12. Open a PR from a branch named `project/<project-name>`

### Home Assistant Integration

Every project **must** be controllable from Home Assistant via the native WLED integration.

- Native WLED integration auto-discovers via mDNS — mDNS must be enabled in `firmware/cfg.json` (`"nw": {"mdns": 1}`)
- No MQTT. Do not add MQTT unless explicitly required.
- Verify on/off, brightness, and color control work in HA before marking a project complete.
- Document all HA entity IDs in the project's `specs.md` under a **"Home Assistant"** section.

### Home Assistant Config Files

Every project must have a `homeassistant/` folder at the project root containing:

| File | Purpose |
|------|---------|
| `homeassistant/README.md` | Import guide with `my.home-assistant.io` blueprint badge links |
| `homeassistant/package.yaml` | HA Package: helpers + scripts + automations |
| `homeassistant/lovelace.yaml` | Dashboard card YAML |
| `homeassistant/blueprints/*.yaml` | Project-specific blueprints (one per automation pattern) |
| `firmware/spiffs/ha-import.html` | Device-served import assistant page |

**Blueprint rules:**
- File name: `{project}-{pattern}.yaml`
- Must include `source_url` pointing to GitHub raw URL
- Use `blueprint.input` for all entity IDs
- Include `domain: automation` at blueprint level

**`ha-import.html` rules:**
- Copy from `_template/firmware/spiffs/ha-import.html`
- Update the `PROJECT_CONFIG` / `REPO_BASE` / `BLUEPRINTS` / `PACKAGE_FILE` block at the top
- Core HTML/JS body must not diverge from the template
- Page reads WLED `/json/info` + `/json/state` to auto-compute HA entity IDs

**package.yaml rules:**
- Top of file: commented entity ID substitution block pointing to `ha-import.html`
- Section order: helpers (`input_boolean`, `input_number`, `input_select`) → `script` → `automation`
- Automation `id` format: `{project}_{automation_slug}`

### hacs-wledext-effects

[hacs-wledext-effects](https://github.com/tamaygz/hacs-wledext-effects) is a HACS custom integration for context-aware LED effects driven by HA state.

**9 built-in effects:** Rainbow Wave, Segment Fade, Loading, State Sync, Breathe, Meter, Sparkle, Chase, Alert.

Each effect creates controllable HA entities (Switch / Number / Select / Sensor / Button).

**Use it when the project needs:**
- Real-time sensor visualization (temperature, CPU, energy, humidity → LED color/fill)
- HA-event-driven notifications (motion, door, security alarm → Alert / Breathe)
- Multi-zone independent data display on one strip
- Automation-controlled effect behavior (pulse rate, color, intensity driven by HA state)

**Skip it when:**
- A static WLED preset or palette is sufficient
- The effect is purely decorative with no HA state dependency

**Setup steps (per project):**
1. Add HACS custom repo `https://github.com/tamaygz/hacs-wledext-effects` (category: Integration)
2. Install "WLED Effects" from HACS → restart HA
3. Settings → Devices & Services → Add → "WLED Effects" → select WLED device
4. Document installed effects and entity IDs in `specs.md` → "Home Assistant"
5. Document installed effects and entity IDs in `specs.md` → "Home Assistant"; add example automations to `homeassistant/package.yaml`

### Generating an Enclosure

- Authoritative API reference: [`.github/skills/enclosure-gen/SKILL.md`](.github/skills/enclosure-gen/SKILL.md)
- Slash command: `/gen-enclosure` (writes SCAD + spec, then renders)
- Manual re-render after editing the SCAD:
  ```powershell
  pwsh tools/render_enclosure.ps1 -Project <project> -ScadName <project>-enclosure
  ```
- Defaults to enforce: snap-on lid (`snapJoins`, no `connectors`), `yappBaseOnly` for `pcbStands`, `ridgeHeight = 6.0` (≥ wallThickness × 1.8), shared library included via `../../../tools/yapp/YAPPgenerator_v3.scad`, explicit `YAPPgenerate();` as the last line
- Commit alongside the SCAD: `<project>-base.stl`, `<project>-lid.stl`, and the 4 preview PNGs (`-base-iso`, `-base-top`, `-lid-iso`, `-lid-top`)
- Inspect the iso PNGs before committing — floating stems on the lid mean a `pcbStands` entry still uses `yappBoth` and must be switched to `yappBaseOnly`

### Modifying Shared Diagram Generation

- Only change files under `tools/diagram_gen/`
- Never duplicate logic into a project folder
- Validate changes by running: `python tools/gen_diagrams.py reefs`
- Commit generated outputs to `<project>/docs/` alongside the code change

### Diagram Types

Four `--type` flags are available:

| `--type` | Module | Output file(s) | Description |
|----------|--------|----------------|-------------|
| `blocks` | `blocks.py` | `concept-system.png` | System block diagram: PSU → ESP32 → level shifter → LED strips → HA |
| `concept` | `concept.py` | `concept-side-view.png`, `concept-top-view.png` | Real-world visualisation: side-view cross-section and top-down floor plan |
| `wiring` | `wiring.py` | `wiring-physical.svg` (+ `.png`) | Color-coded physical wiring diagram with pin labels |
| `schematic` | `schematic.py` | `schematic-level-shifter.png`, `schematic-power.png` | Electrical schematics |

Key `DIAGRAM_CONFIG` fields for concept/real-world diagrams: `lamps` (list with `label`, `cx`), `wood_label`, `box_pos`. See `reefs/gen_diagrams_config.py` for a working example.

### Updating Firmware Config

- `platformio_override.ini` — build-time overrides only; do not touch WLED upstream sources
- `firmware/cfg.json`, `firmware/presets.json` — runtime WLED config exported from the web UI
- **No WiFi credentials in any committed file**

### Maintaining the Parts Register

- Check `tools/parts-register/parts.json` before introducing any new component dimensions, ratings, or board pin mappings.
- During planning, use the register first to answer routine questions about candidate LEDs, boards, PSUs, level shifters, and connectors before re-researching the same part.
- If a part is missing, add it to the register before using it elsewhere in the project.
- New entries should include the technical fields that matter for reuse, not just physical dimensions.
- For boards and devkits, capture pinout data when possible: official image/PDF link, source URL, software identifiers, and a structured pin list with GPIO numbers, aliases, capabilities, and warnings.
- Prefer official datasheets and board pages first, then PlatformIO or framework metadata for machine-readable identifiers, then distributor listings. Mark community-derived data as unverified.
- If you touch an older geometry-only entry during new work, backfill technical metadata or board pinout details instead of creating parallel notes in project files.
- When writing user-facing docs such as `README.md`, `specs.md`, `hardware/bom/bom.md`, or `hardware/wiring/WIRING.md`, surface relevant register facts instead of restating ad-hoc estimates.
- If a register entry has a `source_url`, link to it from user-facing docs when the part is mentioned in a summary or parts table.
- If a board entry has `board_pinout.image_url` or `board_pinout.image_path`, embed or link a preview in project-facing docs when it helps the reader understand the hardware quickly.

### Fixing Wiring Diagrams

- Wiring source is `<project>/gen_diagrams.py` + `gen_diagrams_config.py`
- Regenerate after changes: `python tools/gen_diagrams.py <project> --type wiring`
- Commit updated `<project>/docs/*.png` / `*.svg`

## Boundaries

- Do not modify `.git/` files.
- Do not add generated images without regenerating them from source.
- Do not add new pip dependencies without updating `tools/diagram_gen/requirements.txt`.
- Do not modify the upstream `tools/yapp/YAPPgenerator_v3.scad` library file.
- Do not commit secrets, WiFi credentials, or API keys.
- Do not edit files in `<project>/docs/` by hand — they are tool outputs.

## Commit Convention

```
feat(<project>): <description>
fix(tools): <description>
docs(<project>): <description>
chore: <description>
```

Examples:
```
feat(reefs): add WLED preset for movie mode
fix(tools): correct level-shifter gate count in schematic
docs(reefs): regenerate all diagrams after GPIO reassignment
chore(_template): add effects/ placeholder to template
```

## Pull Request Guidelines

- One logical change per PR
- Title follows the commit convention above
- Include diagram screenshots in the PR description when `docs/` files change
- Reference the relevant `specs.md` section when adding or changing hardware specs
