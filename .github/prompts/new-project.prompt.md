---
mode: agent
description: Scaffold a new ESP32/WLED project from the _template/ skeleton. Fills in specs.md, bom.md, gen_diagrams_config.py, and updates the root README.
---

# New Project Scaffold

Scaffold a new WLED project in this repository.

## Inputs

- **Project name** (slug, no spaces): `$PROJECT_NAME`
- **LED strip type** (e.g. SK6812 RGBW, WS2812B RGB): `$LED_TYPE`
- **LED count per output** (e.g. 60): `$LED_COUNT`
- **Number of outputs** (independent segments): `$NUM_OUTPUTS`
- **One-line description**: `$DESCRIPTION`

## Steps

1. Copy `_template/` → `$PROJECT_NAME/` (preserve all subdirectory structure)

2. Edit `$PROJECT_NAME/specs.md`:
   - Replace `[Project Name]` with the human-readable project name
   - Set Status to `planning`
   - Fill the Requirements section with LED type, count, and power from inputs above
   - Leave Open Questions with at least one placeholder

3. Edit `$PROJECT_NAME/hardware/bom/bom.md`:
   - Calculate peak current: `$LED_COUNT × $NUM_OUTPUTS × 20 mA × channels`
   - Add 20 % headroom to determine minimum PSU current rating
   - Add a placeholder parts list table (Part | Qty | Unit Price | Supplier | Part No.)

4. Create `$PROJECT_NAME/gen_diagrams_config.py`:
   - Copy structure from `reefs/gen_diagrams_config.py`
   - Update `project`, `title`, `psu`, `controller`, `outputs`, `gpio_map`, `lamps` keys
   - Assign GPIO 16, 17, 18 … sequentially for each output

5. Create `$PROJECT_NAME/gen_diagrams.py`:
   - Copy from `reefs/gen_diagrams.py`
   - The `sys.path` insert must point to `../tools` relative to the project folder

6. Update root `README.md`:
   - Add a row to the Projects table: `| [$PROJECT_NAME](./$PROJECT_NAME/) | planning | $LED_TYPE × $LED_COUNT | $DESCRIPTION |`

## Constraints

- Do not create any files outside `$PROJECT_NAME/` and `README.md`
- Do not modify `_template/` — only copy from it
- Do not run `gen_diagrams.py` yet — leave that for after hardware config is finalised
