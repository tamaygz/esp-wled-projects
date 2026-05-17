# 3D Models & Enclosure — Reefs

## Automated Variant Enclosure (Parametric YAPP)

Parametric PETG enclosure generated via the [`enclosure-gen`](../../../.github/skills/enclosure-gen/SKILL.md) skill, using shared YAPP library at `tools/yapp/YAPPgenerator_v3.scad`.

> Legacy controller geometry: the current SCAD and rendered outputs still use the previous ESP32 DevKit mount and front USB opening. The `reefs` project controller definition moved to `ESP8266_NODEMCU_V3`; refit the board mount and service-port cutout before the next print.

**Snap-on lid — no screws, tool-free open/close.**

| Property | Value |
|----------|-------|
| Source | [`reefs-automatedvariant-enclosure.scad`](reefs-automatedvariant-enclosure.scad) |
| Spec | [`reefs-automatedvariant-enclosure-spec.md`](reefs-automatedvariant-enclosure-spec.md) |
| Outer | 150 × 100 × 59 mm |
| Inner | 144 × 94 × 56 mm |
| Wall thickness | 3.0 mm |
| Ridge height | 6.0 mm (≥ wallThickness × 1.8 for snapJoins) |
| Lid closure | 4 × snap-joins on long walls (15 mm wide, posx = 40 & 110) |
| PCB standoffs | 4 × M3, `yappBaseOnly` (no stems on lid) |

### Files

| File | Description |
|------|-------------|
| [`reefs-automatedvariant-base.stl`](reefs-automatedvariant-base.stl) | Base shell |
| [`reefs-automatedvariant-lid.stl`](reefs-automatedvariant-lid.stl) | Lid shell |
| [`reefs-automatedvariant-base-iso.png`](reefs-automatedvariant-base-iso.png) | Base — isometric preview |
| [`reefs-automatedvariant-base-top.png`](reefs-automatedvariant-base-top.png) | Base — top-down preview |
| [`reefs-automatedvariant-lid-iso.png`](reefs-automatedvariant-lid-iso.png) | Lid — isometric preview |
| [`reefs-automatedvariant-lid-top.png`](reefs-automatedvariant-lid-top.png) | Lid — top-down preview |

### Re-generate

```powershell
# From repo root — produces both STLs and all 4 preview PNGs
pwsh tools/render_enclosure.ps1 -Project reefs -ScadName reefs-automatedvariant-enclosure
```

---

## Control Box Enclosure (Legacy BambuStudio)

Custom-designed PETG enclosure for the older ESP32 controller variant, with 74AHCT125 level shifter, screw terminal bus, inline fuses, and IEC C14 inlet.

| Property | Value |
|----------|-------|
| BambuStudio project | [`CustomProjectEnclosureV1.7.8b.3mf`](CustomProjectEnclosureV1.7.8b.3mf) |
| Outer dimensions | ≤ 150 × 100 × 60 mm (L × W × H) |
| Material | PETG (preferred) or ASA |
| Rendered preview | [`case-preview.png`](case-preview.png) |
| Top-view render | [`case-top.png`](case-top.png) |

### Print Settings

| Setting | Value |
|---------|-------|
| Material | PETG |
| Layer height | 0.2 mm |
| Infill | 20% gyroid |
| Walls | 3 |
| Supports | Touching build plate only |
| Bed temp | 80 °C |
| Nozzle | 230 °C |

### Cutouts & Features

| Feature | Dimension | Notes |
|---------|-----------|-------|
| IEC C14 inlet | 28 × 48 mm | Standard panel-mount C14 |
| USB access port | 12 × 6 mm slot | Legacy ESP32-aligned opening; refit for the NodeMCU V3 before reuse |
| Cable gland holes (PG9) | × 2 | One per lamp cable entry |
| Ventilation slots | ≥ 4 × 15 mm per side | PSU natural convection |
| PCB standoffs | 4 × M3, 20 × 30 mm pattern | Legacy ESP32 DevKit mount |
| Lid fastening | 4 × M3 × 8 mm | Top-opening lid with brass inserts |

---

## Aluminium LED Channels

Not a 3D-printed part — off-the-shelf U-profile aluminium channels are used to mount the SK6812 strips on the rear face of each driftwood piece.

| Property | Value |
|----------|-------|
| Profile type | U-channel with diffuser clip |
| Width | 12 mm (fits SK6812 8mm strip with margin) |
| Length | ≥ driftwood rear face length (≤ 1 m) |
| Example product | LUMINES Type-Z or equivalent |
| Purpose | Conducts heat away from wood; provides diffused line light |

---

## Future Models

> If aluminium channel brackets or cable management clips are designed, add STL files here and update the table below.

| File | Purpose | Status |
|------|---------|--------|
| _(none yet)_ | | |
