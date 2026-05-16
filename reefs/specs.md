# PRD: Reefs — WLED Driftwood Ambient Lighting

- **Version**: 1.0  
- **Date**: 2026-05-16  
- **Status**: Draft — awaiting owner review

---

## 1. Product Overview

### 1.1 Document Title and Version

- PRD: Reefs — WLED Driftwood Ambient Lighting
- Version: 1.0

### 1.2 Product Summary

**Reefs** is a DIY ambient lighting installation built around two pieces of natural driftwood. Each piece of driftwood acts as a self-contained lamp: an SK6812 RGBW LED strip is mounted on the back face of the wood (facing the wall), casting diffused, coloured light onto the wall behind it. The room-facing side of each piece remains unlit, framing the glow naturally through the wood grain and texture.

Both lamps are powered and controlled from a single 3D-printed control box housing an ESP32 running WLED and a Honeywell 5 V PSU. WLED exposes each lamp as an independent segment — or optionally a dedicated channel — and integrates with Home Assistant via the native WLED integration, enabling scene-level control and automations.

The project is intended as a permanent room installation with no exposed wiring, a single mains connection, and full smart-home integration out of the box.

### 1.3 Executive Summary

| | |
|---|---|
| **Problem Statement** | Standard ambient lamps offer no physical texture or organic character; smart LED solutions typically require bulky off-the-shelf fixtures that cannot be adapted to natural materials. |
| **Proposed Solution** | Mount RGBW LED strips on the rear face of two driftwood pieces, fed from one centralised ESP32/WLED control box, producing wall-wash ambient light that is individually controllable from Home Assistant. |
| **Success Criteria** | (1) Both lamps respond to WLED commands within 200 ms over Wi-Fi. (2) Each lamp is independently controllable as a Home Assistant light entity. (3) Full-white output at 50 % brightness draws ≤ 4 A total from the PSU. (4) All wiring is concealed inside channels, conduit, or the driftwood profile. (5) The control box fits within a 150 × 100 × 60 mm 3D-printed enclosure. |

---

## 2. Goals

### 2.1 Project Goals

- Deliver two functional ambient lamps with distinct, independently addressable WLED segments.
- Centralise power and control in one enclosure with a single mains input.
- Achieve full Home Assistant integration so both lamps appear as individual light entities.
- Produce a repeatable, documented build that can be reproduced or extended.

### 2.2 Owner Goals

- Individual brightness and colour/white control per lamp.
- Integration with Home Assistant automations (e.g., sunset scene, movie mode).
- Reliable operation at ambient brightness levels (20–60 % typical) with no flicker.
- Clean, furniture-grade finish — no visible wiring between driftwood and control box.

### 2.3 Non-Goals

- Audio-reactive features (not in scope for v1).
- Battery / portable operation.
- More than two lamp segments per control box in this revision.
- Mobile app beyond WLED's built-in web UI and HA integration.
- Any mains-side electrical work beyond plugging in the PSU (handled separately / by qualified person).

---

## 3. User Personas

### 3.1 Key User Types

- **Builder / Maker** — assembles the hardware, flashes WLED, configures HA.
- **Resident / Daily User** — operates lamps via HA dashboard, voice, or automations.

### 3.2 Persona Details

- **Builder**: Comfortable with soldering, ESP32 toolchains, and basic 3D printing. Needs precise wiring specs, pin assignments, and WLED config values — not guesswork.
- **Resident**: Wants one-tap scene activation, consistent behaviour, and no maintenance. Does not interact with WLED UI directly after initial setup.

### 3.3 Role-Based Access

| Role | Access Level |
|---|---|
| Builder | Full WLED web UI, OTA flashing, physical enclosure access |
| Resident | Home Assistant only — light entities, scenes, automations |

---

## 4. Functional Requirements

### 4.1 Lamp Control

**Priority: High**

- `GH-001`: As a resident, I want to turn Lamp 1 and Lamp 2 on/off independently via Home Assistant so that I can use each lamp in separate scenes.
  - **AC**: Each lamp maps to exactly one HA light entity; toggling one does not affect the other.
- `GH-002`: As a resident, I want to set brightness (1–100 %) and colour temperature (warm white ↔ cool white) per lamp so that I can adapt the mood to the time of day.
  - **AC**: Brightness changes are visible within 200 ms; colour temperature range spans at least 2700 K–6500 K via SK6812 RGBW white channel blending.
