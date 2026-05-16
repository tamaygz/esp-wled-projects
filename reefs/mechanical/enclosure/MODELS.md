# 3D Models & Enclosure — Reefs

## Control Box Enclosure

Custom-designed PETG enclosure housing the ESP32, 74AHCT125 level shifter, screw terminal bus, inline fuses, and IEC C14 inlet.

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
| USB-C access port | 12 × 6 mm slot | Aligned to ESP32 USB port for OTA recovery |
| Cable gland holes (PG9) | × 2 | One per lamp cable entry |
| Ventilation slots | ≥ 4 × 15 mm per side | PSU natural convection |
| PCB standoffs | 4 × M3, 20 × 30 mm pattern | ESP32 DevKit mount |
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
