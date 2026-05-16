# BOM — curtaincinemalights (Cinema Curtain LED Sync)

> Generated from specs.md §8 — 2026-05-16
> All dimensions from `tools/parts-register/parts.json` unless noted.

## Components

| # | Component | Spec | Qty | Unit Price | Supplier | Part No. | Notes |
|---|-----------|------|-----|------------|----------|----------|-------|
| 1 | SK6812 RGBW LED strip | 5V, 60 LED/m, IP20, 4-pin (GRBW), 10mm wide | ~3 m (180 LEDs) | ~€8/m | AliExpress / BTF-Lighting | — | **Measure curtain width first** — order cut length + 10 cm slack; 1 m min per order |
| 2 | ESP8266 LOLIN D1 Mini v4 | ESP-12F, 4MB flash, USB-C, 34.2 × 25.6 × 10 mm | 1 | ~€3 | AliExpress / LCSC | C701341 variant | No native mounting holes — friction pocket in enclosure |
| 3 | Hi-Link HLK-20M05 | 5V 4A 20W AC-DC module, DIP, 56 × 32 × 22.5 mm | 1 | ~€4 | LCSC | C465406 | ⚠️ WLED ABL must be ≤ 3200 mA; upgrade to HLK-30M05 if adding more LEDs |
| 4 | Aluminium LED channel (U-profile) | 12–16 mm wide with frosted diffuser lid, cut to curtain width | 1 length | ~€4/m | Local / LUMINES | Type-Z or equiv. | Cut on site; conducts heat away from curtain fabric |
| 5 | 74AHCT125 level shifter | DIP-14, 7.62 mm row pitch, 19.05 × 6.35 × 4.57 mm | 1 | ~€0.30 | LCSC | C57369 | Buffers 3.3 V GPIO → 5 V SK6812 data; uses 1 of 4 gates |
| 6 | 330 Ω resistor | ¼ W, through-hole | 1 | <€0.01 | LCSC | C119313 | Series on GPIO2 data line (ESP8266 side of shifter) — ⚠️ C57436 is 10kΩ (MFR0W4F1002A50), not 330Ω |
| 7 | JST SM 3-pin connector pair | 2.5 mm pitch, M+F pair | 1 pair | ~€0.30 | On hand | — | Female panel-mount in box wall pocket; male plug on strip cable |
| 8 | 3-conductor cable | 20 AWG (or 2× 18 AWG power + 26 AWG data) flex | ~curtain width + 1 m | ~€1.50/m | Local electrical | — | Power + data to strip; route inside curtain rail bracket channel |
| 9 | Schuko captive mains lead | H05VV-F 3×0.75 mm², CEE 7/7 plug, ≥ 1.5 m | 1 | ~€2 | Local / scavenged | — | Mains entry to PSU; strain-relieved inside enclosure via printed cable clamp |
| 10 | Inline blade fuse holder | 5 × 20 mm, wire-mount | 1 | ~€0.50 | Local / LCSC | — | 4 A slow-blow fuse on 5 V rail after PSU output |
| 11 | 4 A slow-blow fuse | 5 × 20 mm | 2 | ~€0.20 ea | Local | — | 1 installed, 1 spare |
| 12 | Heat-shrink tubing | 2 mm, 4 mm, 6 mm assorted | 1 pack | ~€2 | Local | — | All solder joints; mandatory on mains conductors |
| 13 | 3D-printed enclosure | PETG/ASA, ~106 × 46 × 44 mm | 1 | ~€1.50 filament | Self-printed | — | See `mechanical/enclosure/curtaincinemalights-enclosure.scad` |
| 14 | Cable ties (zip-ties) | 2.5 × 100 mm | 1 pack | ~€1 | Local | — | Mains cable strain relief inside box |
| 15 | 1000 µF / 10 V capacitor | Electrolytic, radial | 1 | ~€0.20 | LCSC | — | Across PSU 5 V output; prevents voltage dip on LED color transitions |

> **Total estimated cost:** ~€25–35 depending on LED strip length and whether D1 Mini / PSU are on hand.

---

## Power Budget

Dimensions source: `tools/parts-register/parts.json` (IDs: `D1_MINI_V4`, `HLK_20M05`, `SK6812_RGBW_60`).

| Component | Voltage | Max Current | Typical @ 25 % brightness |
|-----------|---------|-------------|--------------------------|
| SK6812 Curtain — 180 LEDs × 60 mA (all channels, worst case) | 5 V | **10.80 A** | 0.67 A |
| SK6812 Curtain — **WLED ABL cap 3200 mA** | 5 V | **3.20 A** | 0.67 A |
| ESP8266 D1 Mini | 5 V (via onboard LDO) | 0.30 A | 0.18 A |
| 74AHCT125 level shifter | 5 V | 0.02 A | 0.01 A |
| **Total (ABL-limited)** | 5 V | **3.52 A** | **0.86 A** |

> PSU minimum: 3.52 A ÷ 0.80 safety factor = **4.4 A** — HLK-20M05 (4A) is marginal but works at
> ambient room temperature with ABL at 3200 mA. Set WLED LED Preferences → "Max current" = **3200 mA**.
> If operating in a warm enclosure or planning more than 3 m strip: use **HLK-30M05 (6A)** instead.
>
> Formula: `N_leds × mA_per_channel × channels` — SK6812 4-channel at 20 mA/ch × 3 active = 60 mA/LED worst-case.

---

## Voltage Drop (strip cable, 1.5 m run)

| Parameter | Value |
|-----------|-------|
| Cable gauge | 20 AWG |
| Resistance | ~33 mΩ/m |
| Round-trip at 1.5 m | 99 mΩ |
| Max current at ABL cap | 3.2 A |
| Voltage drop | **0.32 V** |
| Strip supply voltage | **4.68 V** ✅ (SK6812 spec: 4.5–5.5 V) |

> Power inject midpoint at LED 90 (1.5 m) using a separate 2-conductor cable from the PSU 5 V rail.
> Without mid-inject, far-end voltage at 3.2 A through 3 m of 20 AWG ≈ 4.36 V — borderline.
> **Recommended: inject at strip midpoint (LED 90) to guarantee ≥ 4.5 V at all pixels.**

---

## Connector & Cable Entry Strategy

| Penetration | Hole | Strain relief | Connector |
|---|---|---|---|
| Mains AC entry (back wall) | Ø9 mm round | Printed 2-screw cable clamp (M3 × 8, brass inserts) pressing on jacket | None (captive Schuko lead); conductors → HLK-20M05 L/N/PE pins |
| LED strip output (left wall) | Rectangular pocket 9.5 × 6 mm (from `JST_SM_2P5_3PIN` register) | Connector body trapped by pocket shoulder + zip-tie on cable inside box | Panel-mount JST SM 3-pin female; male plug from strip cable |
| USB-C OTA (front wall) | 9.0 × 3.5 mm slot (from `D1_MINI_V4` register) | n/a (cable accessed only during flashing) | D1 Mini onboard USB-C |
