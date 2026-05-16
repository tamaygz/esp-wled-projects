# esp-wled-projects

> DIY LED lighting projects powered by **WLED** on ESP32 / ESP8266.

Each subfolder is a self-contained project with firmware config, wiring docs, BOM, 3D models, and design files.

---

## Projects

| Project | Status | LEDs | Description |
|---------|--------|------|-------------|
| [reefs](./reefs/) | wip | — | Reef aquarium lighting controller |

---

## Folder Convention (per project)

```
[project]/
├── firmware/                 # platformio_override.ini, cfg.json, presets.json
├── hardware/
│   ├── wiring/               # Fritzing, KiCad schematics, PDFs
│   ├── pcb/                  # KiCad PCB, Gerbers
│   └── bom/                  # BOM CSV, LCSC part numbers
├── mechanical/
│   ├── 3d-models/            # STL / STEP / F3D
│   ├── enclosure/            # Housing files, print settings
│   └── mounting/             # Brackets, clips, diffusers
├── design/
│   ├── led-map/              # 2D pixel maps, segment plans
│   ├── effects/              # Effect ideas, palette exports, preset JSON
│   └── references/           # Mood boards, inspiration
├── docs/
│   ├── photos/
│   ├── videos/
│   └── notes.md
└── specs.md                  # Project spec sheet
```

See [_template/](./_template/) for a ready-to-copy project skeleton.

---

## Quick Start

1. Copy `_template/` → `my-project/`
2. Fill in `specs.md`
3. Calculate power budget in `hardware/bom/bom.md`
4. Wire up hardware per `hardware/wiring/WIRING.md`
5. Edit `firmware/platformio_override.ini` and flash WLED
6. Configure presets via WLED web UI → export to `design/effects/presets.json`

---

## Common Tools

| Tool | Purpose | Link |
|------|---------|------|
| WLED web installer | Flash firmware | https://install.wled.me |
| WLED air cook | Online custom build | https://wled-compile.github.io |
| KiCad | Schematic / PCB | https://kicad.org |
| Fritzing | Wiring diagrams | https://fritzing.org |
| PrusaSlicer / Bambu Studio | 3D print | — |
| WLED SR fork | Sound-reactive build | https://github.com/MoonModules/WLED-MM |
| LedFX | PC-based audio reactive | https://ledfx.app |

---

## Resources

- [WLED Docs](https://kno.wled.ge) — official documentation
- [WLED GitHub](https://github.com/wled/WLED)
- [r/WLED](https://reddit.com/r/WLED)
- [WLED Discord](https://discord.gg/QAh7wJHrRM)
- [QuinLED](https://quinled.info) — WLED-dedicated hardware
- [Athom pre-flashed controllers](https://www.athom.tech)
