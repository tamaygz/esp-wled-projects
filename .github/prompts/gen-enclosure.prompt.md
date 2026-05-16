---
mode: agent
description: >
  Generate a complete 3D-printable enclosure for an ESP32/WLED project using
  YAPP_Box (MIT-licensed parametric OpenSCAD box generator). Reads project
  documentation and produces a ready-to-render
  mechanical/enclosure/<project>-enclosure.scad, then renders both shells plus
  4 preview PNGs via tools/render_enclosure.ps1. Default lid closure is
  snap-on (no screws).
tools:
  - read_file
  - create_file
  - replace_string_in_file
  - run_in_terminal
---

# /gen-enclosure

Generate a YAPP_Box `.scad` enclosure for project **$PROJECT_NAME** and render
all printable artifacts.

Use the [`enclosure-gen` skill](../skills/enclosure-gen/SKILL.md) as the
canonical reference for the YAPP_Box API, cutout dimensions, ESP32 standoff
geometry, label placement, and the reefs worked example.

---

## Inputs

| Input | Source |
|-------|--------|
| Target outer dimensions (max) | `$PROJECT_NAME/specs.md` → Constraints section |
| Component list + physical dimensions | `$PROJECT_NAME/hardware/bom/bom.md` |
| Connector positions + types | `$PROJECT_NAME/hardware/wiring/WIRING.md` |
| Reusable part dimensions + cutouts | `tools/parts-register/parts.json` |
| Print material / layer height | `$PROJECT_NAME/specs.md` → Mechanical section (optional) |

---

## Steps

### 1. Read project documentation

Read in parallel:
- `$PROJECT_NAME/specs.md`
- `$PROJECT_NAME/hardware/bom/bom.md`
- `$PROJECT_NAME/hardware/wiring/WIRING.md`
- `$PROJECT_NAME/mechanical/enclosure/MODELS.md` (if present)

Then check `tools/parts-register/parts.json` for any controller, PSU, connector, or board already named in the project docs so enclosure sizing reuses canonical repo dimensions and cutout metadata.

### 2. Inventory components

Build two lists:

**Internal layout** (sets interior volume): component, L×W mm, height mm, wiring clearance.

**Face-mounted connectors** (sets cutouts): connector → assigned face → cutout size from the table in the skill.

Prefer parts-register dimensions and `cutouts_needed` over ad-hoc BOM notes whenever the part already exists in the register.

Face assignment rules:
- Mains inlet (IEC C14) → Back wall
- USB-C for OTA → Front or accessible side
- Cable glands (lamp/LED) → Front, away from mains
- Buttons / display → Lid or front wall

### 3. Calculate dimensions

```
inner_L = widest_component_span_along_L + 10mm margin
inner_W = widest_component_span_along_W + 10mm margin
inner_H = standoffHeight + pcbThickness + tallest_internal_component + 10mm
→ round each UP to nearest 5mm
→ verify outer (= inner + 2×wallThickness) fits the spec constraint
```

Default split: `baseWallHeight ≈ 55 %`, `lidWallHeight ≈ 45 %` of inner height.

### 4. Generate `<project>-enclosure.scad`

Create the file at
`$PROJECT_NAME/mechanical/enclosure/$PROJECT_NAME-enclosure.scad`.

**Required file structure** (follow the reefs worked example in the skill):

1. **Line 1:** header comment with project name, date, target dimensions, and the render command
2. **Line 2 (FIRST executable):** `include <../../../tools/yapp/YAPPgenerator_v3.scad>` — must be first so project values below override library defaults
3. Render-control flags (`printBaseShell = true; printLidShell = true; …`)
4. Dimension variables (`pcbLength`, `pcbWidth`, wall heights; paddings = 0 — virtual PCB approach)
5. `wallThickness = 3.0; basePlaneThickness = 1.5; lidPlaneThickness = 1.5;`
6. **`ridgeHeight = 6.0;`** (must satisfy `ridgeHeight >= wallThickness * 1.8` whenever `snapJoins` is non-empty — YAPP asserts this)
7. `pcb = [ ["Main", pcbLength, pcbWidth, 0, 0, pcbThickness, standoffHeight, standoffDiameter, standoffPinDiameter, standoffHoleSlack] ];` — the leading `"Main"` string is required by YAPP v3
8. **`pcbStands`** — ESP32 DevKit pattern, **always use `yappBaseOnly`** (not `yappBoth`) so the lid stays clean
9. **`connectors = [];`** and **`snapJoins = [ [40, 15, yappLeft, yappRight, yappCenter, yappSymmetric] ];`** — snap-on lid is the default. Only fill `connectors[]` if the user explicitly requested screws
10. All six cutout arrays (`cutoutsFront`, `cutoutsBack`, `cutoutsLeft`, `cutoutsRight`, `cutoutsLid`, `cutoutsBase`) — keep empty arrays for unused faces; use `yappCoordBoxInside, yappCenter` throughout
11. **`labelsPlane`** with two mandatory groups:
    - **Project title on lid** (1–3 centred lines):
      - Line 1: project name, size 10, `"Liberation Sans:style=Bold"`, `depth = -0.6` (raised)
      - Line 2 (optional): subtitle, size 6, `depth = -0.4`
      - Line 3 (optional): version/date, size 4, `depth = -0.3`
      - Lid centre: `posx = outerL/2`, `posy = outerW/2` where `outerL = pcbLength + 2 × wallThickness`
      - Line spacing: `1.6 × largest_font_size` mm
      - All centred (`yappTextHAlignCenter, yappTextVAlignCenter`)
    - **Cutout identification labels** — one per external connector:
      - Same face constant as the cutout
      - Horizontal: `posx = cutout_p0 + wallThickness`
      - Above cutout: `posy = (cutout_p1 + hole_half_height + 2 + 2) + basePlaneThickness`
      - Below cutout: `posy = (cutout_p1 − hole_half_height − 2 − 2) + basePlaneThickness`
      - For circles: `hole_half_height = radius`
      - Size 4–5 mm, ALLCAPS text (`"POWER IN"`, `"OTA"`, `"LAMP 1"`)
      - Raised: `depth = -0.4`
