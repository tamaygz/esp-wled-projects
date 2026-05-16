# PRD: curtaincinemalights — Cinema Curtain LED Sync

- **Version**: 1.0
- **Date**: 2026-05-16
- **Status**: `wip`

---

## 1. Concept

A single SK6812 RGBW LED strip (60 LED/m) runs along an aluminium channel profile mounted
on the L-shaped wall brackets of a motorized cinema-style curtain rail, between the wall and
the red curtain fabric. The strip illuminates the gap between wall and curtain, creating a
dynamic halo that mirrors the exact position and movement of the two curtain panels in
real time.

When the curtain opens (two panels from center toward the sides), the LEDs follow: the
center LEDs light first and the lit zone spreads outward — always at the same percentage as
the actual curtain opening. When the curtain closes, the reverse. Cinema mode (projector
playing) switches to a slow dim red breathe; non-cinema mode transitions back to ambient.

The system runs on an **ESP8266 LOLIN D1 Mini** with WLED v0.15 (ESP8266 branch), and all
state-driven effects are orchestrated by **hacs-wledext-effects** (State Sync + Chase +
Breathe) reacting to Home Assistant entities for the motorized cover and media player.

---

## 2. Requirements

- [x] LED type: SK6812 RGBW 60 LED/m, IP20, 5V, GRB+W order, aluminium channel with diffuser
- [x] LED count: 60 × curtain_width_m — plan for 3 m ≈ **180 LEDs** (two virtual half-segments of 90)
- [x] Power: 230 V AC mains → Hi-Link HLK-20M05 (5V 4A) inside enclosure; WLED ABL = 3200 mA
- [x] Mounting: aluminium U-channel profile on L-bracket curtain rail wall mounts; diffusing cover
- [x] Connectivity: 2.4 GHz Wi-Fi (WLED captive portal, then station mode)
- [x] Smart home integration: Home Assistant via native WLED integration (mDNS auto-discovery)
- [x] hacs-wledext-effects: yes — State Sync, Chase, Breathe, Rainbow Wave (see §6)
- [x] Sound-reactive: no
- [x] Outdoor / indoor: indoor (IP20 strip, IP20 enclosure)
- [x] IP rating: IP20 (protected from direct contact; no moisture)

---

## 3. Constraints

- Budget: ~€40 (excluding existing PSU / D1 Mini if on hand)
- Enclosure size max: 120 × 55 × 50 mm — must fit on shelf or inside curtain alcove
- Power availability: 230 V AC socket near curtain rail; no low-voltage DC available on rail
- ESP8266 constraint: WLED v0.15 branch (legacy); single output only; ~150 LED buffer limit
  per JSON API batch — hacs-wledext-effects auto-batches
- Curtain width variable: 2–4 m; WLED LED count configurable in web UI post-flash
  (default config uses 180 LEDs = 3 m; adjust `leds.ins[0].len` in cfg.json or WLED UI)

---

## 4. Mechanical

- Control box: 3D-printed YAPP_Box (PETG/ASA), snap-on lid
- Box outer target: 106 × 46 × 44 mm (inner: 100 × 40 × 35 mm)
- Wall thickness: 3.0 mm
- PSU (HLK-20M05, 56 × 32 × 22.5 mm) and D1 Mini (34.2 × 25.6 × 10 mm) both in base shell
- D1 Mini held in friction-fit pocket (no native mounting holes); PSU held by side-wall ribs
- Aluminium LED channel profile: standard U-profile 12–16 mm wide with clear/frosted diffuser lid
  — length = curtain track width; cut to measure on site

---

## 5. Acceptance Criteria

- [ ] All LEDs addressable at WLED startup; no flickering at 50 % brightness
- [ ] WLED web UI reachable on local network as `curtaincinemalights.local`
- [ ] Both WLED segments (Left Panel, Right Panel) independently controllable from WLED UI
- [ ] Auto-discovered in Home Assistant within 60 s of WLED boot; on/off, brightness, colour verified
- [ ] Template sensor `sensor.cinema_curtain_position` reads cover position correctly
- [ ] State Sync effect on both segments tracks curtain position (center fill, L and R match)
- [ ] Chase effect activates on opening/closing transitions and deactivates when motion stops
- [ ] Breathe (dim red) activates when `media_player.projector` enters `playing` state
- [ ] Breathe stops and ambient mode resumes when projector leaves `playing` state
- [ ] PSU thermal: enclosure surface ≤ 60 °C after 30-min continuous operation
- [ ] Enclosure closed, cable strain-relieved, no exposed mains conductors
- [ ] All hacs-wledext-effects entities documented below with actual entity IDs

---

## 6. Home Assistant

> **Mandatory** — every project in this repo must be controllable from Home Assistant via the
> native WLED integration (auto-discovered via mDNS).

- **Device mDNS hostname:** `curtaincinemalights`
  (set in `firmware/cfg.json` → `"id": {"mdns": "curtaincinemalights"}` and `"nw": {"mdns": 1}`)

### 6.1 Native WLED Integration Entities

| Entity ID | Description |
|-----------|-------------|
| `light.curtaincinemalights` | Master light (both segments) |
| `light.curtaincinemalights_left_panel` | Segment 0 — Left panel (LEDs 0–89, reversed) |
| `light.curtaincinemalights_right_panel` | Segment 1 — Right panel (LEDs 90–179, normal) |

