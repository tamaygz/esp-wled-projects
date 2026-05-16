---
description: >
  Rules for generating diagrams in esp-wled-projects.
  Use these guidelines whenever creating or modifying diagram
  generators, adding a new project, or updating docs/ visuals.
applyTo:
  - "**/gen_diagrams.py"
  - "**/gen_diagrams_config.py"
  - "**/docs/*.png"
  - "**/docs/*.svg"
  - "tools/diagram_gen/**"
---

# Diagram Generation — Copilot Instructions

## Package location
All shared diagram code lives in `tools/diagram_gen/`.  
**Never copy-paste diagram logic into a project folder** — extend the shared package instead.

## Module map

| Module | What it produces | Key public function |
|---|---|---|
| `style.py` | Shared colour palette + `apply_dark_theme()` | Constants only |
| `schematic.py` | Electrical schematics (schemdraw) | `draw_level_shifter_circuit(out)` · `draw_power_circuit(out)` |
| `blocks.py` | System block diagrams (matplotlib) | `draw_system_blocks(config, out)` |
| `concept.py` | Real-world concept illustrations (matplotlib) | `draw_side_view(config, out)` · `draw_top_view(config, out)` |
| `wiring.py` | Physical wiring diagrams (drawsvg) | `draw_physical_wiring(config, out)` |

## Import pattern for a project script

```python
import os, sys
TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools')
sys.path.insert(0, TOOLS)

from diagram_gen import blocks, concept, schematic, wiring
from diagram_gen.style import apply_dark_theme
```

## Adding a new project

1. Create `<project>/gen_diagrams_config.py` exporting `DIAGRAM_CONFIG` dict.  
   Required keys: `title`, `psu`, `controller`, `outputs`, `gpio_map`, `lamps`.  
   Copy from `reefs/gen_diagrams_config.py` as a starting point.

2. Create `<project>/gen_diagrams.py` following the pattern in `reefs/gen_diagrams.py`.

3. Run with:
   ```
   python reefs/gen_diagrams.py           # from repo root
   python tools/gen_diagrams.py reefs     # alternative via CLI runner
   ```

4. All outputs go to `<project>/docs/`.

## Generating diagrams

```bash
# All types for a project:
python tools/gen_diagrams.py reefs

# Single type:
python tools/gen_diagrams.py reefs --type schematic
python tools/gen_diagrams.py reefs --type blocks
python tools/gen_diagrams.py reefs --type concept
python tools/gen_diagrams.py reefs --type wiring
```

## Library rules

- **schemdraw ≥ 0.22**: `elm.Ic()` and `elm.IcPin()` for IC boxes.  
  `elm.Ic` is a **block element** — do NOT chain `.right(n)` / `.left(n)` on it.  
  Use `.at(position)` to place it. Two-terminal elements (`elm.Line`, `elm.Fuse`,
  `elm.Resistor`) accept `.right(n)`, `.left(n)`, `.up(n)`, `.down(n)`.
- **drawsvg ≥ 2.4**: import as `import drawsvg as draw`. No `__version__` attr.  
  Save SVG with `d.save_svg(path)`. PNG export requires `cairosvg` or Cairo libs.
- **matplotlib**: always call `matplotlib.use("Agg")` **before** importing pyplot  
  to prevent window pop-ups on headless / CI environments.

## Colour palette

All colours are defined in `tools/diagram_gen/style.py`.  
Never hardcode hex values in diagram modules — reference style constants:

```python
from . import style
style.WIRE_RED   # +5V rail
style.WIRE_BLK   # GND
style.WIRE_GRN   # DATA signal
style.LED_DOT    # LED dot / warm yellow
style.GLOW       # light halo
style.ACCENT     # primary (ESP32, titles)
style.ACCENT2    # secondary (data signals, level shifter)
```

## Output conventions

- `docs/schematic-level-shifter.png` — level shifter circuit
- `docs/schematic-power.png` — power distribution
- `docs/concept-system.png` — system block diagram
- `docs/concept-side-view.png` — cross-section illustration
- `docs/concept-top-view.png` — floor plan illustration
- `docs/wiring-physical.svg` — physical wiring diagram (+ .png if cairosvg present)
