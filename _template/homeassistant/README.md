# Home Assistant — [Project Name]

This folder contains all Home Assistant configuration artifacts for this project.
Use **one or more** of the import methods below.

---

## What's included

| File | Purpose |
|------|---------|
| `package.yaml` | HA Package: helpers (input_boolean/number/select), scripts, and automations |
| `blueprints/*.yaml` | Importable automation blueprints (one per automation pattern) |
| `lovelace.yaml` | Ready-made dashboard card for this device |

---

## Method 1 — Device Import Assistant (recommended)

After flashing firmware + filesystem:

1. Open `http://[wled-ip]/ha-import.html` in your browser
2. The page reads your WLED device config and shows the correct entity IDs
3. Click **Import blueprint** links to import automations directly into HA
4. Click **Download package.yaml** to get a pre-filled package file

---

## Method 2 — Blueprint import via HA UI

Paste each URL below into **Settings → Automations & scenes → Blueprints → Import Blueprint**:

<!-- Add badge links per blueprint, e.g.:
[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Ftamaygz%2Fesp-wled-projects%2Fmain%2F[project]%2Fhomeassistant%2Fblueprints%2F[file].yaml)
-->

---

## Method 3 — HA Package (manual copy)

1. Copy `package.yaml` to your HA config `packages/` folder (create it if it doesn't exist)
2. Ensure `configuration.yaml` contains:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
3. Edit the entity ID substitution block at the top of `package.yaml` to match your instance
4. Restart Home Assistant

---

## Method 4 — Lovelace dashboard card

1. In HA, go to your dashboard → Edit → Add Card → Manual
2. Paste the contents of `lovelace.yaml`
3. Adjust entity IDs to match your instance
