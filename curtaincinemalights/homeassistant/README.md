# Home Assistant — Curtain Cinema Lights

This folder contains all Home Assistant configuration artifacts for the `curtaincinemalights` project.
Use **one of the methods** below to import automations, helpers, and dashboard cards into your HA instance.

---

## What's included

| File | Purpose |
|------|---------|
| `package.yaml` | HA Package: template sensor, helpers, scripts, and all 8 automations |
| `blueprints/curtaincinemalights-curtain-sync.yaml` | Sync LED effects to curtain open/close state |
| `blueprints/curtaincinemalights-cinema-mode.yaml` | Switch to cinema Breathe when projector plays |
| `lovelace.yaml` | Ready-made dashboard card (light controls, preset selector, curtain gauge) |

The automations also exist as raw YAML in [`design/effects/ha-automations.yaml`](../design/effects/ha-automations.yaml) for reference.

---

## Prerequisites

Before importing:

1. **WLED device discovered** — ensure `curtaincinemalights.local` is reachable and the WLED integration is added in HA (Settings → Devices & Services → Add → WLED).
2. **hacs-wledext-effects installed** — add `https://github.com/tamaygz/hacs-wledext-effects` as a HACS custom repo (category: Integration), install "WLED Effects", restart HA, then add the integration and configure:
   - `ccl_left_state_sync` — State Sync, Left Panel, source: `sensor.cinema_curtain_position`
   - `ccl_right_state_sync` — State Sync, Right Panel, source: `sensor.cinema_curtain_position`
   - `ccl_chase_left` — Chase, Left Panel
   - `ccl_chase_right` — Chase, Right Panel
   - `ccl_ambient_rainbow` — Rainbow Wave, master
   - `ccl_cinema_breathe` — Breathe, master (dim red)
3. **Template sensor created** — add the `template:` block from `package.yaml` to `configuration.yaml`, or create via Settings → Helpers → Template Sensor.

---

## Method 1 — Device Import Assistant (recommended)

After flashing firmware + filesystem:

1. Open `http://curtaincinemalights.local/ha-import.html` in your browser (on the same network as the device)
2. The page reads your WLED device config and shows the exact HA entity IDs
3. Click **Import in HA** to open each blueprint directly in your HA instance
4. Click **Download package.yaml** to get a pre-filled package file with entity IDs substituted

---

## Method 2 — Blueprint import via HA UI

Click each badge to open the blueprint importer directly in your Home Assistant:

**Curtain Sync** — sync LED fill and chase effects to cover entity state:

[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ftamaygz%2Fesp-wled-projects%2Fmain%2Fcurtaincinemalights%2Fhomeassistant%2Fblueprints%2Fcurtaincinemalights-curtain-sync.yaml)

**Cinema Mode** — switch to dim red Breathe when projector plays:

[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ftamaygz%2Fesp-wled-projects%2Fmain%2Fcurtaincinemalights%2Fhomeassistant%2Fblueprints%2Fcurtaincinemalights-cinema-mode.yaml)

After import, HA will ask you to pick entity IDs in the automation editor UI — no YAML editing needed.

---

## Method 3 — HA Package (manual copy)

1. Copy `package.yaml` to `<ha-config>/packages/curtaincinemalights.yaml`
2. Ensure `configuration.yaml` contains:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
3. Edit the substitution block at the top of `package.yaml`:
   - `[MASTER_LIGHT]` → `light.curtaincinemalights`
   - `[SEGMENT_1]` → `light.curtaincinemalights_left_panel`
   - `[SEGMENT_2]` → `light.curtaincinemalights_right_panel`
   - `cover.cinema_curtain` → your actual curtain cover entity
   - `media_player.projector` → your actual projector/TV entity
4. Restart Home Assistant

---

## Method 4 — Lovelace dashboard card

1. In HA, open your dashboard → Edit → Add Card → Manual
2. Paste the contents of `lovelace.yaml`
3. Adjust entity IDs (`light.curtaincinemalights`, `light.curtaincinemalights_left_panel`, etc.) to match your instance
4. Save

---

## Entity IDs reference

| Entity | Expected ID | Notes |
|--------|-------------|-------|
| Master light | `light.curtaincinemalights` | Controls all 180 LEDs |
| Left Panel | `light.curtaincinemalights_left_panel` | LEDs 0–89, reversed |
| Right Panel | `light.curtaincinemalights_right_panel` | LEDs 90–179 |
| Curtain position sensor | `sensor.cinema_curtain_position` | Template sensor, 0–100 % |
| Cinema mode toggle | `input_boolean.cinema_mode_active` | Created by package.yaml |
| Preset selector | `select.curtaincinemalights_preset` | Auto-created by WLED integration |

Verify all IDs in HA: Settings → Devices & Services → WLED → Curtain Cinema Lights.