- `GH-003`: As a resident, I want to apply WLED effects (e.g., slow colour breathe, fire, candlelight) per lamp independently so that lamps can display different effects simultaneously.
  - **AC**: Any of the standard WLED effect presets can be applied to Lamp 1 without changing Lamp 2's current preset.

### 4.2 Home Assistant Integration

**Priority: High**

- `GH-004`: As a builder, I want WLED to auto-discover in Home Assistant via the native WLED integration so that no manual YAML configuration is required.
  - **AC**: Both lamps appear as separate HA entities within 60 s of WLED booting on the local network, with no manual YAML.
- `GH-005`: As a resident, I want a "Reef Scene" HA script that activates a slow-shifting warm colour preset on both lamps simultaneously so that one tap sets the room ambience.
  - **AC**: The scene sets both lamps to the designated preset within 500 ms.

### 4.3 Power & Safety

**Priority: High**

- `GH-006`: As a builder, I want the PSU to remain below 80 % rated load at maximum typical brightness so that there is thermal headroom for continuous operation.
  - **AC**: Calculated peak draw (see §8 Power Budget) ≤ 80 % of PSU rated current at 5 V.
- `GH-007`: As a builder, I want a 5 A blade fuse inline on each 5 V power run to the strips so that a wiring fault cannot damage the PSU or start a fire.
  - **AC**: Each lamp's power feed has a dedicated inline fuse rated ≤ 5 A before the first LED.

### 4.4 Physical Build

**Priority: High**

- `GH-008`: As a builder, I want the LED strip to be mounted on the rear face of the driftwood using aluminium channel / diffuser profile so that heat is conducted away from the wood and the light is diffused evenly.
  - **AC**: Strip operating temperature at 50 % brightness ≤ 45 °C measured on the strip backing after 60 min continuous operation.
- `GH-009`: As a builder, I want all inter-device wiring to run inside 10 mm cable management channels or behind baseboard so that no loose wires are visible in the finished installation.
  - **AC**: Zero exposed wire segments visible from the room-facing side of either lamp or the floor.

---

## 5. User Experience & Functionality

### 5.1 First-Time Setup Flow

1. Flash WLED to ESP32 via USB before enclosure assembly.
2. Connect ESP32 to home Wi-Fi via WLED's captive portal (AP mode on first boot).
3. In WLED web UI, configure two LED outputs (GPIO 16 → Lamp 1, GPIO 17 → Lamp 2) with correct LED count and SK6812 type.
4. Install WLED integration in Home Assistant → auto-discovers both segments as light entities.
5. Assign entities to a room; create "Reef Scene" script.
6. Power-cycle test: both lamps illuminate to startup preset within 3 s.

### 5.2 Day-to-Day Operation

- **Standard use**: Resident taps HA dashboard tile or scene button; lamps respond within 200 ms.
- **Automation**: Lamps activate at sunset to warm preset; dim to 10 % at 23:00; turn off at 00:00.
- **Effect switching**: Resident can pick any WLED preset from HA's light card effects list.

### 5.3 Edge Cases

| Scenario | Expected Behaviour |
|---|---|
| Wi-Fi drops | WLED keeps current state; reconnects automatically; HA shows "unavailable" until reconnect |
| Power cycle | WLED restores last known state from flash within 3 s |
| One lamp data wire disconnected | That segment shows error in WLED UI; other lamp unaffected |
| PSU overload (unlikely) | Inline fuse blows; only one lamp affected if fuses per-lamp |

### 5.4 Physical UX Notes

- No physical buttons required for v1 (HA + WLED web UI sufficient).
- Control box mounts in a concealed location (shelf interior, behind furniture) — not a decorative item.
- USB-C port on ESP32 must remain accessible through enclosure wall for OTA recovery.

---

## 6. Narrative

A homeowner powers on their living room at dusk. Home Assistant triggers the "Reef Scene" — both driftwood pieces begin emitting a slow warm amber glow from their rear faces, painting the wall behind them with organic pools of light filtered through the wood texture. Each lamp is an independent entity: one shifts to a gentle blue-white for reading while the other holds a warm flicker for ambience. All of this runs from a single small 3D-printed box tucked behind a shelf, fed by one mains lead, requiring zero maintenance beyond occasional OTA firmware updates pushed from Home Assistant.

---

## 7. Success Metrics

### 7.1 Build Quality Metrics

