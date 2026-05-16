# BOM — Reefs (Driftwood Ambient Lamps)

> Generated from specs.md §8.2 — 2026-05-16

## Components

| # | Component | Spec | Qty | Source | Notes |
|---|-----------|------|-----|--------|-------|
| 1 | SK6812 RGBW LED strip | 5 V, 60 LED/m, IP30, 4-pin (GRBW) | 2 × 1 m (60 LEDs each) | AliExpress / local | Order 1.1 m per lamp; trim to fit |
| 2 | ESP32 DevKit (38-pin) | ESP32-WROOM-32, USB-C preferred | 1 | LCSC C701341 / AliExpress | Any 38-pin pinout works |
| 3 | Honeywell 5 V PSU | 5 V DC, ≥ 10 A (50 W) | 1 | User-specified | Verify nameplate rating ≥ 10 A |
| 4 | Aluminium LED channel | U-profile with diffuser, 12 mm wide, ≥ 1 m | 2 | e.g., LUMINES Type-Z | Conducts heat away from wood |
| 5 | 3-conductor cable | 18 AWG power + 26 AWG data, or 3-core 20 AWG flex | 2 × 2.5 m | — | 0.5 m slack; one cable per lamp |
| 6 | 330 Ω resistor | ¼ W, through-hole | 2 | — | Series on GPIO data line at ESP32 side |
| 7 | 74AHCT125 level shifter | SO-14 or DIP-14 | 1 | — | 3.3 V → 5 V for SK6812 data; 2 channels used |
| 8 | Blade fuse holder (inline) | 5 × 20 mm, panel or wire mount | 2 | — | One per lamp 5 V power run |
| 9 | 5 A blade fuse | 5 × 20 mm slow-blow | 4 | — | 2 installed + 2 spare |
| 10 | JST SM 3-pin connector (M+F pair) | 5 A rated | 2 pairs | — | Detachable lamp connection point |
| 11 | Screw terminal block | 5 mm pitch, 4-pos | 1 | — | PSU → bus distribution inside control box |
| 12 | 3D-printed enclosure | ~150 × 100 × 60 mm PETG/ASA | 1 | Self-printed | See `mechanical/enclosure/MODELS.md` |
| 13 | M3 × 8 mm screws + brass inserts | — | 8 | — | Mount ESP32 and PSU bracket |
| 14 | IEC C14 inlet with switch + fuse | Chassis mount, 2 A slow-blow | 1 | — | Mains entry to control box |
| 15 | Heat-shrink tubing | 2 mm, 4 mm, 6 mm assorted | 1 pack | — | Insulate all solder joints |
| 16 | Cable gland PG9 | Nylon, IP54 | 2 | — | One per lamp cable entry into enclosure |

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
