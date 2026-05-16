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
| `reefs/` | Active project — driftwood ambient lamps (SK6812 RGBW, ESP32, Home Assistant) |
| `.github/instructions/` | Scoped Copilot instruction files |
| `.github/prompts/` | Reusable prompt templates |
| `.github/agents/` | Custom agent mode definitions |

## Common Agent Tasks

### Adding a New Project

1. Copy `_template/` → `<project-name>/`
2. Edit `<project-name>/specs.md` (concept, requirements, acceptance criteria)
3. Fill `<project-name>/hardware/bom/bom.md` with LED current budget
4. Create `<project-name>/gen_diagrams_config.py` following `reefs/gen_diagrams_config.py`
5. Create `<project-name>/gen_diagrams.py` following `reefs/gen_diagrams.py`
6. Add a row to the Projects table in `README.md`
7. Add a **"Home Assistant"** section to `specs.md` — list expected entity IDs and note whether `hacs-wledext-effects` is applicable
8. Set a unique mDNS hostname in `firmware/cfg.json` so HA auto-discovers the device
9. Open a PR from a branch named `project/<project-name>`

### Home Assistant Integration

Every project **must** be controllable from Home Assistant via the native WLED integration.

- Native WLED integration auto-discovers via mDNS — mDNS must be enabled in `firmware/cfg.json` (`"nw": {"mdns": 1}`)
- No MQTT. Do not add MQTT unless explicitly required.
- Verify on/off, brightness, and color control work in HA before marking a project complete.
- Document all HA entity IDs in the project's `specs.md` under a **"Home Assistant"** section.

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
5. Store example automations in `design/effects/ha-automations.yaml`

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

### Fixing Wiring Diagrams

- Wiring source is `<project>/gen_diagrams.py` + `gen_diagrams_config.py`
- Regenerate after changes: `python tools/gen_diagrams.py <project> --type wiring`
- Commit updated `<project>/docs/*.png` / `*.svg`

## Boundaries

- Do not modify `.git/` files.
- Do not add generated images without regenerating them from source.
- Do not add new pip dependencies without updating `tools/diagram_gen/requirements.txt`.
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
