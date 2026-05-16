# LED Map & Effects Design — Reefs

## Physical Layout

Two separate 1 m SK6812 RGBW strips, each mounted in an aluminium U-channel on the **rear face** of one driftwood piece (wall-facing). Light washes the wall; the room-facing side of the wood stays dark.

```
LAMP 1 — Driftwood piece A
  Strip direction (DIN end at JST connector, left side of lamp)

  [0] [1] [2] [3] ... [57] [58] [59]
   ◀─────────────────────────────────
   DIN                            end
   (JST connector end)

LAMP 2 — Driftwood piece B (identical layout)

  [60] [61] [62] ... [117] [118] [119]   ← universe indices
    [0]  [1]  [2] ...  [57]  [58]  [59]  ← local strip indices
```

Both strips are addressed as a single 120-LED WLED universe split into two segments.

---

## Segment Plan

| Segment | WLED Index | Start LED | End LED | GPIO | Description |
|---------|------------|-----------|---------|------|-------------|
| 0 | Segment 0 | 0 | 59 | GPIO 16 | Lamp 1 — left driftwood piece |
| 1 | Segment 1 | 60 | 119 | GPIO 17 | Lamp 2 — right driftwood piece |

WLED output configuration:
- Output 1: GPIO 16, type SK6812 RGBW, count 60, colour order GRBW, start 0
- Output 2: GPIO 17, type SK6812 RGBW, count 60, colour order GRBW, start 60

> Each segment maps to one Home Assistant light entity: `light.reef_lamps_lamp_1` and `light.reef_lamps_lamp_2`.

---

## Preset Design

Presets are stored in `firmware/presets.json` and exported from the WLED web UI.

| # | Name | Effect | Palette / Colour | Speed | Brightness | Notes |
|---|------|--------|------------------|-------|-----------|-------|
| 1 | Warm Ambient | Solid (fx 0) | RGBW (255,180,100,200) | — | 40% (102) | Boot preset — warm amber glow |
| 2 | Reef Calm | Colorwaves (fx 65) | Ocean (pal 11) | Slow (30) | 30% (77) | Slow shifting blue-teal |
| 3 | Night Glow | Solid (fx 0) | RGBW (255,140,40,255) | — | 10% (26) | Very dim warm for night use |

---

## White Channel Strategy (SK6812 RGBW)

SK6812 has an independent white LED channel. WLED controls it via the W value in RGBW colour.

| Use case | Recommended RGBW values | Notes |
|----------|------------------------|-------|
| Warm white (3000 K) | (255, 140, 40, 200) | Mix warm RGB with white channel |
| Cool white (6500 K) | (150, 180, 255, 255) | Blue shift + high W |
| Max output / photo | (255, 255, 255, 255) | All channels full |
| Night mode | (255, 140, 40, 255) | Low brightness setting |
| Effects only | RGB colour, W=0 | Disable white channel for vivid colour effects |

---

## Useful WLED Effects (for ambience)

| Effect ID | Name | Recommended Use |
|-----------|------|-----------------|
| 0 | Solid | Boot preset, night mode |
| 65 | Colorwaves | Reef calm — slow ocean waves |
| 91 | Flow | Gentle colour drift |
| 38 | Ripple | Active ambient |
| 45 | Fire 2012 | Warm flame effect |
| 55 | Breathe | Soft pulsing alert / mood |
| 26 | Chase | Party / active mode |
