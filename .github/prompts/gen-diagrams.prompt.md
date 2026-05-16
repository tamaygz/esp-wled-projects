---
mode: agent
description: Regenerate all diagrams (or a specific type) for a project using tools/gen_diagrams.py. Validates the config file before running.
---

# Generate Diagrams

Regenerate the visual documentation for a project.

## Inputs

- **Project name** (folder name): `$PROJECT`
- **Diagram type** (optional — omit to regenerate all): `$TYPE`
  Valid types: `schematic`, `blocks`, `concept`, `wiring`

## Steps

1. Verify `$PROJECT/gen_diagrams_config.py` exists and exports `DIAGRAM_CONFIG` with the required keys: `project`, `title`, `psu`, `controller`, `outputs`, `gpio_map`, `lamps`.

2. Verify `$PROJECT/gen_diagrams.py` exists and imports from `tools/diagram_gen` via `sys.path`.

3. Run the diagram generator from the repo root:
   ```bash
   # All types:
   python tools/gen_diagrams.py $PROJECT

   # Single type:
   python tools/gen_diagrams.py $PROJECT --type $TYPE
   ```

4. Confirm output files were written to `$PROJECT/docs/`:
   - `concept-side-view.png` — real-world side-view cross-section (concept type)
   - `concept-top-view.png` — top-down floor-plan with lamp positions (concept type)
   - `concept-system.png` — system block diagram: PSU → ESP32 → level shifter → strips (blocks type)
   - `wiring-physical.svg` — color-coded physical wiring diagram (and `.png` if cairosvg available) (wiring type)
   - `schematic-level-shifter.png` — level shifter circuit (schematic type)
   - `schematic-power.png` — power distribution circuit (schematic type)

5. If the run fails, check for:
   - Missing pip packages → `pip install -r tools/diagram_gen/requirements.txt`
   - `schemdraw` version < 0.22 → upgrade
   - `drawsvg` import issues → confirm `import drawsvg as draw` (not `drawsvg2`)

## Notes

- All output goes to `$PROJECT/docs/` — never to any other path.
- Do not hand-edit generated PNG/SVG files. Fix the generator source instead.
- Commit generated outputs alongside the config change that triggered regeneration.
