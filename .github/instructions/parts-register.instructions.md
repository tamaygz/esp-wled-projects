---
description: Parts Dimensions Register — enforce register-first workflow when specifying component dimensions in any project file
applyTo:
  - "**/bom.md"
  - "**/*-enclosure.scad"
  - "**/WIRING.md"
  - "**/specs.md"
  - "**/*.scad"
---

# Parts Dimensions Register Rules

Before adding any component dimensions to a `bom.md`, `specs.md`, `WIRING.md`, or enclosure SCAD file, **check `tools/parts-register/parts.json` first**.

## Rules

1. **Register-first**: When a component appears in `parts.json`, use those dimensions verbatim. Do not look up dimensions independently or use rounded/approximated values when a verified entry exists.

2. **Propagate to SCAD**: When writing or modifying a `*-enclosure.scad` file, derive `boxInnerHeight`, cutout sizes, and PCB standoff positions from `pcb_or_body_mm` and `cutouts_needed` in the register entry. Add a comment citing the `PART_ID`:
   ```scad
   // JST_SM_2P5_3PIN — parts-register: 9.5×6.0mm pocket
   [9.5, 6.0, ...]
   ```

3. **Add before use**: If a component is not yet in the register, add a `"verified": false` entry to `parts.json` (with a `source_url` and an estimate note in `key_notes`) **before** using the dimensions in any other file. Use web search to find the best available source, then add the result to the register.

4. **Flag unverified in SCAD/BOM**: Any SCAD or BOM file that uses dimensions from a `"verified": false` register entry must include a comment next to the affected value:
   ```scad
   // UNVERIFIED — confirm HLK_30M05 dimensions before manufacturing
   ```

5. **Update, don't duplicate**: If measured or datasheet dimensions differ from the register, update `parts.json` first, then propagate the correction to all affected files in the same commit.

## Quick Reference

| Resource | Path |
|----------|------|
| Register JSON | `tools/parts-register/parts.json` |
| Field documentation | `tools/parts-register/README.md` |

## Adding a New Part (checklist)

- [ ] Search LCSC/JLCPCB or the manufacturer's datasheet page for confirmed dimensions
- [ ] Assign a `SCREAMING_SNAKE_CASE` `PART_ID`
- [ ] Set `"verified": true` only if dimensions come from an official datasheet or distributor listing
- [ ] Set `source_url` to the specific page used
- [ ] Commit `parts.json` first, then the project file that references it
