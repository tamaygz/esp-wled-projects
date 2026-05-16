# Reefs Enclosure — Automated Variant Spec

Generated via `enclosure-gen` skill using YAPP_Box v3.3.8.

## Dimensions

| Parameter | Value |
|-----------|-------|
| Outer | 150 × 100 × 59 mm |
| Inner (usable) | 144 × 94 × 56 mm |
| Wall thickness | 3.0 mm |
| Base floor | 1.5 mm |
| Lid ceiling | 1.5 mm |
| Base wall height | 30 mm |
| Lid wall height | 26 mm |
| Ridge height | 5.0 mm |
| Corner radius | 3.0 mm |

## Files

| File | Description | Size |
|------|-------------|------|
| `reefs-automatedvariant-enclosure.scad` | Parametric SCAD config | 5.7 KB |
| `reefs-automatedvariant-base.stl` | Base shell | 2.3 MB |
| `reefs-automatedvariant-lid.stl` | Lid shell | 3.8 MB |

## Shared Library

`tools/yapp/YAPPgenerator_v3.scad` — YAPP_Box v3.3.8 (mrWheel/YAPP_Box, MIT)

Include pattern: `include` must come **before** all config variables (OpenSCAD "last assignment wins").  
`YAPPgenerate()` is called explicitly to bypass the library's `if (debug)` guard.

## Wall Cutouts

### Back wall — IEC C14 mains inlet
- Opening: 28 × 48 mm (rectangle)
- Centre: Y = 47 mm (centred on 94 mm inner width), Z = 25 mm from inner floor
- Purpose: panel-mount IEC C14 inlet with built-in switch + fuse

### Front wall — USB-C OTA access
- Opening: 12 × 8 mm (rectangle)
- Centre: Y = 47 mm, Z = 10 mm from inner floor
- Purpose: cable access for ESP32 USB-C port during OTA flashing

### Left wall — Lamp 1
- PG9 cable gland: Ø16 mm (radius 8), centre X = 72 mm, Z = 25 mm
- Ventilation: 4 × (15 × 4 mm) slots at Z = 20 mm, X = 15, 40, 104, 129 mm

### Right wall — Lamp 2 (mirror of left)
- PG9 cable gland: Ø16 mm (radius 8), centre X = 72 mm, Z = 25 mm
- Ventilation: 4 × (15 × 4 mm) slots at Z = 20 mm, X = 15, 40, 104, 129 mm

## ESP32 Standoffs

4 × M3 threaded standoffs (5 mm height, Ø7 mm outer, Ø3 mm pin):

| Position | PCB coord (X, Y) | Corner |
|----------|-----------------|--------|
| Back-left | 81, 35 | yappBackLeft |
| Back-right | 81, 58 | yappBackRight |
| Front-left | 126, 35 | yappFrontLeft |
| Front-right | 126, 58 | yappFrontRight |

Board orientation: USB-C end toward FRONT wall (high X).

## Lid Connectors

4 × M3 corner screws, 5 mm from each inner corner:
- Standoff height: 5 mm (sufficient for M3 screw engagement; was incorrectly 12 mm)
- Screw: M3 (Ø3 mm), head Ø6 mm
- Insert hole: Ø3.2 mm (self-threading M3; use Ø4.2 mm for heat-set insert)

## Lid Labels (engraved)

| Text | Face | Position | Size |
|------|------|----------|------|
| `REEFS` (bold) | Lid | centre | 10 mm |
| `WLED v0.15 \| SK6812 RGBW` | Lid | centre | 6 mm |
| `2x 60-LED Lamps \| 5V 10A PSU` | Lid | centre | 4 mm |
| `POWER IN` (bold) | Back | above IEC cutout | 4 mm |
| `OTA` | Front | above USB-C cutout | 4 mm |
| `LAMP 1` | Left | above PG9 | 4 mm |
| `LAMP 2` | Right | above PG9 | 4 mm |

## Print Settings

| Parameter | Recommended |
|-----------|-------------|
| Material | PETG (or ASA for higher heat tolerance) |
| Layer height | 0.2 mm |
| Perimeters | 4 |
| Infill | 20 % (gyroid or grid) |
| Supports | None required |
| Bed adhesion | Brim (base), none needed for lid |

## Render Commands

From `reefs/mechanical/enclosure/`:

```bash
# Base only
openscad --render -o reefs-automatedvariant-base.stl \
  reefs-automatedvariant-enclosure.scad -D "printLidShell=false"

# Lid only
openscad --render -o reefs-automatedvariant-lid.stl \
  reefs-automatedvariant-enclosure.scad -D "printBaseShell=false"
```

## Spec Compliance

| Requirement | Target | Actual |
|-------------|--------|--------|
| Outer length | ≤ 150 mm | 150 mm ✓ |
| Outer width | ≤ 100 mm | 100 mm ✓ |
| Outer height | ≤ 60 mm | 59 mm ✓ |
| ESP32 mount | 4× M3 standoffs | ✓ |
| Mains entry | IEC C14 back wall | ✓ |
| OTA access | USB-C front wall | ✓ |
| Cable glands | 2× PG9 (left + right) | ✓ |
| Ventilation | 4 slots per side | ✓ |
| Fasteners | 4× M3 corner screws | ✓ |
