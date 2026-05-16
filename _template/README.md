# [Project Name]

> One-line description of the lighting project.

---

## Concept

<!-- Describe the lighting effect and installation in 2–3 sentences. -->

### How the lighting works — side view

<!-- The LED strip mounts on the rear face of the object, casting light between it and the wall. -->

![Side-view cross-section](docs/concept-side-view.png)

### Installation floor plan — top view

<!-- Shows lamp positions along the wall and cable runs to the control box. -->

![Top-down floor plan](docs/concept-top-view.png)

### System overview

![System block diagram](docs/concept-system.png)

> **Note:** Run `python tools/gen_diagrams.py <project-name>` from the repo root to generate the images above.

---

## Quick Facts

| Property | Value |
|---|---|
| **Board** | ESP32-WROOM-32 |
| **LED Type** | — |
| **LED Count** | — |
| **Power Supply** | — |
| **WLED Version** | — |
| **Smart home** | Home Assistant (native WLED integration) |

---

## Documentation Index

| Document | What's inside |
|---|---|
| [specs.md](specs.md) | Full PRD: concept, requirements, power budget, BOM, WLED config, HA integration |
| [hardware/bom/bom.md](hardware/bom/bom.md) | Bill of materials, current budget, PSU sizing |
| [hardware/wiring/WIRING.md](hardware/wiring/WIRING.md) | GPIO assignments, power rails, cable runs |
| [design/led-map/LED-DESIGN.md](design/led-map/LED-DESIGN.md) | Segment plan, preset design, colour strategy |
| [design/effects/ha-automations.yaml](design/effects/ha-automations.yaml) | Home Assistant automation examples |
| [mechanical/enclosure/MODELS.md](mechanical/enclosure/MODELS.md) | 3D print settings, cutout dimensions |
| [firmware/platformio_override.ini](firmware/platformio_override.ini) | WLED build config (env, usermods, build flags) |
| [firmware/cfg.json](firmware/cfg.json) | WLED device config (mDNS, outputs, boot preset) |
| [firmware/presets.json](firmware/presets.json) | Exported WLED presets |

---

## Wiring & Schematics

![Physical wiring](docs/wiring-physical.svg)

See [hardware/wiring/WIRING.md](hardware/wiring/WIRING.md) for the full GPIO table and wiring notes.

| Level-shifter circuit | Power distribution |
|---|---|
| ![Level-shifter schematic](docs/schematic-level-shifter.png) | ![Power schematic](docs/schematic-power.png) |

---

## Build Checklist (MVP)

- [ ] Flash WLED to ESP32, verify Wi-Fi
- [ ] Bench-test LED strip on GPIO 16
- [ ] Assemble control box (PSU, ESP32, level shifter)
- [ ] Wire lamp cables; connect via JST connectors
- [ ] Configure WLED: outputs, LED count, colour order, boot preset
- [ ] Add WLED integration to Home Assistant; verify light entities
- [ ] Mount installation; conceal cables
- [ ] Thermal soak: 60 min at 50 % brightness — verify ≤ 45 °C on strip

---

## Resources

- [specs.md](specs.md) — full project spec
- [WLED Docs](https://kno.wled.ge)
- [WLED GitHub](https://github.com/wled/WLED)
- [WLED Discord](https://discord.gg/QAh7wJHrRM)