### 6.2 Helper Entities to Create in HA

| Entity ID | Type | Purpose |
|-----------|------|---------|
| `sensor.cinema_curtain_position` | Template sensor | Exposes `cover.cinema_curtain` `current_position` attribute (0–100 %) as a numeric sensor for hacs-wledext-effects State Sync |
| `input_boolean.cinema_mode_active` | Input boolean | Manual override — set `on` to force cinema Breathe regardless of projector state |

Template sensor YAML (add to `configuration.yaml` or in the Template integration UI):
```yaml
template:
  - sensor:
      - name: "Cinema Curtain Position"
        unique_id: cinema_curtain_position_sensor
        state: "{{ state_attr('cover.cinema_curtain', 'current_position') | int(0) }}"
        unit_of_measurement: "%"
        device_class: power_factor
        state_class: measurement
```

### 6.3 hacs-wledext-effects

**Installation:**
1. Add HACS custom repo `https://github.com/tamaygz/hacs-wledext-effects` (category: Integration)
2. Install "WLED Effects" → restart HA
3. Settings → Devices & Services → Add → "WLED Effects" → select `curtaincinemalights` device

**Effects to install and configure:**

| Effect | Instance Name | Segment | Config notes |
|--------|--------------|---------|-------------|
| **State Sync** | `ccl_left_state_sync` | Left Panel (seg 0) | `state_entity: sensor.cinema_curtain_position`, `min_value: 0`, `max_value: 100`, `animation_mode: fill`, color warm amber `255,147,41` |
| **State Sync** | `ccl_right_state_sync` | Right Panel (seg 1) | Same config; segment is not reversed in effect — the WLED segment itself is reversed so fill naturally goes center→left |
| **Chase** | `ccl_chase_left` | Left Panel | Triggered on `opening` state; direction outward |
| **Chase** | `ccl_chase_right` | Right Panel | Triggered on `opening` state; direction outward |
| **Breathe** | `ccl_cinema_breathe` | Both (master) | `pulse_rate: 0.3`, dim red `180,0,0`, brightness 40; active during projector `playing` |
| **Rainbow Wave** | `ccl_ambient_rainbow` | Both (master) | Idle/ambient when curtain fully open and no cinema mode |

**Expected effect switch entities:**

| Entity ID | Effect |
|-----------|--------|
| `switch.wled_context_effects_ccl_left_state_sync` | Left panel curtain position |
| `switch.wled_context_effects_ccl_right_state_sync` | Right panel curtain position |
| `switch.wled_context_effects_ccl_chase_left` | Left panel opening chase |
| `switch.wled_context_effects_ccl_chase_right` | Right panel opening chase |
| `switch.wled_context_effects_ccl_cinema_breathe` | Cinema mode breathe |
| `switch.wled_context_effects_ccl_ambient_rainbow` | Ambient rainbow wave |

### 6.4 Automation Logic Summary

See `design/effects/ha-automations.yaml` for full YAML.

| Trigger | Action |
|---------|--------|
| `cover.cinema_curtain` → `opening` | Stop State Sync; start Chase both panels (outward) |
| `cover.cinema_curtain` → `closing` | Stop State Sync; start Chase both panels (inward) |
| `cover.cinema_curtain` → `open` or `closed` | Stop Chase; resume State Sync / Rainbow Wave |
| `cover.cinema_curtain` position changes (stationary) | State Sync updates automatically via sensor |
| `media_player.projector` → `playing` | Stop all effects; start Cinema Breathe |
| `media_player.projector` → `idle` / `off` | Stop Cinema Breathe; resume State Sync or Rainbow Wave |

---

## 7. Open Questions

- [ ] Exact curtain width (measure on site → update `leds.ins[0].len` in WLED)
- [ ] HA entity IDs for `cover.cinema_curtain` and `media_player.projector` (confirm from HA instance)
- [ ] Confirm actual hacs-wledext-effects entity ID suffix format after first install
- [ ] Level shifter: 74AHCT125 recommended for ESP8266 → 5V SK6812; verify if direct GPIO2 works reliably at install
- [ ] IP rating of aluminium track / diffuser — confirm IP20 acceptable (not near open window)

---

## 8. Power Budget

| Component | Voltage | Max Current | Typical @ 25 % brightness |
|-----------|---------|-------------|--------------------------|
| SK6812 — 180 LEDs × 60 mA/LED (worst case all white) | 5 V | **10.80 A** | ~0.67 A |
| SK6812 — 180 LEDs × 60 mA (WLED ABL cap: 3200 mA) | 5 V | **3.20 A** | ~0.67 A |
| ESP8266 D1 Mini | 5 V (onboard reg) | 0.30 A | 0.18 A |
| 74AHCT125 level shifter | 5 V | 0.02 A | 0.01 A |
| **Total (ABL capped)** | 5 V | **3.52 A** | **0.86 A** |

> PSU: HLK-20M05 rated 4A. Load at ABL cap = 3.52A = **88 % of rated current** — acceptable for
> continuous operation at ambient temperature. If usage ever peaks near 100 % brightness (white),
> reduce ABL to 3000 mA or upgrade to HLK-30M05 (6A).

---

## 9. Changelog

| Date | Change |
|------|--------|
| 2026-05-16 | Initial spec |
