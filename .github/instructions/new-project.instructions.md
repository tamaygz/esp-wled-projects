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
4. **Enclosure** — once wiring is finalised, run `/gen-enclosure` to generate `mechanical/enclosure/<project>-enclosure.scad` — see **Enclosure Generation** section below
5. **`gen_diagrams_config.py`** — copy from `reefs/gen_diagrams_config.py`, update values
6. **`gen_diagrams.py`** — copy from `reefs/gen_diagrams.py`, update project import path
7. **`firmware/cfg.json`** — set a unique mDNS hostname: `"id": {"mdns": "<project-name>"}` and ensure `"nw": {"mdns": 1}`
8. **`README.md`** (project level) — full project README following the **Project README Structure** standard below: concept images first, documentation index table, wiring diagrams, build checklist
9. **`README.md`** (repo root) — add a row to the Projects table
10. **Review pass** — after scaffolding or broad project doc updates, switch to the `ESP/WLED Project Reviewer` agent or the planner's review handoff so the first pass is checked for missing artifacts, register-backed hardware facts, and current repo-meta coherence

## Planning With The Parts Register

At each planning step, check `tools/parts-register/parts.json` first so the project reuses known part data instead of re-deriving it.

| Planning step | Use the register for |
|---------------|----------------------|
| Concept / part selection | Compare candidate LED strips, controller boards, PSUs, and connectors already used in the repo |
| specs.md | Pull canonical part names, MPNs, voltages, protocols, and board capabilities |
| bom.md | Reuse exact part identity, sizing assumptions, and source links |
| WIRING.md | Reuse connector notes, board pinout data, GPIO warnings, and level-shifter guidance |
| Enclosure planning | Reuse `pcb_or_body_mm`, `cutouts_needed`, connector bodies, and board heights |
| README.md | Reuse concise part facts, `source_url` links, and board pinout previews when available |

If a required part is missing from the register, add it before finalizing the project docs.

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
| `controller` | str | blocks, wiring | Controller label (e.g. `"ESP32-WROOM-32\nWLED v16+"`) |
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

## Project README Structure

Every project `README.md` **must** follow this section order:

1. **Title + one-liner** — `# Project Name` and a `>` blockquote tagline
2. **Concept section** — 2–3 sentences describing the lighting effect and installation, immediately followed by the three concept images:
   - `docs/concept-side-view.png` — real-world cross-section of the lamp/object
   - `docs/concept-top-view.png` — floor-plan with installation positions and cable run
   - `docs/concept-system.png` — system block diagram (PSU → ESP32 → strips → HA)
3. **Quick Facts table** — board, LED type, LED count, PSU, WLED version, smart-home target
4. **Key Components / Parts Snapshot** — concise table sourced from `tools/parts-register/parts.json` for the controller, LED strip, PSU, level shifter, and any connector or module that is central to the build. Include:
   - register `PART_ID`
   - part name / role in the project
   - 1–3 high-value facts from the register
   - link to `source_url` when present
   - for boards, a pinout preview or pinout link when `board_pinout.image_url` or `board_pinout.image_path` is available
5. **Documentation Index table** — one row per document that physically exists in the project, linking to:
   - `specs.md`
   - `hardware/bom/bom.md`
   - `hardware/wiring/WIRING.md`
   - `design/led-map/LED-DESIGN.md`
   - `design/effects/ha-automations.yaml`
   - `mechanical/enclosure/MODELS.md` (when enclosure exists)
   - `firmware/platformio_override.ini`
   - `firmware/cfg.json`
   - `firmware/presets.json`
6. **Wiring & Schematics section** — embed `docs/wiring-physical.svg`, then a two-column table containing `docs/schematic-level-shifter.png` and `docs/schematic-power.png`; include a text link to `hardware/wiring/WIRING.md` for the GPIO table
7. **Build Checklist** — project-specific MVP steps as a task list
8. **Resources** — at minimum link to `specs.md`, WLED Docs, and WLED GitHub

