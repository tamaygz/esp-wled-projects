# Parts Dimensions Register

`parts.json` provides verified physical dimensions for components commonly used across projects in this repository. It is the single source of truth for enclosure SCAD cutout sizes, PCB footprint planning, and BOM documentation.

## Purpose

When designing enclosures, wiring, or PCB layouts, check this register **first** before measuring components manually or looking up datasheets. Using register values ensures consistency between `bom.md`, `*-enclosure.scad`, and `WIRING.md` files across the repo.

## Units

All dimensions are in **millimetres (mm)**. `pcb_or_body_mm` gives the bounding box `l × w × h` (length × width × height) of the component's PCB footprint or encapsulated body.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable component name |
| `manufacturer` | string | Component manufacturer |
| `mfr_part_number` | string | Manufacturer part number |
| `category` | string | Component category (e.g. `microcontroller`, `ac_dc_psu`, `led_strip`) |
| `pcb_or_body_mm` | object | Bounding box `l` (length), `w` (width), `h` (height) in mm |
| `mounting_holes` | array | Mounting hole positions relative to bounding box bottom-left corner |
| `cutouts_needed` | array | Panel or enclosure cutout specs (for ports, connectors, etc.) |
| `key_notes` | array | Engineering notes, gotchas, and usage guidance |
| `source_url` | string | Primary datasheet or product page used to verify dimensions |
| `verified` | boolean | `true` if confirmed from official datasheet; `false` if estimated |

## Using the Register

- **Enclosure SCAD files**: Reference `pcb_or_body_mm` and `cutouts_needed` when sizing `boxInnerHeight`, PCB standoffs, and cutout arrays in YAPP_Box SCAD files. Add a comment citing the `PART_ID`.
- **BOM files (`bom.md`)**: Cross-reference part names and MPN values against register entries.
- **WIRING.md**: Reference connector dimensions for cable routing guidance and strain-relief sizing.

## Adding a New Part

1. Assign a unique `PART_ID` key (e.g. `MY_PART_REV2`) — use `SCREAMING_SNAKE_CASE`.
2. Fill all fields. Use `"verified": false` if any dimension is estimated.
3. Set `source_url` to the official datasheet page, or an LCSC/JLCPCB listing as a fallback.
4. Add a note in `key_notes` explaining what is estimated and how to verify it.
5. Commit the updated `parts.json` in the same commit as the first project file that uses the new dimensions.

If adding a part that is already in the register but a different revision or voltage variant, create a new `PART_ID` with a suffix (e.g. `HLK_5M12` for the 12V variant).

## Unverified Entries

Entries with `"verified": false` have dimensions estimated from family-series data, community sources, or prior art. They are safe for initial planning but must be confirmed from an official datasheet before committing to final PCB layout or enclosure manufacturing.

Any SCAD or BOM file using an unverified entry should include a comment:
```
// UNVERIFIED — confirm HLK_30M05 dimensions before manufacturing
```

## Parts Included

| PART_ID | Name | L × W × H (mm) | Category | Verified |
|---------|------|-----------------|----------|----------|
| `D1_MINI_V4` | Wemos LOLIN D1 Mini v4 | 34.2 × 25.6 × 10.0 | microcontroller | ✅ |
| `HLK_30M05` | Hi-Link HLK-30M05 30W 5V 6A | 57.5 × 33.6 × 22.5 | ac_dc_psu | ⚠️ estimated |
| `HLK_20M05` | Hi-Link HLK-20M05 20W 5V 4A | 56.0 × 32.0 × 22.5 | ac_dc_psu | ✅ |
| `HLK_5M05` | Hi-Link HLK-5M05 5W 5V 1A | 38.0 × 23.0 × 18.0 | ac_dc_psu | ✅ |
| `IC_74AHCT125_DIP14` | 74AHCT125 Quad Buffer DIP-14 | 19.05 × 6.35 × 4.57 | level_shifter_ic | ✅ |
| `JST_SM_2P5_3PIN` | JST SM 2.5mm 3-pin Connector | 9.5 × 6.0 × 6.0 | connector | ⚠️ estimated |
| `SK6812_RGBW_60` | SK6812 RGBW LED Strip 60 LED/m | 1000 × 10 × 1.5 per m | led_strip | ✅ |
