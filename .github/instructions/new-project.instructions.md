---
description: >
  New project scaffolding conventions and specs.md authoring rules.
  Use when creating a new project folder, filling out specs.md,
  editing README.md, or working with the _template/ skeleton.
applyTo:
  - "_template/**"
  - "*/specs.md"
  - "README.md"
---

# New Project — Instructions

## Starting a New Project

Always start from `_template/` — never create the folder structure from scratch:

```bash
cp -r _template/ <project-name>/
```

Then work through these steps **in order**:

1. **`specs.md`** — fill out concept, requirements, constraints, acceptance criteria, and the **Home Assistant** section
2. **`hardware/bom/bom.md`** — calculate current budget, select PSU, list all parts
3. **`hardware/wiring/WIRING.md`** — document GPIO assignments, power rails, wire runs
4. **`gen_diagrams_config.py`** — copy from `reefs/gen_diagrams_config.py`, update values
5. **`gen_diagrams.py`** — copy from `reefs/gen_diagrams.py`, update project import path
6. **`firmware/cfg.json`** — set a unique mDNS hostname: `"id": {"mdns": "<project-name>"}` and ensure `"nw": {"mdns": 1}`
7. **`README.md`** (project level) — brief overview, link to specs.md
8. **`README.md`** (repo root) — add a row to the Projects table

## specs.md Structure

A `specs.md` must contain at minimum:

- **Concept**: one paragraph describing the project and intended effect
- **Requirements**: LED type, count, power source, mounting, connectivity, smart home target
- **Constraints**: budget, enclosure size, power availability
- **Acceptance Criteria**: checklist of "done" conditions (all LEDs responding, WLED reachable, presets saved, no flicker, thermal OK, enclosure closed, HA control verified)
- **Open Questions**: anything not yet decided
- **Home Assistant** *(mandatory)*: list expected HA entity IDs (e.g. `light.reefs_lamp_1`), the mDNS device name used, and whether [hacs-wledext-effects](https://github.com/tamaygz/hacs-wledext-effects) effects are needed and which ones

## hacs-wledext-effects

If the project uses state-driven LED effects, add a `design/effects/ha-automations.yaml` file with example automations. Note in `specs.md` which effects are installed and their entity IDs.

Use hacs-wledext-effects when the strip should visualize a HA sensor value, fire notification-style alerts from HA events, or when automation-controlled effect behaviour is needed. Skip it when a static WLED preset is sufficient or there is no HA state dependency.

## DIAGRAM_CONFIG Keys

`gen_diagrams_config.py` must export `DIAGRAM_CONFIG` with at minimum:

| Key | Type | Used by | Description |
|-----|------|---------|-------------|
| `project` | str | all | Folder name of the project |
| `title` | str | all | Display title for diagram headers |
| `psu` | str | blocks, wiring | PSU label (e.g. `"Brand 5V / 10A"`) |
| `controller` | str | blocks, wiring | Controller label (e.g. `"ESP32-WROOM-32\nWLED v0.15+"`) |
| `shifter` | str \| None | blocks, wiring | Level shifter label, or `None` to omit |
| `integration` | str \| None | blocks | Smart-home block label (e.g. `"Home\nAssistant"`) |
| `outputs` | list[dict] | blocks, wiring | Each has `name` and `strip` keys |
| `gpio_map` | list[dict] | wiring | Each has `gpio`, `label`, `color` |
| `lamps` | list[dict] | concept | Each has `label`, `cx` (x-position along wall) |
| `wood_label` | str | concept | Label inside the driftwood / object silhouette in the side-view |
| `box_pos` | tuple(float,float) | concept | (x, y) position of the control box in the top-down floor plan |
| `power_label` | str | wiring | PSU label shown on the wiring diagram power block |

Copy `reefs/gen_diagrams_config.py` and update all values for the new project.

## Diagram Types

Four types are produced by `python tools/gen_diagrams.py <project>`:

| Type flag | Module | Output file(s) | What it shows |
|-----------|--------|----------------|---------------|
| `blocks` | `blocks.py` | `concept-system.png` | System block diagram: PSU → ESP32 → level shifter → LED strips → HA integration |
| `concept` | `concept.py` | `concept-side-view.png`, `concept-top-view.png` | Real-world visualisation: cross-section of lamp on wall (side), floor-plan with lamp positions and cable run (top) |
| `wiring` | `wiring.py` | `wiring-physical.svg` (+ `.png`) | Color-coded physical wiring: ESP32 pins → level shifter → JST connectors |
| `schematic` | `schematic.py` | `schematic-level-shifter.png`, `schematic-power.png` | Electrical schematics: level-shifter gate circuit and power distribution |

## README.md Projects Table

When adding a project, append a row to the table in the root `README.md`:

```markdown
| [project-name](./project-name/) | Status | LED type × count | One-line description |
```

Status values: `planning`, `wip`, `done`, `archived`.