| Metric | Target |
|---|---|
| WLED command-to-lamp latency | ≤ 200 ms (LAN, measured with WLED HTTP API) |
| HA entity discovery time | ≤ 60 s from WLED boot |
| Strip operating temperature at 50 % brightness | ≤ 45 °C after 60 min |
| Total PSU draw at full white, 100 % brightness | ≤ rated PSU current × 80 % |
| Visible exposed wiring | 0 segments |

### 7.2 Reliability Metrics

| Metric | Target |
|---|---|
| WLED uptime between reboots | ≥ 30 days (no watchdog resets) |
| Wi-Fi reconnect after router restart | ≤ 30 s |
| State restore after power cut | Correct last-state within 3 s |

---

## 8. Technical Specifications

### 8.1 System Architecture

```
MAINS (230 V AC)
       │
       ▼
┌─────────────────────────────────────────────────┐
│               CONTROL BOX (3D-printed)          │
│                                                 │
│  ┌───────────────────┐   ┌───────────────────┐  │
│  │  Honeywell 5 V    │   │     ESP32 DevKit  │  │
│  │  PSU              │──▶│     (WLED)        │  │
│  │  (≥ 10 A / 50 W)  │5V │                   │  │
│  └────────┬──────────┘   │  GPIO16 ──[330Ω]─┼──┼──▶ DATA Lamp 1
│           │              │  GPIO17 ──[330Ω]─┼──┼──▶ DATA Lamp 2
│           │5V/GND        │                   │  │
│           ├──[5A fuse]───┼───────────────────┼──┼──▶ 5V/GND Lamp 1
│           └──[5A fuse]───┼───────────────────┼──┼──▶ 5V/GND Lamp 2
│                          └───────────────────┘  │
│  [ USB-C port accessible on enclosure wall ]    │
└─────────────────────────────────────────────────┘
          │                         │
    2 m run                   2 m run
    18 AWG (5V, GND)          18 AWG (5V, GND)
    26 AWG (DATA)             26 AWG (DATA)
          │                         │
          ▼                         ▼
  ┌───────────────┐         ┌───────────────┐
  │  DRIFTWOOD    │         │  DRIFTWOOD    │
  │  Lamp 1       │         │  Lamp 2       │
  │               │         │               │
  │  [aluminium   │         │  [aluminium   │
  │   LED channel]│         │   LED channel]│
  │  SK6812 RGBW  │         │  SK6812 RGBW  │
  │  strip (rear) │         │  strip (rear) │
  └───────────────┘         └───────────────┘
       wall-wash                  wall-wash
       (wall side)                (wall side)
```

### 8.2 Bill of Materials

| # | Component | Spec | Qty | Notes |
|---|---|---|---|---|
| 1 | SK6812 RGBW LED strip | 5 V, 60 LED/m, IP30, 4-pin | 2 × **1 m** (60 LEDs each) | Order 1.1 m per lamp to allow for trimming to fit |
| 2 | ESP32 DevKit (38-pin) | ESP32-WROOM-32, USB-C preferred | 1 | Any 38-pin pinout works |
| 3 | Honeywell 5 V PSU | 5 V DC, ≥ 10 A (50 W) | 1 | User-specified; verify actual model current rating |
| 4 | Aluminium LED channel | U-profile with diffuser, 12 mm wide, ≥ strip length | 2 | e.g., LUMINES Type-Z or equivalent; conduct heat away from wood |
| 5 | 3-conductor cable | 18 AWG (power) + 26 AWG (data) **or** 3-core 20 AWG flex | 2 × 2.5 m | Adds 0.5 m slack; one cable per lamp |
| 6 | 330 Ω resistor | 1/4 W, through-hole | 2 | On data line at ESP32 GPIO; reduces signal ringing |
| 7 | 74AHCT125 level shifter | SO-14 or DIP-14 | 1 | 3.3 V → 5 V for SK6812 data; 2 channels used |
| 8 | Blade fuse holder (inline) | 5 × 20 mm, panel or wire mount | 2 | One per lamp 5 V power run |
| 9 | 5 A blade fuse | 5 × 20 mm slow-blow | 4 | 2 installed + 2 spare |
| 10 | JST SM 3-pin connectors (M+F pair) | 5 A rated | 2 pairs | Detachable connection at lamp entry point |
| 11 | Screw terminal block | 5 mm pitch, 4-pos | 1 | PSU → bus distribution in control box |
| 12 | 3D-printed enclosure | ~150 × 100 × 60 mm | 1 | See §8.5 |
| 13 | M3 × 8 mm screws + brass inserts | — | 8 | Mount ESP32 and PSU bracket |
| 14 | IEC C14 inlet with switch + fuse | Chassis mount, 2 A fuse | 1 | Mains entry to control box |
| 15 | Heat-shrink tubing assorted | 2 mm, 4 mm, 6 mm | 1 pack | Insulate all solder joints |
| 16 | Cable gland PG9 | Nylon, IP54 | 2 | One per lamp cable entry into enclosure |

