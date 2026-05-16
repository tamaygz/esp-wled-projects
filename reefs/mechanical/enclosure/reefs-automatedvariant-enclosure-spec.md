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
| Ridge height | 6.0 mm |
| Corner radius | 3.0 mm |

> Ridge height bumped from 5.0 → 6.0 mm to satisfy YAPP's snap-join geometry
> constraint (`ridgeHeight ≥ wallThickness × 1.8 = 5.4 mm`).

## Files

| File | Description |
|------|-------------|
| `reefs-automatedvariant-enclosure.scad` | Parametric SCAD config |
| `reefs-automatedvariant-base.stl` | Base shell (print-ready) |
| `reefs-automatedvariant-lid.stl` | Lid shell (print-ready) |
| `reefs-automatedvariant-base-iso.png` | Base preview — isometric |
| `reefs-automatedvariant-base-top.png` | Base preview — top-down |
| `reefs-automatedvariant-lid-iso.png`  | Lid preview — isometric  |
| `reefs-automatedvariant-lid-top.png`  | Lid preview — top-down  |

Render all six in one step:

```powershell
pwsh tools/render_enclosure.ps1 -Project reefs -ScadName reefs-automatedvariant-enclosure
```

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

4 × M3 threaded standoffs (5 mm height, Ø7 mm outer, Ø3 mm pin), **base only**
(`yappBaseOnly` — the lid stays clear of standoff stems):

| Position | PCB coord (X, Y) | Corner |
|----------|-----------------|--------|
| Back-left | 81, 35 | yappBackLeft |
| Back-right | 81, 58 | yappBackRight |
| Front-left | 126, 35 | yappFrontLeft |
| Front-right | 126, 58 | yappFrontRight |

Board orientation: USB-C end toward FRONT wall (high X).

## Lid Closure — Snap-On (no screws)

The lid uses YAPP `snapJoins` so it presses onto the base by hand and can be
opened without tools. Four snaps total, on the two long walls:

| Snap | Wall | Position along wall | Width |
|------|------|--------------------|-------|
| 1 | Left  | 40 mm  | 15 mm |
| 2 | Left  | 110 mm | 15 mm (mirrored via `yappSymmetric`) |
| 3 | Right | 40 mm  | 15 mm |
| 4 | Right | 110 mm | 15 mm (mirrored via `yappSymmetric`) |

SCAD entry:

```scad
connectors = [];
snapJoins  = [
  [40, 15, yappLeft, yappRight, yappCenter, yappSymmetric],
];
```

If screw fastening is later required, replace `snapJoins` with a `connectors[]`
entry and drop `ridgeHeight` back to 5.0 mm.

## Lid Labels (engraved)

| Text | Face | Position | Size |
|------|------|----------|------|
| `REEFS` (bold) | Lid | centre | 10 mm |
| `WLED v16 \| SK6812 RGBW` | Lid | centre | 6 mm |
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

From repo root — single command produces both STLs **and** the four preview PNGs:

```powershell
pwsh tools/render_enclosure.ps1 -Project reefs -ScadName reefs-automatedvariant-enclosure
```

Manual fallback (per shell):

```bash
openscad --render -o reefs-automatedvariant-base.stl \
  reefs-automatedvariant-enclosure.scad -D "printLidShell=false"
openscad --render -o reefs-automatedvariant-lid.stl  \
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
| Fasteners | tool-free | 4× snap-joins (no screws) ✓ |
