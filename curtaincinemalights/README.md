# curtaincinemalights — Cinema Curtain LED Sync

SK6812 RGBW LED strip running inside an aluminium curtain-rail channel that illuminates
the gap between a motorized cinema-red curtain and the wall. The lit zone mirrors the
curtain's exact open/close position in real time — center-first, spreading outward —
driven by **hacs-wledext-effects State Sync** reacting to a Home Assistant cover entity.

---

## Concept

| Side View | Top-Down Floor Plan |
|:---------:|:-------------------:|
| ![Side view](docs/concept-side-view.png) | ![Top view](docs/concept-top-view.png) |

---

## System Block Diagram

![System blocks](docs/concept-system.png)

---

## Quick Facts

| Property | Value |
|----------|-------|
| Controller | ESP8266 LOLIN D1 Mini v4 |
| WLED version | v0.15 (ESP8266 branch) |
| LED strip | SK6812 RGBW 60 LED/m, 5V, GRBW order |
| Default LED count | 180 LEDs (3 m) — adjustable in WLED UI |
| Output pin | GPIO2 (D4) via 74AHCT125 level shifter |
| PSU | Hi-Link HLK-20M05 — 5V / 4A |
| WLED ABL limit | 3200 mA |
| Segments | Left Panel (LEDs 0–89, reversed) + Right Panel (LEDs 90–179) |
| HA mDNS hostname | `curtaincinemalights.local` |
| HA master entity | `light.curtaincinemalights` |
| hacs-wledext-effects | State Sync (position fill), Chase (movement), Breathe (cinema mode) |
| Enclosure | 3D-printed YAPP_Box — ~106 × 46 × 44 mm, PETG/ASA, snap-on lid |

---

## Documentation Index

| Doc | Contents |
|-----|----------|
| [specs.md](specs.md) | Full project spec, requirements, acceptance criteria, HA integration plan |
| [hardware/bom/bom.md](hardware/bom/bom.md) | Bill of materials, power budget, connector strategy |
| [hardware/wiring/WIRING.md](hardware/wiring/WIRING.md) | Wiring guide, pin allocation, 74AHCT125 pinout |
| [design/led-map/LED-DESIGN.md](design/led-map/LED-DESIGN.md) | Segment layout, curtain-position → LED mapping |
| [design/effects/ha-automations.yaml](design/effects/ha-automations.yaml) | Home Assistant template sensor, helpers, and 8 automations |
| [mechanical/enclosure/MODELS.md](mechanical/enclosure/MODELS.md) | Enclosure print specs, file list, re-render command |
| [firmware/cfg.json](firmware/cfg.json) | WLED config: device name, segments, GPIO, ABL |
| [firmware/platformio_override.ini](firmware/platformio_override.ini) | PlatformIO build override for ESP8266 D1 Mini |
| [firmware/presets.json](firmware/presets.json) | 3 WLED presets: Warm Amber, Cinema Dim Red, Ambient Wave |

---

## Wiring Diagram

![Physical wiring](docs/wiring-physical.svg)

---

## Schematics

| Level Shifter | Power Supply |
|:-------------:|:------------:|
| ![Level shifter schematic](docs/schematic-level-shifter.png) | ![Power schematic](docs/schematic-power.png) |

---

## Enclosure Previews

| Base shell | Lid |
|:----------:|:---:|
| ![Base iso](mechanical/enclosure/curtaincinemalights-base-iso.png) | ![Lid iso](mechanical/enclosure/curtaincinemalights-lid-iso.png) |

Source: [`mechanical/enclosure/curtaincinemalights-enclosure.scad`](mechanical/enclosure/curtaincinemalights-enclosure.scad)  
Re-render: `pwsh tools/render_enclosure.ps1 -Project curtaincinemalights -ScadName curtaincinemalights-enclosure`

---

## First-Time Setup

1. Flash WLED v0.15 (ESP8266 branch) using PlatformIO:
   ```
   cp curtaincinemalights/firmware/platformio_override.ini <wled-repo>/
   pio run -e d1_mini_curtaincinemalights -t upload
   ```
2. Connect to the **WLED-curtaincinemalights** captive portal on your phone → enter Wi-Fi credentials.
3. Upload `firmware/cfg.json` and `firmware/presets.json` via WLED web UI (Config → Security & Updates → Import Settings / Presets).
4. Home Assistant should auto-discover `curtaincinemalights.local` within 60 s.
5. Create the template sensor from `design/effects/ha-automations.yaml` → add to `configuration.yaml`.
6. Install hacs-wledext-effects (see `specs.md §6.3`) → configure effects per spec.
7. Import automations from `design/effects/ha-automations.yaml`.

---

## Adjusting for Your Curtain Width

| Width | LED count | Segment split | WLED setting |
|-------|-----------|---------------|--------------|
| 2.0 m | 120 | 0–59 + 60–119 | Change total LEDs + segment stops in WLED UI |
| 2.5 m | 150 | 0–74 + 75–149 | " |
| 3.0 m (default) | 180 | 0–89 + 90–179 | Default config |
| 4.0 m | 240 | 0–119 + 120–239 | " |
