# Wiring Notes — [Project Name]

## Connections

```
5V PSU (+) ──┬──── ESP32 VIN
             └──── LED Strip VCC
PSU GND  (−) ──┬──── ESP32 GND
               └──── LED Strip GND

ESP32 GPIO2 ── [470Ω] ── LED Strip DATA
```

## Power Injection

For strips > 50 LEDs, inject power at every 50-LED interval:

```
PSU (+5V) ──── ──── ──── ...
               ↑    ↑
           LED[0]  LED[50]  (inject every ~50 LEDs)
```

## Top 5 Mistakes (WLED)

1. No 300–500Ω resistor on data line → signal reflections / flickering
2. Shared ground missing between ESP and strip → erratic behavior
3. Powering 5V strip from ESP 3V3 pin → undervoltage
4. No 1000µF cap on PSU rail → voltage dip on colour change
5. Long data line without signal booster → bit errors at high speeds

## Schematic Files

- `wiring/wiring-diagram.fzz` — Fritzing source
- `wiring/wiring-diagram.pdf` — PDF export for quick reference
- `pcb/` — KiCad PCB (if applicable)
