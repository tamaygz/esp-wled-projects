# BOM — Reefs (Driftwood Ambient Lamps)

> Generated from specs.md §8.2 — 2026-05-16

## Components

| # | Component | Spec | Qty | Unit Price | Supplier | Part No. | Notes |
|---|-----------|------|-----|------------|----------|----------|-------|
| 1 | SK6812 RGBW LED strip | 5 V, 60 LED/m, IP30, 4-pin (GRBW) | 2 × 1 m (60 LEDs each) | ~€8/m | AliExpress / BTF-Lighting | — | Order 1.1 m per lamp; trim to fit |
| 2 | ESP32 DevKit (38-pin) | ESP32-WROOM-32, USB-C preferred | 1 | ~€4 | LCSC | C701341 | Any 38-pin pinout works |
| 3 | Honeywell 5 V PSU | 5 V DC, ≥ 10 A (50 W) | 1 | (user-owned) | — | — | Verify nameplate rating ≥ 10 A |
| 4 | Aluminium LED channel | U-profile with diffuser, 12 mm wide, ≥ 1 m | 2 | ~€5 ea | Local / LUMINES | Type-Z or equiv. | Conducts heat away from wood |
| 5 | 3-conductor cable | 18 AWG power + 26 AWG data, or 3-core 20 AWG flex | 2 × 2.5 m | ~€2/m | Local electrical | — | 0.5 m slack; one cable per lamp |
| 6 | 330 Ω resistor | ¼ W, through-hole | 2 | <€0.01 ea | LCSC | C119313 | Series on GPIO data line at ESP32 side — ⚠️ C57436 is 10kΩ (MFR0W4F1002A50), not 330Ω |
| 7 | 74AHCT125 level shifter | SO-14 or DIP-14 | 1 | ~€0.30 | LCSC | C12494 | 3.3 V → 5 V for SK6812 data; 2 channels used |
| 8 | Blade fuse holder (inline) | 5 × 20 mm, panel or wire mount | 2 | ~€0.50 ea | LCSC / local | — | One per lamp 5 V power run |
| 9 | 5 A blade fuse | 5 × 20 mm slow-blow | 4 | <€0.20 ea | Local | — | 2 installed + 2 spare |
| 10 | JST SM 3-pin connector (M+F pair) | 2.5 mm pitch, 3 A rated | 2 pairs | ~€0.30/pair | on hand | — | **Female panel-mounted** in box wall pocket (lamp side male); V+/GND/DATA |
| 11 | Phoenix-style pluggable terminal | 3-pos, 5.08 mm pitch, screw clamp (PCB header + plug) | 1 | (on hand) | on hand | — | Internal 5 V distribution (PSU → fuses); replaces classic screw terminal |
| 12 | 3D-printed enclosure | ~150 × 100 × 60 mm PETG/ASA | 1 | ~€2 filament | Self-printed | — | See `mechanical/enclosure/reefs-automatedvariant-enclosure-spec.md` |
| 13 | M3 × 8 mm screws + brass inserts | — | 12 | ~€0.10 ea | Local | — | 4× ESP32 standoffs, 2× PSU bracket, **2× mains cable clamp**, 4× spare |
| 14 | Schuko captive mains lead | H05VV-F 3×0.75 mm², CEE 7/7 plug, ≥ 1.5 m | 1 | ~€2 | Local / scavenged | — | Mains entry; outer jacket clamped inside box; conductors go to PSU L/N/PE screws |
| 15 | Heat-shrink tubing | 2 mm, 4 mm, 6 mm assorted | 1 pack | ~€2 | Local / AliExpress | — | Insulate all solder joints; mandatory on every mains conductor |
| 16 | Cable ties (zip-ties) | 2.5 × 100 mm | 1 pack | ~€1 | Local | — | Strain-relief anchors for 2× lamp cables inside box |

> **Total estimated cost (excluding PSU):** ~€35–45 — drops vs. v1 because IEC C14 inlet, screw terminal block and PG9 glands are eliminated. PSU is user-owned.

---

## Power Budget

| Component | Voltage | Max Current | Typical @ 50 % brightness |
|-----------|---------|-------------|--------------------------|
| SK6812 Lamp 1 — 60 LEDs × 60 mA (all channels) | 5 V | **3.60 A** | 0.90 A |
| SK6812 Lamp 2 — 60 LEDs × 60 mA (all channels) | 5 V | **3.60 A** | 0.90 A |
| ESP32 DevKit | 5 V (via onboard reg) | 0.50 A | 0.20 A |
| 74AHCT125 level shifter | 5 V | 0.02 A | 0.01 A |
| **Total** | 5 V | **7.72 A** | **2.01 A** |

> PSU minimum rating: 7.72 A ÷ 0.80 = **9.65 A** → use a **10 A (50 W) 5 V PSU**.
>
> Formula used: `N_leds × mA_per_channel × channels` — SK6812 4-channel at 20 mA/channel × 3 active channels max = 60 mA/LED worst-case.

---

## Voltage Drop (per lamp cable, 2 m run)

| Parameter | Value |
|-----------|-------|
| Cable gauge | 18 AWG |
| Resistance | ~21 mΩ/m |
| Round-trip at 2 m | 84 mΩ |
| Max current (1 m strip full load) | 3.6 A |
| Voltage drop | **0.30 V** |
| Strip supply voltage | **4.70 V** ✅ (SK6812 spec: 4.5–5.5 V) |

---

## Connector & Cable Entry Strategy

No cable glands or IEC inlet used — all box penetrations are 3D-printed features in the enclosure SCAD.

| Penetration | Hole | Strain relief | Connector |
|---|---|---|---|
| Mains AC entry (back wall) | Ø8 mm round | **Printed 2-screw cable clamp** (M3 inserts) pressing on jacket | None (captive Schuko lead); conductors → PSU L/N/PE screw terminals |
| Lamp 1 output (left wall) | Rectangular pocket ~9.5 × 6 mm with internal shoulder | Connector body trapped by pocket shoulder + internal zip-tie | **Panel-mounted JST SM 3-pin female**; male plug from lamp cable inserts from outside |
| Lamp 2 output (right wall) | Rectangular pocket ~9.5 × 6 mm with internal shoulder | As above | As above |
| USB-C OTA (front wall) | 12 × 8 mm slot | n/a (cable accessed only during flashing) | ESP32 onboard USB-C |

### JST SM 3-pin current headroom

JST SM is rated 3 A/contact; worst-case per lamp is 3.6 A (60 LEDs × 60 mA at 100% white). Mitigations:

- **WLED ABL** (auto brightness limiter) set to **2800 mA per output** in LED Preferences
- **OR** cap UI max brightness at ~85% via boot preset

Typical real-world ambient use (50% coloured) draws <1 A per lamp, so the headroom only matters for the synthetic worst case.
