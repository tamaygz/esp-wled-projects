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
7. Open a PR from a branch named `project/<project-name>`

### Modifying Shared Diagram Generation

- Only change files under `tools/diagram_gen/`
- Never duplicate logic into a project folder
- Validate changes by running: `python tools/gen_diagrams.py reefs`
- Commit generated outputs to `<project>/docs/` alongside the code change

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