**Rules:**
- Concept images must appear **before** the Quick Facts table — visuals communicate the idea before the spec details.
- The Key Components section must reuse register facts instead of hand-written approximations whenever the relevant part exists in `tools/parts-register/parts.json`.
- If the register provides `source_url`, link it from the Key Components table or related part mention.
- If the register provides `board_pinout.image_url` or `board_pinout.image_path`, show a board pinout preview or an explicit pinout link in the README.
- If diagrams have not been generated yet, keep the `![](docs/...)` image tags in place and add a callout: `> Run \`python tools/gen_diagrams.py <project>\` to generate these images.`
- Only link files that physically exist. Remove links to empty stubs from the Documentation Index.
- Do not hand-edit anything in `docs/` — regenerate via `python tools/gen_diagrams.py <project>`.

## README.md Projects Table

When adding a project, append a row to the table in the root `README.md`:

```markdown
| [project-name](./project-name/) | Status | LED type × count | One-line description |
```

Status values: `planning`, `wip`, `done`, `archived`.

## Enclosure Generation

Use **YAPP_Box** (MIT, 485⭐, actively maintained) as the standard enclosure design tool for all projects:
<https://github.com/mrWheel/YAPP_Box>

YAPP_Box produces parametric, command-line renderable OpenSCAD files. No MakerWorld login or browser required.

### Workflow

1. Run the `/gen-enclosure` slash command — it reads `specs.md`, `bom.md`, and `WIRING.md` to calculate dimensions and cutout positions
2. A complete `mechanical/enclosure/<project>-enclosure.scad` config file is generated. The SCAD includes the shared YAPP library via relative path `../../../tools/yapp/YAPPgenerator_v3.scad` — **do not** copy the library into the project folder
3. Render the base, the lid, and 4 preview PNGs with the helper:
   ```powershell
   pwsh tools/render_enclosure.ps1 -Project <project> -ScadName <project>-enclosure
   ```
4. Inspect the iso PNGs — lid must be clean (no floating standoff stems). If stems appear, change the offending `pcbStands` entry to `yappBaseOnly` and re-render.

### Output files

| File | Committed? |
|------|-----------|
| `mechanical/enclosure/<project>-enclosure.scad` | ✅ Yes (source) |
| `mechanical/enclosure/<project>-enclosure-spec.md` | ✅ Yes (parameter sheet) |
| `mechanical/enclosure/<project>-base.stl` | ✅ Yes |
| `mechanical/enclosure/<project>-lid.stl` | ✅ Yes |
| `mechanical/enclosure/<project>-{base,lid}-{iso,top}.png` | ✅ Yes (4 previews) |
| `tools/yapp/YAPPgenerator_v3.scad` | Shared — lives in `tools/yapp/`, **not** in the project folder |

### Key YAPP_Box design rules

- **Snap-on lid is the default** (`snapJoins = [[40, 15, yappLeft, yappRight, yappCenter, yappSymmetric]]`, `connectors = []`). Only use screw connectors if the user explicitly requests them.
- **`ridgeHeight = 6.0`** (must satisfy `ridgeHeight >= wallThickness * 1.8` whenever `snapJoins` is non-empty — YAPP asserts this at render time).
- **`pcbStands` must use `yappBaseOnly`** — lid stays clean, no floating posts.
- Use the **virtual PCB approach**: set `pcbLength`/`pcbWidth` to the desired inner dimensions, set all padding to `0`.
- Always use `yappCoordBoxInside, yappCenter` for cutout positioning.
- The `include <...>` line must be the **first** executable line; explicit `YAPPgenerate();` is the **last** line.

### MakerWorld alternative

If you prefer a browser GUI or need the MrPractical aesthetic, the MakerWorld
**Customizable Project Enclosure Box** (designId 952727) is an alternative.
Requires Bambu Lab account. No CLI render path — browser download only.
Use YAPP_Box for all new projects and automation scenarios.

### Skill reference

The `enclosure-gen` skill contains the complete YAPP_Box API reference including:
- All dimension calculation formulas
- Cutout array formats with shape constants
- Standard component cutout dimensions table (IEC C14, PG9, USB-C, barrel jack, etc.)
- ESP32 DevKit standoff dimensions
- CLI render commands
- Complete reefs project worked example