> **Strip length confirmed**: 1 m per lamp (60 LEDs each, 120 LEDs total). The strip should span the full driftwood rear face length minus ~5 mm clearance each end. Trim to fit after dry-fitting the aluminium channel.

### 8.3 Power Budget

| Component | Voltage | Max Current | Typical (50 % brightness) |
|---|---|---|---|
| SK6812 Lamp 1 — 60 LEDs × 60 mA | 5 V | **3.60 A** | **0.90 A** |
| SK6812 Lamp 2 — 60 LEDs × 60 mA | 5 V | **3.60 A** | **0.90 A** |
| ESP32 DevKit | 5 V (via USB reg) | 0.50 A | 0.20 A |
| Level shifter 74AHCT125 | 5 V | 0.02 A | 0.01 A |
| **Total** | 5 V | **7.72 A** | **2.01 A** |

> PSU minimum rating: 7.72 A ÷ 0.80 = **9.65 A** → use a **10 A (50 W) 5 V PSU**.  
> Verify Honeywell PSU nameplate rating ≥ 10 A before finalising.

### 8.4 Wiring Detail

#### 8.4.1 Control Box Internal Wiring

```
IEC C14 Inlet
  ├── Live   ──▶  PSU L
  ├── Neutral ──▶  PSU N
  └── Earth  ──▶  PSU PE ──▶ enclosure ground screw

PSU +5V ──▶ Terminal Block V+
PSU GND ──▶ Terminal Block GND

Terminal Block V+  ──▶ [5A fuse] ──▶ JST Lamp 1 Pin 1 (5V)
Terminal Block GND ──▶             ──▶ JST Lamp 1 Pin 2 (GND)
Terminal Block V+  ──▶ [5A fuse] ──▶ JST Lamp 2 Pin 1 (5V)
Terminal Block GND ──▶             ──▶ JST Lamp 2 Pin 2 (GND)

ESP32 GPIO16 ──[330Ω]──▶ 74AHCT125 Channel A IN
                         74AHCT125 Channel A OUT ──▶ JST Lamp 1 Pin 3 (DATA)

ESP32 GPIO17 ──[330Ω]──▶ 74AHCT125 Channel B IN
                         74AHCT125 Channel B OUT ──▶ JST Lamp 2 Pin 3 (DATA)

74AHCT125 VCC ──▶ Terminal Block V+ (5V)
74AHCT125 GND ──▶ Terminal Block GND
ESP32 5V (Vin) ──▶ Terminal Block V+
ESP32 GND     ──▶ Terminal Block GND
```

#### 8.4.2 Lamp Cable (per lamp, 2 m run)

```
Pin 1  (18 AWG red)   ──▶ LED strip +5V pad
Pin 2  (18 AWG black) ──▶ LED strip GND pad
Pin 3  (26 AWG white) ──▶ LED strip DIN pad
```

> Keep data wire physically separate from the power pair (twist or space ≥ 5 mm) to minimise EMI coupling.

#### 8.4.3 Voltage Drop Check

- 18 AWG copper resistance: ~21 mΩ/m
- Round-trip at 2 m: 2 × 2 m × 21 mΩ/m = **84 mΩ**
- At 3.6 A (1 m strip, full load): ΔV = 3.6 × 0.084 = **0.30 V**
- Strip supply voltage: 5.0 − 0.30 = **4.70 V** ✅ (SK6812 spec: 4.5–5.5 V)

### 8.5 WLED Configuration

| Parameter | Lamp 1 | Lamp 2 |
|---|---|---|
| LED output | Output 1 | Output 2 |
| GPIO | 16 | 17 |
| LED type | SK6812 RGBW | SK6812 RGBW |
| LED count | **60** | **60** |
| Color order | GRBW | GRBW |
| Max current limit | 4000 mA | 4000 mA |
| Segment | Segment 0 | Segment 1 |
| mDNS name | `reefs.local` | — (same device) |

> **WLED build note**: use WLED v16.0 or later (the v16 series introduced major effect, segment, and color-handling improvements and ships the native Home Assistant integration auto-discovery).

