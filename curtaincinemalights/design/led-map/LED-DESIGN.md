# LED Design — curtaincinemalights

> Curtain: two-panel, center-open, motorized
> Strip: single SK6812 RGBW run, 60 LED/m, in aluminium channel along curtain rail

---

## Physical Layout

```
Wall                               Ceiling
  │                                   │
  │  ◄── aluminium track + strip ──► │
  │  LED 0                  LED 179  │
  │  ├─────────────────────────────┤  │
  │  │  Left panel   Right panel  │  │
  │  │  0 → 89       90 → 179     │  │
  │  │                            │  │
  │  ▲ data in              data → │  │ (single data run, no mid-inject on data)
  │  (from box, JST SM female)     │  │
  │                                   │
  └───────────────────────────────────┘
```

- LED 0 = far left end of curtain track
- LED 89 = center-left (1 LED to the left of physical center)
- LED 90 = center-right (1 LED to the right of physical center)
- LED 179 = far right end of curtain track
- Power injection at both LED 0 (start of strip) and LED 90 (midpoint) — data is a single continuous run

---

## Segment Configuration

Both segments are on a **single physical WLED output (GPIO2)**.  
WLED version: v0.15 (ESP8266 branch — single output, segments are virtual software split).

| Segment | ID | LED range | WLED `rev` | Fill direction | Name |
|---------|----|-----------|------------|----------------|------|
| Left Panel | 0 | 0 – 89 | `true` (reversed) | From center outward → left | `Left Panel` |
| Right Panel | 1 | 90 – 179 | `false` (normal) | From center outward → right | `Right Panel` |

**Why reversed on Left Panel?**  
With `rev=true`, LED 89 (nearest center) is effectively LED index 0 of the reversed segment.
WLED's fill-based effects (State Sync `animation_mode: fill`) light from index 0 upward.
So with the left segment reversed, fill lights from center toward the left edge — exactly
matching the left curtain panel opening outward.

The right segment (`rev=false`) naturally lights from index 0 (LED 90, nearest center)
outward toward the right edge.

---

## Effect Behavior Mapping

| Curtain state | LED behavior | hacs-wledext-effects instance |
|---------------|--------------|-------------------------------|
| Fully closed (position = 0 %) | No LEDs lit (or a dim accent, configurable) | State Sync → 0 % fill = dark |
| Partially open (e.g. 50 %) | Center 50 % of each half lit, warm amber | State Sync fill ← `sensor.cinema_curtain_position` |
| Fully open (position = 100 %) | All LEDs lit, warm amber, then transition to Rainbow Wave | State Sync 100 %, then Rainbow Wave |
| Opening (cover.state = `opening`) | Chase effect sweeping outward on both halves | Chase (both segments) |
| Closing (cover.state = `closing`) | Chase effect sweeping inward on both halves | Chase (both segments, direction reversed) |
| Cinema mode (projector `playing`) | Dim red, slow breathe; all other effects paused | Breathe (master) |

---

## WLED cfg.json Segment Definitions

```json
"seg": [
  {
    "id": 0, "start": 0,  "stop": 89,
    "name": "Left Panel",  "rev": true,
    "col": [[255, 147, 41, 30]], "fx": 0
  },
  {
    "id": 1, "start": 90, "stop": 179,
    "name": "Right Panel", "rev": false,
    "col": [[255, 147, 41, 30]], "fx": 0
  }
]
```

`col`: [R=255, G=147, B=41, W=30] — warm amber with slight warm-white channel.
`fx: 0` = static (hacs-wledext-effects overrides this when an effect is active).

---

## Adjusting LED Count for Different Curtain Widths

| Curtain width | LED count | Segment split |
|---------------|-----------|---------------|
| 2.0 m | 120 LEDs | 0–59 + 60–119 |
| 2.5 m | 150 LEDs | 0–74 + 75–149 |
| 3.0 m (default) | 180 LEDs | 0–89 + 90–179 |
| 3.5 m | 210 LEDs | 0–104 + 105–209 |
| 4.0 m | 240 LEDs | 0–119 + 120–239 |

To adjust: in WLED web UI → LED Preferences → change total LED count and both segment stop values.
Or edit `firmware/cfg.json` manually and reflash / reupload.

> **ESP8266 buffer limit:** WLED v0.15 on ESP8266 supports ≤ ~500 LEDs on one output but JSON
> API calls are batched at ~150 LED chunks. All counts in the table above are within safe limits.

---

## Colour Presets

| Preset | Effect | Colour | Notes |
|--------|--------|--------|-------|
| 1 — Warm Amber | Solid | R255 G147 B41 W30 | Boot default; nice ambient when curtain partially open |
| 2 — Cinema Dim | Solid / Breathe | R180 G0 B0 W0 | Loaded by HA automation when projector starts |
| 3 — Ambient Wave | Rainbow Wave | — | Loaded by HA automation when curtain fully open (non-cinema) |
