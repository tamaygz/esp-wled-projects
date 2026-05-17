# Home Assistant — Reefs

Driftwood ambient lamps — two SK6812 RGBW segments on one ESP8266 NodeMCU V3 WLED device.

---

## What's included

| File | Purpose |
|------|---------|
| `package.yaml` | Helpers, scripts, and automations for both lamps |
| `blueprints/reefs-sunset-on.yaml` | Turn on at sunset |
| `blueprints/reefs-night-dim.yaml` | Dim to night mode at a set time |
| `blueprints/reefs-off.yaml` | Turn off at a set time |
| `lovelace.yaml` | Ready-made dashboard card |

---

## Method 1 — Device Import Assistant (recommended)

1. Flash firmware + filesystem via PlatformIO (see `firmware/platformio_override.ini`)
2. Open `http://reefs.local/ha-import.html` (or use the device IP)
3. The page reads your WLED segment names and shows the correct entity IDs
4. Import blueprints and/or download a pre-filled `package.yaml`

---

## Method 2 — One-click blueprint import

Click each badge to import directly into your Home Assistant instance:

### Sunset On
[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ftamaygz%2Fesp-wled-projects%2Fmain%2Freefs%2Fhomeassistant%2Fblueprints%2Freefs-sunset-on.yaml)

### Night Dim
[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ftamaygz%2Fesp-wled-projects%2Fmain%2Freefs%2Fhomeassistant%2Fblueprints%2Freefs-night-dim.yaml)

### Turn Off
[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ftamaygz%2Fesp-wled-projects%2Fmain%2Freefs%2Fhomeassistant%2Fblueprints%2Freefs-off.yaml)

---

## Method 3 — HA Package (manual copy)

1. Copy `package.yaml` → `<ha-config>/packages/reefs.yaml`
2. Ensure `configuration.yaml`:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
3. Edit the entity ID substitution block at the top of `package.yaml`
4. Restart HA

**Expected entity IDs** (if mDNS name is `reefs`, segments named `Lamp 1` / `Lamp 2`):

| Entity | ID |
|--------|-----|
| Master light | `light.reefs` |
| Lamp 1 (Driftwood A) | `light.reefs_lamp_1` |
| Lamp 2 (Driftwood B) | `light.reefs_lamp_2` |
| Preset selector | `select.reefs_preset` |

---

## Method 4 — Dashboard card

Add → Manual card → paste `lovelace.yaml`.

---

## hacs-wledext-effects (optional)

Install [hacs-wledext-effects](https://github.com/tamaygz/hacs-wledext-effects) via HACS for state-driven effects:

- **Breathe** — pulse lamps on motion or notification
- **Meter** — display sensor values (temperature, energy) via brightness/color fill
- **Alert** — multi-severity color alerts from HA events

See `design/effects/ha-automations.yaml` for example automations using these effects.
