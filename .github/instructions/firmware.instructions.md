---
description: >
  PlatformIO and WLED firmware configuration rules.
  Use whenever editing platformio_override.ini, cfg.json, presets.json,
  WLED build flags, usermods, or flashing instructions.
applyTo:
  - "**/firmware/**"
  - "**/platformio_override.ini"
---

# Firmware — Instructions

## File Roles

| File | Purpose |
|------|---------|
| `platformio_override.ini` | Build-time overrides — extends a WLED base environment |
| `cfg.json` | WLED runtime config exported from the web UI |
| `presets.json` | WLED presets and playlists exported from the web UI |

The `platformio_override.ini` lives alongside the WLED repo's own `platformio.ini` when building. It is **not** a standalone PlatformIO project.

## platformio_override.ini Structure

```ini
[env:esp32dev_<project>]
extends = env:esp32dev          ; always extend a WLED base env

custom_usermods =
  ; list usermods one per line

build_flags =
  ${env:esp32dev.build_flags}   ; always inherit parent flags first
  -D SOME_FLAG=value
```

Valid base environments: `esp32dev`, `esp32_eth`, `esp8266`, `esp01`.

## Security: Credentials

**Never commit WiFi station credentials.** Configure SSID / password via:
1. WLED Captive Portal on first boot (AP mode `wled-ap`)
2. WLED web UI → WiFi Setup

If a build flag default is needed for the AP fallback only:
```ini
build_flags =
  ${env:esp32dev.build_flags}
  -D WLED_AP_PASS='"changeme"'    ; AP fallback, not station credentials
```

## Common Build Flags

| Flag | Default | Notes |
|------|---------|-------|
| `LEDPIN` | 2 | Main LED data GPIO |
| `BTNPIN` | 0 | Physical button GPIO |
| `WLED_MAX_BUSSES` | 3 | Increase for >3 LED outputs |
| `USERMOD_AUDIOREACTIVE` | off | Enables audioreactive usermod |

## Flashing

```bash
# From within the WLED repo directory with the project override alongside it:
pio run -e esp32dev_<project> -t upload                       # USB serial
pio run -e esp32dev_<project> -t upload --upload-port=<ip>    # OTA
```

## cfg.json / presets.json

Export from WLED UI:
- `cfg.json`: **Config** → **Security & Updates** → **Backup**
- `presets.json`: same backup page, or export individual presets

Do not hand-edit these JSON files for simple changes — use the WLED web UI and re-export.

## Home Assistant / mDNS

Every project must be discoverable by Home Assistant via mDNS. Two required keys in `cfg.json`:

```json
{
  "id": { "mdns": "<project-name>" },
  "nw": { "mdns": 1 }
}
```

- `mdns` hostname must be unique across all devices on the network.
- HA native WLED integration auto-discovers the device once mDNS is active.
- Do not configure MQTT unless there is an explicit reason — the native integration is sufficient.