**Startup preset recommendations:**
- Preset 1 "Warm Ambient": Effect = Solid, Colour = CCT 3000 K at 40 % brightness, applied to both segments.
- Set as boot preset in WLED → LED Preferences → Boot Preset.

### 8.6 GPIO Pin Assignment (ESP32)

| GPIO | Function | Notes |
|---|---|---|
| 16 | LED Data — Lamp 1 | Via 330 Ω + level shifter |
| 17 | LED Data — Lamp 2 | Via 330 Ω + level shifter |
| 0 | Boot mode (strapping) | Do not connect to LED data |
| 2 | Onboard LED (status) | Leave free |
| EN | Reset | Accessible via enclosure reset hole |

> Avoid GPIO 0, 2, 12, 15 for LED data — these are strapping pins and affect boot mode.

### 8.7 3D-Printed Enclosure Design Spec

| Feature | Requirement |
|---|---|
| Outer dimensions | ≤ 150 × 100 × 60 mm (L × W × H) |
| Wall thickness | ≥ 2.5 mm (PETG or ASA recommended for thermal stability) |
| Ventilation | ≥ 4 × 15 mm slot openings on each side (PSU convection) |
| IEC inlet cutout | 28 × 48 mm (standard C14 panel mount) |
| USB-C access port | 12 × 6 mm slot on enclosure side, aligned with ESP32 USB port |
| Cable gland holes | 2 × PG9 knockouts (one per lamp cable) |
| PCB standoffs | 4 × M3 brass heat-set inserts, 20 × 30 mm pattern for ESP32 DevKit |
| Lid fastening | 4 × M3 screws, top-opening lid |
| Strain relief | Cable glands PG9 provide strain relief; no additional clamps needed |

> Source files: [`mechanical/enclosure/CustomProjectEnclosureV1.7.8b.3mf`](mechanical/enclosure/CustomProjectEnclosureV1.7.8b.3mf) — BambuStudio 3MF project.  
> See [`mechanical/enclosure/MODELS.md`](mechanical/enclosure/MODELS.md) for full print profile.

---

### 8.8 Home Assistant Integration

#### Device Discovery

WLED auto-discovers in Home Assistant via the **native WLED integration** (no YAML required).

- mDNS hostname: **`reefs.local`**
- `cfg.json` must have `"nw": {"mdns": 1}` and `"id": {"mdns": "reefs"}` (see `firmware/cfg.json`)
- HA discovers the device within 60 s of WLED boot; both segments appear as separate light entities.

#### Expected HA Entity IDs

| Entity | Entity ID | Notes |
|--------|-----------|-------|
| Lamp 1 (Driftwood A) | `light.reef_lamps_lamp_1` | Segment 0, GPIO 16 |
| Lamp 2 (Driftwood B) | `light.reef_lamps_lamp_2` | Segment 1, GPIO 17 |
| Master (both lamps) | `light.reef_lamps` | WLED device master entity |

> Entity IDs are auto-generated by WLED integration from the device name + segment names set in `cfg.json`.  
> Verify actual entity IDs in HA after first discovery and update automations accordingly.

#### hacs-wledext-effects

`hacs-wledext-effects` is **not required** for the v1 reefs build — all effects are purely decorative with no relationship to HA sensor state. Static WLED presets + the automations below are sufficient.

If state-driven effects are added in a future revision (e.g., Breathe on notification, Meter for temperature), install `hacs-wledext-effects` and document effect entity IDs here.

#### Automations

Example automations are in [`design/effects/ha-automations.yaml`](design/effects/ha-automations.yaml):

| Automation | Trigger | Action |
|------------|---------|--------|
| Sunset on | 30 min before sunset | Both lamps → Warm Ambient, 40% |
| Late evening dim | 23:00 | Both lamps → Night Glow, 10% |
| Midnight off | 00:00 | Both lamps off |
| **Reef Scene** script | Manual / HA dashboard | Both lamps → Warm Ambient, 40%, 2 s transition |

#### Acceptance Criteria

- [ ] Both lamp entities appear in HA within 60 s of WLED boot — no manual YAML
- [ ] `light.reef_lamps_lamp_1` and `light.reef_lamps_lamp_2` independently controllable (on/off, brightness, colour, effect)
- [ ] "Reef Scene" script activates both lamps within 500 ms
- [ ] Sunset automation fires within 30 s of scheduled time
- [ ] HA shows "unavailable" on Wi-Fi loss and recovers within 30 s on reconnect

---

