# Project Spec — [Project Name]

> Status: `planning` | `wip` | `done` | `archived`

## Concept

_One paragraph: what is this project, what effect should it create, where will it live._

## Requirements

- [ ] LED type: 
- [ ] LED count: 
- [ ] Power: 
- [ ] Mounting: 
- [ ] Connectivity: WiFi / BLE / wired
- [ ] Smart home integration: HA / MQTT / none
- [ ] Sound-reactive: yes / no
- [ ] Outdoor / indoor:
- [ ] IP rating needed:

## Constraints

- Budget: 
- Enclosure size max (L × W × H mm): 
- Power availability (USB 5 V / 12 V DC / mains):

## Mechanical

- Enclosure: 3D-printed YAPP_Box (default — generated via `/gen-enclosure`)
- Lid closure: snap-on (default)
- Material: PETG / ASA
- Wall thickness: 3.0 mm

## Acceptance Criteria

- [ ] All LEDs addressable and responding
- [ ] WLED web UI reachable on local network
- [ ] Presets saved and cycling correctly
- [ ] No flicker at any brightness level
- [ ] Thermal: no heat issues at 1-hour runtime
- [ ] Enclosure closed and mounted
- [ ] Auto-discovered in Home Assistant; on/off, brightness, colour verified

## Home Assistant

> **Mandatory** — every project in this repo must be controllable from Home Assistant via the native WLED integration (auto-discovered via mDNS).

- **Device mDNS hostname:** `<project-name>` (set in `firmware/cfg.json` → `"id": {"mdns": "<project-name>"}` and `"nw": {"mdns": 1}`)
- **Expected HA entities:**
  - `light.<project_name>` (one per WLED segment / output)
  - _(add more rows as segments are added)_
- **hacs-wledext-effects:** _yes / no_ — only if the strip should visualise an HA sensor value or fire HA-event-driven alerts. List effects to install (Rainbow Wave, Meter, State Sync, Alert, Breathe, …).
- **Automations:** documented in `design/effects/ha-automations.yaml`.

## Open Questions

- 
- 

## Changelog

| Date | Change |
|------|--------|
| YYYY-MM-DD | Initial spec |