12. Empty arrays for unused features: `boxMounts = []; lightTubes = []; pushButtons = []; displayMounts = [];`
13. **Last line:** `YAPPgenerate();` — explicit call required to bypass the library's `if(debug)` guard

**File encoding:** save as **UTF-8 without BOM**. In PowerShell:
```powershell
[System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding $false))
```

### 5. Render STLs + previews

The repo provides a one-shot helper that produces both shells **and** 4 preview PNGs:

```powershell
pwsh tools/render_enclosure.ps1 -Project $PROJECT_NAME -ScadName $PROJECT_NAME-enclosure
```

Outputs (committed alongside the SCAD):

| File | Purpose |
|------|---------|
| `$PROJECT_NAME-base.stl` | Base shell, print-ready |
| `$PROJECT_NAME-lid.stl` | Lid shell, print-ready |
| `$PROJECT_NAME-base-iso.png` | Isometric preview of base |
| `$PROJECT_NAME-base-top.png` | Top-down preview of base |
| `$PROJECT_NAME-lid-iso.png` | Isometric preview of lid |
| `$PROJECT_NAME-lid-top.png` | Top-down preview of lid |

Visually inspect the iso PNGs before committing: the lid must have **no floating
PCB stems** (if it does, switch the relevant `pcbStands` entries to
`yappBaseOnly`).

### 6. Update `MODELS.md`

Replace `$PROJECT_NAME/mechanical/enclosure/MODELS.md` with a section that
includes:

- Parameter table (outer/inner dims, wall thickness, base/lid wall heights, lid closure = snap-on)
- Print settings table (PETG, 0.2 mm layer, 20 % gyroid, 3 perimeters, no supports)
- Cutouts table (face, component, dimensions)
- PCB standoffs row (ESP32 DevKit, M3 self-thread, 23 × 45 mm, `yappBaseOnly`)
- Files table linking every artifact (SCAD, both STLs, all 4 PNGs, spec)
- Render command (helper script call from §5)

### 7. Report to the user

Print exactly:

```
Enclosure generated and rendered.

SCAD source:
  $PROJECT_NAME/mechanical/enclosure/$PROJECT_NAME-enclosure.scad

STLs (print-ready):
  $PROJECT_NAME-base.stl
  $PROJECT_NAME-lid.stl

Previews (committed for review):
  $PROJECT_NAME-base-iso.png   $PROJECT_NAME-base-top.png
  $PROJECT_NAME-lid-iso.png    $PROJECT_NAME-lid-top.png

Lid closure: snap-on (4 snap-joins, no screws).
To re-render after edits:
  pwsh tools/render_enclosure.ps1 -Project $PROJECT_NAME -ScadName $PROJECT_NAME-enclosure
```

---

## Constraints

- **Do not** download `YAPPgenerator_v3.scad` into the project folder — the shared library lives at `tools/yapp/YAPPgenerator_v3.scad` and is included via relative path
- **Do not** default to screw-fastened lids — snap-on is the project standard
- **Do not** use `yappBoth` for PCB standoffs — `yappBaseOnly` keeps the lid clean
- **Do not** put the `include` line at the bottom of the file — OpenSCAD's "last assignment wins" will overwrite your project values
- **Do not** omit the trailing `YAPPgenerate();` call — without it the STL will be empty
- Always commit the STLs and preview PNGs alongside the SCAD
