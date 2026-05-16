---
name: new-project
description: Scaffold a new ESP32/WLED project from the _template/ skeleton. Fills in specs.md, bom.md, gen_diagrams_config.py, and updates the root README.
argument-hint: "project-name led-type led-count outputs description"
agent: agent
tools:
   - read
   - search
   - edit
   - vscode/askQuestion
---

# New Project Scaffold

Scaffold a new WLED project in this repository.

If any required input is missing or ambiguous, use the VS Code ask-question tool to collect it with suggested options and keep free-form input enabled.

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
   - Check `tools/parts-register/parts.json` first for the selected board, LED strip, PSU, level shifter, and connector facts
   - Fill the Requirements section with LED type, count, and power from inputs above
   - Add a **Home Assistant** section listing: expected HA entity IDs, mDNS device name (`<project-name>`), and whether hacs-wledext-effects is applicable
   - Leave Open Questions with at least one placeholder

3. Edit `$PROJECT_NAME/hardware/bom/bom.md`:
   - Calculate peak current: `$LED_COUNT × $NUM_OUTPUTS × 20 mA × channels`
   - Add 20 % headroom to determine minimum PSU current rating
   - Reuse register-backed part names, source links, and dimensions when the selected parts already exist in `tools/parts-register/parts.json`
   - Add a placeholder parts list table (Part | Qty | Unit Price | Supplier | Part No.)

4. Create `$PROJECT_NAME/gen_diagrams_config.py`:
   - Copy structure from `reefs/gen_diagrams_config.py`
   - Update `project`, `title`, `psu`, `controller`, `outputs`, `gpio_map`, `lamps` keys
   - Assign GPIO 16, 17, 18 … sequentially for each output

5. Create `$PROJECT_NAME/gen_diagrams.py`:
   - Copy from `reefs/gen_diagrams.py`
   - The `sys.path` insert must point to `../tools` relative to the project folder

6. Set mDNS hostname in `$PROJECT_NAME/firmware/cfg.json`:
   - Add/update `"id": {"mdns": "$PROJECT_NAME"}` and `"nw": {"mdns": 1}`
   - The hostname must be unique on the network — use the project slug

7. Create `$PROJECT_NAME/design/effects/ha-automations.yaml` with a placeholder comment:
   ```yaml
   # Home Assistant automations for $PROJECT_NAME
   # Add example automations here once hacs-wledext-effects effects are configured
   ```

8. **Enclosure stub** — leave `$PROJECT_NAME/mechanical/enclosure/MODELS.md` as the template stub. Do **not** generate the SCAD now; run `/gen-enclosure` after BOM and wiring are finalised so the cutout dimensions and PCB standoff layout are correct.

9. Edit `$PROJECT_NAME/README.md` with the correct project README structure:

   **Section order (required):**
   1. `# $PROJECT_NAME` title and `>` one-liner tagline
   2. **Concept** section — 2–3 sentences, then three image embeds with a generate note:
      ```markdown
      ![Side-view cross-section](docs/concept-side-view.png)
      ![Top-down floor plan](docs/concept-top-view.png)
      ![System block diagram](docs/concept-system.png)
      > Run `python tools/gen_diagrams.py $PROJECT_NAME` from the repo root to generate these images.
      ```
   3. **Quick Facts** table — board, `$LED_TYPE`, count, PSU, WLED version, Home Assistant
   4. **Key Components / Parts Snapshot** — build a short table from `tools/parts-register/parts.json` covering the controller, LED strip, PSU, level shifter, and any important connector. Include `PART_ID`, role, 1–3 key facts, `source_url` link when present, and board pinout preview/link when available.
   5. **Documentation Index** table — link every file that will exist:
      `specs.md`, `hardware/bom/bom.md`, `hardware/wiring/WIRING.md`,
      `design/led-map/LED-DESIGN.md`, `design/effects/ha-automations.yaml`,
      `firmware/platformio_override.ini`, `firmware/cfg.json`, `firmware/presets.json`
   6. **Wiring & Schematics** section — embed `docs/wiring-physical.svg`, two-column table with
      `docs/schematic-level-shifter.png` and `docs/schematic-power.png`, link to `hardware/wiring/WIRING.md`
   7. **Build Checklist** — project-specific MVP steps (flash, bench-test, assemble, configure WLED, add to HA, mount, thermal soak)
   8. **Resources** — link `specs.md`, WLED Docs, WLED GitHub

10. Update root `README.md`:
   - Add a row to the Projects table: `| [$PROJECT_NAME](./$PROJECT_NAME/) | planning | $LED_TYPE × $LED_COUNT | $DESCRIPTION |`

11. After the scaffold is in place, switch to the `ESP/WLED Project Reviewer` agent or use the planner's review handoff so the first pass is checked for missing files, parts-register-backed hardware facts, and repo-meta coherence before it is treated as complete.

## Constraints

- Do not create any files outside `$PROJECT_NAME/` and `README.md`
- Do not modify `_template/` — only copy from it
- Do not run `gen_diagrams.py` yet — leave that for after hardware config is finalised
- Keep `![](docs/...)` image tags in the README even though images do not exist yet; the generate note explains this
- If a required part is missing from the parts register, add it before finalizing the README, specs, or BOM text that describes that part
