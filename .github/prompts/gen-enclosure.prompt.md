---
mode: agent
description: >
  Generate a complete 3D enclosure for an ESP32/WLED project using YAPP_Box
  (MIT-licensed parametric OpenSCAD box generator). Reads project documentation
  and produces a ready-to-render mechanical/enclosure/<project>-enclosure.scad
  file and an updated MODELS.md. Run after hardware wiring is finalised.
tools:
  - read_file
  - create_file
  - replace_string_in_file
  - run_in_terminal
---

# /gen-enclosure

Generate a YAPP_Box `.scad` enclosure for project **$PROJECT_NAME**.

Use the `enclosure-gen` skill as the primary reference for the YAPP_Box API,
cutout dimensions, and component tables.

---

## Inputs

Gather these facts before writing any file:

| Input | Source |
|-------|--------|
| Target outer dimensions (max) | `$PROJECT_NAME/specs.md` → Constraints section |
| Component list + physical dimensions | `$PROJECT_NAME/hardware/bom/bom.md` |
| Connector positions + types | `$PROJECT_NAME/hardware/wiring/WIRING.md` |
| Print material / layer height | `$PROJECT_NAME/specs.md` → Mechanical section |

---

## Steps

### 1. Read project documentation

Read the following files in parallel:
- `$PROJECT_NAME/specs.md`
- `$PROJECT_NAME/hardware/bom/bom.md`
- `$PROJECT_NAME/hardware/wiring/WIRING.md`

If `$PROJECT_NAME/mechanical/enclosure/MODELS.md` exists, read it for any
pre-existing enclosure constraints.

---

### 2. Inventory components

Build two lists from the BOM and wiring docs:

**Internal layout** (determines interior volume):

| Component | L×W mm | Height mm | Notes |
|-----------|--------|-----------|-------|
| (fill from BOM) | | | |

**Face-mounted connectors** (determine cutouts):

| Connector | Type | Assigned face | Cutout (W×H or radius) |
|-----------|------|---------------|------------------------|
| (fill from BOM + WIRING.md) | | | |

Face assignment rules:
- Mains inlet (IEC C14) → Back wall (largest face if applicable)
- USB-C for OTA/programming → Front wall or most accessible side
- Cable glands (lamp/LED cables) → Front wall, away from mains
- Buttons / display → Lid or front wall
- Multiple identical connectors → Same face, evenly spaced

---

### 3. Calculate dimensions

```
inner_L = widest_component_footprint_along_L + 10mm margin   (5mm each side)
inner_W = widest_component_footprint_along_W + 10mm margin
inner_H = tallest_stack (standoffHeight + pcbThickness + tallest_component) + 10mm

Round each dimension UP to nearest 5mm.

outer_L = inner_L + 2 × wallThickness
outer_W = inner_W + 2 × wallThickness
outer_H = inner_H + basePlaneThickness + lidPlaneThickness

Verify outer fits the constraint in specs.md.
If it does not, reduce margins proportionally and document the trade-off.
```

Split the inner height into base + lid wall heights.
Default split: baseWallHeight ≈ 55 % of inner_H, lidWallHeight ≈ 45 %.
Ensure `ridgeHeight` (default 5.0) ≤ `lidWallHeight`.

---

### 4. Generate `<project>-enclosure.scad`

Create the file at `$PROJECT_NAME/mechanical/enclosure/$PROJECT_NAME-enclosure.scad`
using the template structure from the `enclosure-gen` skill.

The file **must** include (in this order):
1. Header comment with project name, date, outer dimensions, render commands
2. Render control flags (`printBaseShell`, `printLidShell`, etc.)
3. Dimension variables (pcbLength, pcbWidth, wall heights, paddings = 0)
4. `pcb = [ ["Main", ...] ]` block
5. `pcbStands` — 4 standoffs for ESP32 DevKit or actual PCB mounting holes
6. `connectors` — 4×M3 lid corner screws
7. All six cutout arrays (`cutoutsFront`, `cutoutsBack`, `cutoutsLeft`, `cutoutsRight`, `cutoutsLid`, `cutoutsBase`)
8. `labelsPlane` — project name on lid (optional)
9. Empty arrays for unused features (snapJoins, boxMounts, lightTubes, pushButtons, displayMounts)
10. `include <./YAPPgenerator_v3.scad>` — **this must be the very last line**

