---
description: >
  Wiring, BOM, PCB, and hardware documentation rules for ESP32/WLED projects.
  Use when editing wiring diagrams, bill of materials, KiCad schematics,
  or adding hardware specs to any project.
applyTo:
  - "**/hardware/**"
  - "**/bom/**"
  - "**/wiring/**"
  - "**/pcb/**"
---

# Hardware — Instructions

## Level Shifting (Critical)

ESP32 GPIO outputs are **3.3 V logic**. LED strips (SK6812, WS2812B) require a **5 V data signal**. Always place a level shifter on every LED data line.

- Preferred ICs: **SN74HCT245** (octal) or **74AHCT125** (quad buffer)
- One gate per data channel
- OE pin active-low — tie to GND to keep buffers always enabled
- Bypass caps: 100 nF ceramic close to each VCC pin

## Power Injection

For LED strips longer than 1 m (or >50 LEDs):
- Inject power at both ends of the strip
- Inject every ≤ 50 LEDs for runs >2 m
- Wire gauge: 22 AWG minimum for ≤1 A; 18 AWG for >1 A per run

## Current Budget Formula

```
I_total = N_leds × mA_per_channel × channels
```

- SK6812 RGBW: use 20 mA per channel, 4 channels → 80 mA/LED maximum
- WS2812B RGB: use 20 mA per channel, 3 channels → 60 mA/LED maximum
- Apply a **20 % safety headroom** when selecting PSU wattage
- Add **10 % derating** for continuous operation

Example (SK6812, 60 LEDs): `60 × 20 mA × 4 = 4.8 A peak` → PSU ≥ 6 A (with headroom)

## bom.md Format

`hardware/bom/bom.md` must include:

1. **Power budget table** (LED current calculation, headroom, PSU selection)
2. **Parts list table** with columns: Part, Qty, Unit Price, Supplier, Part No., Notes
3. **Total cost estimate**

Preferred suppliers: LCSC (PCB components), Aliexpress / BTF-Lighting (LED strips), Mouser / DigiKey (precision parts).

## Common GND

The PSU 5 V GND and the ESP32 GND **must share a common ground**. This is not automatic — wire it explicitly between the PSU terminal block and the ESP32 GND pin.

## KiCad Conventions

- Schematic sources: `hardware/pcb/*.kicad_sch`
- PCB source: `hardware/pcb/*.kicad_pcb`
- Gerber exports: `hardware/pcb/gerbers/`
- Export Gerbers before every board order; commit them alongside the source

## GPIO Assignment (WLED defaults — override in cfg.json or via build flag)

| Signal | Recommended GPIO |
|--------|-----------------|
| LED Data 1 | GPIO 16 |
| LED Data 2 | GPIO 17 |
| LED Data 3 | GPIO 18 |
| IR Receiver | GPIO 4 |
| Button | GPIO 0 |

Avoid: GPIO 0 (boot mode), GPIO 2 (boot LED), GPIO 12 (boot flash voltage), GPIO 15 (boot messages).