## 9. Milestones & Roadmap

### MVP (v1.0) — Both Lamps Functional

| Step | Task | Done? |
|---|---|---|
| 1 | Flash WLED to ESP32, verify Wi-Fi connection | ☐ |
| 2 | Bench-test SK6812 strip with WLED (single strip, GPIO 16) | ☐ |
| 3 | Measure driftwood rear faces; cut and mount aluminium channels | ☐ |
| 4 | Solder strips into channels; test both strips on bench | ☐ |
| 5 | Print control box enclosure v1 | ☐ |
| 6 | Assemble control box: PSU, terminal block, ESP32, level shifter, fuses | ☐ |
| 7 | Wire both lamp cables; connect via JST connectors | ☐ |
| 8 | Configure WLED: 2 outputs, LED counts, SK6812 type, boot preset | ☐ |
| 9 | Add WLED integration to Home Assistant; verify 2 light entities | ☐ |
| 10 | Mount lamps; route and conceal cables | ☐ |
| 11 | Thermal soak test: 60 min at 50 % brightness; verify ≤ 45 °C | ☐ |

### v1.1 — Polish

- Create Home Assistant "Reef Scene" script.
- Add sunrise/sunset automations.
- Label all wires inside control box.
- Photograph and archive wiring for future reference.

### v2.0 — Future Consideration

- Add physical touch button on each driftwood piece (capacitive, via GPIO).
- Audio-reactive mode (microphone breakout on ESP32).
- Power monitor (INA226) to track real-time draw.

### Technical Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| SK6812 data signal marginal at 3.3 V over 2 m | Medium | 74AHCT125 level shifter (included in BOM) |
| Driftwood thickness blocks heat dissipation | Low | Aluminium channel conducts heat to air, not into wood |
| PSU current rating insufficient | Low | Verify nameplate before build; replace if < 10 A |
| WLED 2-output support on selected GPIO | Low | GPIO 16/17 are proven WLED output pins on ESP32-WROOM-32 |

---

## 10. Open Questions

- Which exact driftwood piece dimensions (length × depth) determine the final strip length per lamp?
- Is the Honeywell PSU model confirmed as ≥ 10 A, or does it need replacement?
- Should the control box mount inside a shelf or on the wall behind it?
- Is cable management via baseboard trunking sufficient, or does the installation need in-wall conduit?

---

## 11. Changelog

| Date | Change |
|------|--------|
| 2026-05-16 | Initial spec (v1.0 draft) |

---

## 12. Appendix — User Stories

| ID | User Story | Priority | Acceptance Criteria |
|---|---|---|---|
| GH-001 | As a resident, I want to control Lamp 1 and Lamp 2 independently from HA so that each lamp can be set to different states. | High | Toggling one HA entity does not change the other's state. |
| GH-002 | As a resident, I want to set brightness and colour temperature per lamp so that I can adapt ambience to activity. | High | Full 1–100 % brightness range; CCT range 2700–6500 K usable. |
| GH-003 | As a resident, I want to apply WLED effects per lamp independently so that lamps can display different effects simultaneously. | Medium | Any WLED effect applied to Lamp 1 does not override Lamp 2. |
| GH-004 | As a builder, I want WLED to auto-discover in HA with no manual YAML so that setup is repeatable. | High | Both entities appear in HA within 60 s of WLED boot, zero manual config. |
| GH-005 | As a resident, I want a single "Reef Scene" HA trigger that sets both lamps to the warm ambient preset so that one tap sets the room mood. | Medium | Both lamps reach preset within 500 ms of scene trigger. |
| GH-006 | As a builder, I want the PSU to run at < 80 % load at peak brightness so that it runs safely long-term. | High | Calculated peak draw ≤ PSU rated current × 0.80. |
| GH-007 | As a builder, I want a 5 A inline fuse on each lamp power feed so that a fault cannot damage the PSU. | High | Each lamp cable has dedicated fuse; fuse blows on 6 A sustained test current. |
| GH-008 | As a builder, I want the LED strips in aluminium channels so that heat is conducted away from the wood. | High | Strip temp ≤ 45 °C at 50 % brightness after 60 min. |
| GH-009 | As a builder, I want all wiring concealed so that the installation looks furniture-grade. | High | No visible wire segments from room-facing viewpoint. |
| GH-010 | As a builder, I want a USB-C port accessible on the enclosure for OTA recovery so that I can re-flash without disassembly. | Medium | USB cable connects to ESP32 through enclosure port without removing lid. |
