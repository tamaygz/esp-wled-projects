# LED Map & Effects Design — [Project Name]

## Physical Layout

<!-- Describe how LEDs are physically arranged. Add ASCII art or link to image -->

```
    [0]  [1]  [2]  ...
     ↓
  Strip direction
```

## Segment Plan

| Segment | Start LED | End LED | Description |
|---------|-----------|---------|-------------|
| 0 | 0 | 59 | Main strip |
| 1 | 60 | 119 | Secondary loop |

## 2D Matrix (if applicable)

- Matrix width: —
- Matrix height: —
- Serpentine: yes / no
- First LED: top-left / bottom-left
- Mapping file: `led-map/custom-map.json`

## Preset Ideas

| Name | Effect | Palette | Notes |
|------|--------|---------|-------|
| Reef Calm | Ocean | Aquatic | Slow, 5% brightness |
| Reef Party | Rainbow | Party | Fast, sound-reactive |
| Nightlight | Solid | None | Warm white, 3% |

## Useful WLED Effects

- `114` — Sunrise (great for wakeup lamp)
- `65` — Colorwaves
- `91` — Flow
- `38` — Ripple
- `122` — 2D Game of Life (matrix only)
