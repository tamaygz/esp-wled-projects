# AGENTS.md — esp-wled-projects

This file provides guidance for GitHub Copilot Coding Agent and other AI agents operating on this repository. See `.github/copilot-instructions.md` for full project conventions.

## Repository Purpose

Mono-repo for DIY LED lighting projects powered by **WLED** on ESP32/ESP8266. Each subdirectory is a self-contained project with firmware, hardware docs, mechanical designs, and generated diagrams.

The repo root is also a reusable **meta layer**: it defines how new projects are planned, scaffolded, reviewed, and documented. Agents should treat the root-level docs and `.github/` customizations as the control plane for creating or upgrading project folders.

## Repository Map

| Path | Purpose |
|------|---------|
| `_template/` | Copy-paste skeleton for every new project |
| `README.md` | Public-facing explanation of the repo, the meta layer, and the project list |
| `tools/parts-register/` | Shared parts register and schema documentation |
| `tools/diagram_gen/` | Shared Python library for generating all project diagrams |
| `tools/gen_diagrams.py` | CLI runner: `python tools/gen_diagrams.py <project>` |
| `tools/yapp/YAPPgenerator_v3.scad` | Shared YAPP_Box library (MIT) — included by every project SCAD |
| `tools/render_enclosure.ps1` | One-shot helper: renders base + lid STLs + 4 preview PNGs |
| `tools/upload_spiffs.py` | WiFi file push: uploads `firmware/spiffs/` files to a live WLED device over HTTP (no USB needed) |
| `reefs/` | Active project — driftwood ambient lamps (SK6812 RGBW, ESP32, Home Assistant) |
| `curtaincinemalights/` | Active project — curtain-integrated cinema lighting (SK6812 RGBW, ESP8266, Home Assistant) |
| `reefs/homeassistant/` | HA package, blueprints, lovelace card, import guide |
| `reefs/firmware/spiffs/ha-import.html` | Device-served HA import assistant page |
| `.github/instructions/` | Scoped Copilot instruction files |
| `.github/prompts/` | Reusable prompt templates (incl. `/gen-enclosure`, `/gen-diagrams`, `/new-project`) |
| `.github/skills/enclosure-gen/` | API reference for YAPP_Box / OpenSCAD enclosure generation |
| `.github/agents/` | Custom agent definitions |
| `.github/hooks/README.md` | Hook policy and adoption guidance for deterministic automation |

## Doc Ownership

Use the root docs by role instead of treating them as interchangeable:

- `README.md` is the public-facing entry point. Keep it oriented around what the repo contains, how the meta layer helps, and how consumers should start a new project.
- `AGENTS.md` is the quick operational guide for coding agents. Keep it directive, repo-specific, and implementation-oriented.
- `.github/copilot-instructions.md` is the canonical always-on policy layer. Put broad repo rules there when they must apply consistently.
- `tools/parts-register/README.md` is the schema and sourcing reference for the parts register.
- `.github/hooks/README.md` explains when hooks are appropriate and when they are the wrong mechanism.

When a meta-level edit changes workflow, update all affected docs in the same pass instead of leaving the story split across files.

## VS Code Insiders Customizations

This repo is set up for the current VS Code Insiders customization model:

- `.github/copilot-instructions.md` and `AGENTS.md` provide always-on guidance.
- `.github/instructions/*.instructions.md` provide scoped rules with `applyTo` patterns.
- `.github/prompts/*.prompt.md` provide slash-command workflows.
- `.github/agents/*.agent.md` provide specialized personas with tool restrictions.
- `.github/skills/*/SKILL.md` provide reusable capabilities and reference material.
- `.github/hooks/README.md` documents when hooks should and should not be used in this repo.

### Handoffs, Subagents, And Hooks

- Prefer agent handoffs for guided phase changes such as planning → review so the user stays in control while the next step is obvious.
- Prefer subagents only for isolated research, parallel analysis, or specialized review perspectives. Keep those flows explicit rather than implicit.
- Use hooks only for deterministic automation and guardrails. Hooks are not a replacement for user decisions, clarifying questions, or planning logic.
- If hooks are added later, keep them under `.github/hooks/*.json`, make commands cross-platform, and keep them narrowly scoped.

For discoverability and troubleshooting in VS Code Insiders:

- open `Chat: Open Customizations` to manage prompts, instructions, skills, agents, hooks, and plugins
- use `/agents`, `/prompts`, `/instructions`, `/skills`, and `/hooks` in chat to open the relevant configuration UIs
- use the Chat diagnostics view to inspect which customizations loaded and whether any have metadata errors
- if you open only a child folder of this repo, enable `chat.useCustomizationsInParentRepositories` so the root customizations are discovered

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

### Meta-Level Doc Updates

When the task is about the repo root, `.github/`, shared tools, or the parts register rather than a single lighting build:

1. Start with `README.md`, `AGENTS.md`, and `.github/copilot-instructions.md` to understand the current public story and internal workflow.
2. Check whether the change also affects `tools/parts-register/README.md` or `.github/hooks/README.md`.
3. Keep public explanation in `README.md` and operational detail in `AGENTS.md` or `.github/copilot-instructions.md` instead of duplicating full sections in all three places.
4. After broad meta edits, prefer a reviewer pass to catch drift between prompts, instructions, agents, and root docs.

### Debugging A Real Build

Use the `ESP/WLED Realworld Hardware Debug` agent when a physical setup is not working and the failure location is still unclear.

- Start from the target project's `specs.md`, `hardware/bom/bom.md`, `hardware/wiring/WIRING.md`, and `firmware/cfg.json`.
- Use the VS Code ask-question tool to capture the actual hardware used, the main symptom, and any substitutions or added parts.
- Compare the documented design to the real build and produce a clear delta before recommending major fixes.
- Validate whether substitutions are acceptable, marginal, or fundamentally incompatible before telling the user to rebuild anything.
- Debug in the right order: power → boot/GPIO → data path → LED config → Home Assistant / automation layer.

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
5. Add example automations to `homeassistant/package.yaml` or `design/effects/ha-automations.yaml`

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

### User Decisions And Ambiguities

- When user input is needed for planning or tradeoffs, prefer the VS Code ask-question tool over ad-hoc prose questions.
- Always offer concrete options first and keep free-form input enabled so the user can override or refine the suggestion.
- Use structured questions for ambiguous choices such as LED family, board selection, PSU strategy, enclosure constraints, HA integration depth, and whether to proceed with scaffolding or generation steps.

### Review Workflow

- Use the planner agent to gather requirements and scaffold a project.
- After scaffolding or major meta-layer edits, hand off to the project reviewer agent instead of treating the first pass as complete.
- The review phase should verify current VS Code customization conventions, repo instruction coherence, project doc completeness, and parts-register-backed hardware summaries.

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
