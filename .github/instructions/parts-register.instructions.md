---
description: Parts Register — enforce register-first workflow for dimensions, technical metadata, and board pinouts
applyTo:
  - "**/bom.md"
  - "**/*-enclosure.scad"
  - "**/WIRING.md"
  - "**/specs.md"
  - "**/*.scad"
---

# Parts Register Rules

Before adding any component dimensions, technical specifications, or board pin mappings to a `bom.md`, `specs.md`, `WIRING.md`, or enclosure SCAD file, **check `tools/parts-register/parts.json` first**.

## Rules

1. **Register-first**: When a component appears in `parts.json`, use its register data verbatim. Do not look up dimensions, ratings, or pin mappings independently when a verified entry already exists.

2. **Propagate to SCAD**: When writing or modifying a `*-enclosure.scad` file, derive `boxInnerHeight`, cutout sizes, and PCB standoff positions from `pcb_or_body_mm` and `cutouts_needed` in the register entry. Add a comment citing the `PART_ID`:
   ```scad
   // JST_SM_2P5_3PIN — parts-register: 9.5×6.0mm pocket
   [9.5, 6.0, ...]
   ```

3. **Add before use**: If a component is not yet in the register, add a `"verified": false` entry to `parts.json` **before** using it in any project file. Use web search to find the best available source, then add the result to the register.

4. **Capture technical fields that matter**: New entries should include the design-critical technical data for that category, not just geometry. Examples include voltage/current limits, protocol, color order, mating connector, MCU, wireless capability, flash/PSRAM size, or operating temperature.

5. **Boards require pinout metadata when available**: For development boards and controller boards, add `software_identifiers` and `board_pinout` whenever official documentation or framework metadata exists. Prefer a structure that includes:
   - `image_url` or `image_path`
   - `source_url`
   - `pins[]` with silkscreen label, GPIO, aliases, capabilities, and warnings

6. **Use source priority**: Prefer official manufacturer datasheets and official board pages first, then PlatformIO board manifests or framework variant files for software identifiers, then distributor listings, and only then community references. Mark community-derived data as unverified.

7. **Flag unverified in SCAD/BOM**: Any SCAD or BOM file that uses dimensions from a `"verified": false` register entry must include a comment next to the affected value:
   ```scad
   // UNVERIFIED — confirm HLK_30M05 dimensions before manufacturing
   ```

8. **Update, don't duplicate**: If measured or datasheet dimensions differ from the register, update `parts.json` first, then propagate the correction to all affected files in the same commit.

9. **Backfill touched legacy entries**: If you are already using an older geometry-only entry for new work, extend it with technical metadata or board pinout data when reliable sources are available.

## Quick Reference

| Resource | Path |
|----------|------|
| Register JSON | `tools/parts-register/parts.json` |
| Field documentation | `tools/parts-register/README.md` |

## Adding a New Part (checklist)

- [ ] Search LCSC/JLCPCB or the manufacturer's datasheet page for confirmed dimensions
- [ ] Capture the technical fields that drive actual design decisions for that part category
- [ ] For boards, capture official pinout docs plus software identifiers and a structured `board_pinout.pins` list when possible
- [ ] Assign a `SCREAMING_SNAKE_CASE` `PART_ID`
- [ ] Set `"verified": true` only if dimensions come from an official datasheet or distributor listing
- [ ] Set `source_url` to the specific page used
- [ ] Commit `parts.json` first, then the project file that references it
