# Enclosure — 3D Models

> Run `/gen-enclosure` to generate the `.scad` source file and populate this document
> with project-specific parameters and render instructions.

## Control Box

| Parameter | Value |
|-----------|-------|
| Outer dimensions | — |
| Inner dimensions | — |
| Wall thickness | — |
| Base wall height | — |
| Lid wall height | — |
| Corner style | — |
| Generator | [YAPP_Box v3](https://github.com/mrWheel/YAPP_Box) (MIT) |

## Print Settings

| Parameter | Value |
|-----------|-------|
| Material | PETG |
| Layer height | 0.2 mm |
| Infill | 20% Gyroid |
| Perimeters | 3 |
| Supports | None |

## Cutouts & Features

| Face | Component | Cutout dimensions | Notes |
|------|-----------|------------------|-------|
| — | — | — | — |

## PCB Standoffs

| Component | Mount type | Hole pattern |
|-----------|-----------|-------------|
| — | — | — |

## Files

| File | Purpose |
|------|---------|
| `<project>-enclosure.scad` | YAPP_Box source config — version controlled |
| `YAPPgenerator_v3.scad` | YAPP library (MIT) — version controlled |
| `*.stl` | Rendered output — **NOT committed** (add to `.gitignore`) |

## Render Instructions

```bash
# Download library (once)
# https://github.com/mrWheel/YAPP_Box/releases/latest → YAPPgenerator_v3.scad

# Render base
openscad --render -o <project>-box.stl <project>-enclosure.scad -D printLidShell=false

# Render lid
openscad --render -o <project>-lid.stl <project>-enclosure.scad -D printBaseShell=false
```

Install OpenSCAD from <https://openscad.org/downloads.html>.
