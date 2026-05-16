# Enclosure — 3D Models

> Run `/gen-enclosure` to generate the `.scad` source file and populate this
> document with project-specific parameters. Both STLs and 4 preview PNGs are
> committed alongside the SCAD source.

## Control Box

| Parameter | Value |
|-----------|-------|
| Outer dimensions (L × W × H) | — |
| Inner dimensions | — |
| Wall thickness | 3.0 mm |
| Base wall height | — |
| Lid wall height | — |
| Ridge height (snap fit) | 6.0 mm (≥ wallThickness × 1.8) |
| Lid closure | Snap-on (4 snap-joins, no screws) |
| Generator | [YAPP_Box v3](https://github.com/mrWheel/YAPP_Box) (MIT) — shared at `tools/yapp/YAPPgenerator_v3.scad` |

## Print Settings

| Parameter | Value |
|-----------|-------|
| Material | PETG (or ASA for higher temp) |
| Layer height | 0.2 mm |
| Infill | 20 % Gyroid |
| Perimeters | 3 |
| Supports | None |

## Cutouts & Features

| Face | Component | Cutout dimensions | Notes |
|------|-----------|------------------|-------|
| — | — | — | — |

## PCB Standoffs

| Component | Mount type | Hole pattern | YAPP flag |
|-----------|-----------|--------------|-----------|
| ESP32 DevKit | M3 self-thread | 23 × 45 mm | `yappBaseOnly` |

## Files

| File | Purpose | Committed |
|------|---------|-----------|
| `<project>-enclosure.scad` | YAPP_Box source config | ✅ |
| `<project>-enclosure-spec.md` | Per-project parameter sheet | ✅ |
| `<project>-base.stl` | Base shell, print-ready | ✅ |
| `<project>-lid.stl` | Lid shell, print-ready | ✅ |
| `<project>-base-iso.png` | Isometric preview of base | ✅ |
| `<project>-base-top.png` | Top-down preview of base | ✅ |
| `<project>-lid-iso.png` | Isometric preview of lid | ✅ |
| `<project>-lid-top.png` | Top-down preview of lid | ✅ |

The YAPP library is **not** copied into the project — it is included by
relative path from the shared location: `../../../tools/yapp/YAPPgenerator_v3.scad`.

## Render Instructions

From the repo root:

```powershell
pwsh tools/render_enclosure.ps1 -Project <project> -ScadName <project>-enclosure
```

The helper invokes OpenSCAD twice for the STLs and four times for the preview
PNGs, then prints a summary table.

Install OpenSCAD from <https://openscad.org/downloads.html>. Default expected
path: `C:\Program Files\OpenSCAD\openscad.exe`.
