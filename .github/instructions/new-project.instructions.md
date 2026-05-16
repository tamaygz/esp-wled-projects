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

1. **`specs.md`** — fill out concept, requirements, constraints, acceptance criteria
2. **`hardware/bom/bom.md`** — calculate current budget, select PSU, list all parts
3. **`hardware/wiring/WIRING.md`** — document GPIO assignments, power rails, wire runs
4. **`gen_diagrams_config.py`** — copy from `reefs/gen_diagrams_config.py`, update values
5. **`gen_diagrams.py`** — copy from `reefs/gen_diagrams.py`, update project import path
6. **`README.md`** (project level) — brief overview, link to specs.md
7. **`README.md`** (repo root) — add a row to the Projects table

## specs.md Structure

A `specs.md` must contain at minimum:

- **Concept**: one paragraph describing the project and intended effect
- **Requirements**: LED type, count, power source, mounting, connectivity, smart home target
- **Constraints**: budget, enclosure size, power availability
- **Acceptance Criteria**: checklist of "done" conditions (all LEDs responding, WLED reachable, presets saved, no flicker, thermal OK, enclosure closed)
- **Open Questions**: anything not yet decided

## DIAGRAM_CONFIG Keys

`gen_diagrams_config.py` must export `DIAGRAM_CONFIG` with at minimum:

| Key | Type | Description |
|-----|------|-------------|
| `project` | str | Folder name of the project |
| `title` | str | Display title for diagram headers |
| `psu` | str | PSU label (e.g. `"Brand 5V / 10A"`) |
| `controller` | str | Controller label (e.g. `"ESP32-WROOM-32\nWLED v0.15+"`) |
| `outputs` | list[dict] | Each has `name` and `strip` keys |
| `gpio_map` | list[dict] | Each has `gpio`, `label`, `color` |
| `lamps` | list[dict] | Each has `label`, `cx` (x position) |

Copy `reefs/gen_diagrams_config.py` and update all values for the new project.

## README.md Projects Table

When adding a project, append a row to the table in the root `README.md`:

```markdown
| [project-name](./project-name/) | Status | LED type × count | One-line description |
```

Status values: `planning`, `wip`, `done`, `archived`.