Use `yappCoordBoxInside, yappCenter` for all cutout positioning.
Add inline comments explaining each cutout's purpose and its source in the BOM.

---

### 5. Download YAPP library

If `$PROJECT_NAME/mechanical/enclosure/YAPPgenerator_v3.scad` does not exist,
print the following instruction:

```
Download YAPPgenerator_v3.scad and place it alongside the enclosure .scad:

  Releases: https://github.com/mrWheel/YAPP_Box/releases/latest
  Direct (latest main):
  https://raw.githubusercontent.com/mrWheel/YAPP_Box/main/YAPPgenerator_v3.scad

  Save to: $PROJECT_NAME/mechanical/enclosure/YAPPgenerator_v3.scad
```

---

### 6. Update `MODELS.md`

Create or replace `$PROJECT_NAME/mechanical/enclosure/MODELS.md` with:

```markdown
# $PROJECT_NAME — Enclosure

## Control Box

| Parameter | Value |
|-----------|-------|
| Outer dimensions | L×W×Hmm |
| Inner dimensions | L×W×Hmm |
| Wall thickness | Xmm |
| Base wall height | Xmm |
| Lid wall height | Xmm |
| Corner style | Rounded / radius Xmm |
| Box type (YAPP boxType) | 0 |

## Print Settings

| Parameter | Value |
|-----------|-------|
| Material | PETG |
| Layer height | 0.2mm |
| Infill | 20% Gyroid |
| Perimeters | 3 |
| Supports | None |

## Cutouts & Features

| Face | Component | Cutout | Coordinates |
|------|-----------|--------|-------------|
| (list each cutout from the .scad file) | | | |

## PCB Standoffs

| Component | Mount type | Hole pattern |
|-----------|-----------|-------------|
| ESP32 DevKit | M3 self-threading | 23×45mm |

## Render Instructions

```bash
# Download library (once)
curl -L https://raw.githubusercontent.com/mrWheel/YAPP_Box/main/YAPPgenerator_v3.scad \
     -o mechanical/enclosure/YAPPgenerator_v3.scad

# Base only
openscad --render -o mechanical/enclosure/$PROJECT_NAME-box.stl \
         mechanical/enclosure/$PROJECT_NAME-enclosure.scad \
         -D printLidShell=false

# Lid only
openscad --render -o mechanical/enclosure/$PROJECT_NAME-lid.stl \
         mechanical/enclosure/$PROJECT_NAME-enclosure.scad \
         -D printBaseShell=false
```

## Files

| File | Purpose |
|------|---------|
| `$PROJECT_NAME-enclosure.scad` | YAPP_Box source config — version controlled |
| `YAPPgenerator_v3.scad` | YAPP library (MIT) — version controlled |
| `*.stl` | Rendered output — NOT committed (add to .gitignore) |
```

---

### 7. Print render instructions

After files are written, print this exact block to the user:

```
Enclosure files created:
  mechanical/enclosure/$PROJECT_NAME-enclosure.scad
  mechanical/enclosure/MODELS.md

To render STL files:

  1. Download YAPPgenerator_v3.scad into the same folder (see MODELS.md for URL)

  2. Install OpenSCAD from https://openscad.org/downloads.html (if not installed)

  3. Render base:
     openscad --render -o $PROJECT_NAME-box.stl $PROJECT_NAME-enclosure.scad -D printLidShell=false

  4. Render lid:
     openscad --render -o $PROJECT_NAME-lid.stl $PROJECT_NAME-enclosure.scad -D printBaseShell=false

  5. Or open the .scad in the OpenSCAD GUI to preview and adjust before rendering.

Gitignore reminder — add to $PROJECT_NAME/.gitignore (or root .gitignore):
  mechanical/enclosure/*.stl
```
