# BOM — [Project Name]

> Generated: YYYY-MM-DD

| # | Component | Value / Part | Package | Qty | Source | LCSC | Unit Price | Notes |
|---|-----------|--------------|---------|-----|--------|------|------------|-------|
| 1 | Microcontroller | ESP32-DEVKITC-32E | DevKit | 1 | LCSC | C701341 | | |
| 2 | LED Strip | WS2812B 60LED/m IP30 | 5 m roll | 1 | | | | 5V data |
| 3 | Power Supply | 5V 10A switching | brick | 1 | | | | |
| 4 | Resistor | 470Ω ¼W | 0805 | 1 | | | | data line |
| 5 | Capacitor | 1000µF 10V electrolytic | 8x12mm | 1 | | | | PSU decoupling |
| 6 | Connector | XT60 female (PSU side) | — | 1 | | | | |
| 7 | Connector | JST-SM 3-pin | strip end | 2 | | | | |

## Power Budget

| Rail | Component | Count | mA each | Total mA |
|------|-----------|-------|---------|---------|
| 5V | WS2812B (worst-case white) | 60 | 60 | 3600 |
| 5V | ESP32 | 1 | 250 | 250 |
| **Total** | | | | **~3850 mA** |

Recommended PSU: **5V 5A minimum**, 10A with headroom.
