# Parts Register

`parts.json` provides verified physical dimensions, important technical metadata, and board pinout data for components commonly used across projects in this repository. It is the single source of truth for enclosure SCAD cutout sizes, PCB footprint planning, BOM documentation, and reusable board/pin metadata.

## Purpose

When designing enclosures, wiring, firmware configs, or PCB layouts, check this register **first** before measuring components manually or looking up datasheets. Using register values ensures consistency between `bom.md`, `*-enclosure.scad`, `WIRING.md`, and any board-specific firmware notes across the repo.

This register is also part of the repo's meta layer. Its job is not just to store data, but to reduce duplicated research across projects: once a part is in the register with good sources and notes, future projects should reuse that work instead of rebuilding it.

## When To Use It

Open this register before you:

- choose between boards, PSUs, LED strips, connectors, or level shifters
- write a BOM, wiring guide, `specs.md`, or enclosure SCAD file
- describe core components in a project README
- need a board pinout, PlatformIO ID, or enclosure cutout dimension

If a project file contains design-critical part facts and the register could have supplied them, the register should usually be updated first.

## Source Priority

Use sources in this order whenever possible:

1. Official manufacturer datasheet
2. Official board/product page with downloadable pinout, schematics, or technical specs
3. PlatformIO board manifest or framework variant files for software-facing board identifiers and pin aliases
4. Distributor parametric listing (LCSC, JLCPCB, Mouser, DigiKey) when the official source is missing a specific dimension
5. Trusted community references only as a fallback, marked with `"verified": false`

For boards, prefer storing both the human-facing board documentation source and the machine-facing source used to derive software pin names.

## Units

All dimensions are in **millimetres (mm)**. `pcb_or_body_mm` gives the bounding box `l × w × h` (length × width × height) of the component's PCB footprint or encapsulated body.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable component name |
| `manufacturer` | string | Component manufacturer |
| `mfr_part_number` | string | Manufacturer part number |
| `category` | string | Component category (e.g. `microcontroller`, `ac_dc_psu`, `led_strip`) |
| `pcb_or_body_mm` | object | Bounding box `l` (length), `w` (width), `h` (height) in mm |
| `mounting_holes` | array | Mounting hole positions relative to bounding box bottom-left corner |
| `cutouts_needed` | array | Panel or enclosure cutout specs (for ports, connectors, etc.) |
| `electrical` | object | Optional electrical characteristics that drive design decisions |
| `interfaces` | array | Optional protocols or buses the part exposes or requires |
| `software_identifiers` | object | Optional board or firmware identifiers such as PlatformIO board ID or Arduino variant |
| `board_pinout` | object | Optional board-only pinout image, textual mapping, and machine-readable pin list |
| `key_notes` | array | Engineering notes, gotchas, and usage guidance |
| `source_url` | string | Primary datasheet or product page used to verify dimensions |
| `verified` | boolean | `true` if confirmed from official datasheet; `false` if estimated |

### `electrical`

Store only fields that materially affect hardware, enclosure, or firmware work. Common examples:

- `supply_voltage_v`
- `logic_voltage_v`
- `input_voltage_range_v`
- `output_voltage_v`
- `max_current_a`
- `max_power_w`
- `operating_temp_c`
- `wireless`
- `flash_mb`
- `psram_mb`

### `interfaces`

Use this for protocols and board-level connectivity that affect project design. Examples: `usb_c`, `uart`, `i2c`, `spi`, `pwm`, `adc`, `ws2812_800khz`, `wifi`, `ble`.

### `software_identifiers`

Use this primarily for development boards and modules. Helpful fields include:

- `platformio_board`
- `arduino_variant`
- `frameworks`
- `mcu`
- `usb_bridge`

This mirrors the way PlatformIO board manifests expose machine-readable board metadata and makes future tooling easier to build.

### `board_pinout`

Use this for development boards, controller boards, or modules with named pins. Capture both a human-facing view and a structured machine-readable view when the source material allows it.

Recommended subfields:

| Field | Type | Description |
|-------|------|-------------|
| `image_url` | string | Official pinout PDF/image URL when available |
| `image_path` | string | Optional repo-local image path if a pinout image is committed later |
| `source_url` | string | Page used to verify the pinout |
| `headers` | array | Header-level grouping such as left/right header or connector block |
| `pins` | array | One entry per exposed pin or labeled pad |

Each `pins` entry should use a stable structure when possible:

```json
{
	"label": "D4",
	"gpio": 2,
	"aliases": ["SDA"],
	"header": "left",
	"capabilities": ["digital_io", "i2c", "pwm"],
	"default_use": "user_io",
	"warnings": ["boot_strapping_pin"],
	"notes": "Avoid pulling low during boot"
}
```

Use `warnings` for constraints such as boot-strapping pins, input-only pins, flash-connected pins, ADC limitations, or 5V-unsafe pads.

## What To Collect

Best practice is to store the smallest set of technical details that repeatedly affect project design decisions.

### All parts

- Mechanical envelope: body size, mounting holes, enclosure cutouts
- Procurement identity: manufacturer, exact MPN, canonical source URL
- Design-critical notes: mating connector, package family, orientation, revision caveats

### Boards and devkits

- MCU/module, logic voltage, USB connector type, regulator/output rails
- Wireless capabilities, flash/PSRAM size when relevant
- PlatformIO board ID, Arduino variant, or other software-facing identifiers
- Pinout image link plus a structured pin list with GPIO numbers, aliases, capabilities, and warnings

### Power modules and regulators

- Input range, output rails, max current, max power, isolation class if applicable
- Fuse or creepage notes that affect integration

### LED strips

- Protocol, supply voltage, color order, LED density, cut interval, current-per-LED assumptions

### Connectors

- Pitch, current rating, wire gauge range, mating part numbers, retention or panel-mount notes

### Logic ICs and sensors

- Supply range, logic compatibility, package type, channel count, and any bus/protocol requirements

## Using the Register

- **Enclosure SCAD files**: Reference `pcb_or_body_mm` and `cutouts_needed` when sizing `boxInnerHeight`, PCB standoffs, and cutout arrays in YAPP_Box SCAD files. Add a comment citing the `PART_ID`.
- **BOM files (`bom.md`)**: Cross-reference part names and MPN values against register entries.
- **WIRING.md**: Reference connector dimensions for cable routing guidance and strain-relief sizing.
- **Board-driven firmware docs**: Reuse `software_identifiers` and `board_pinout` instead of recreating board notes in project files.
- **Project-facing READMEs and specs**: Reuse concise register-backed facts, `source_url` links, and pinout references instead of writing freehand summaries.

Existing entries may still be geometry-first. When you touch an existing part for new work, backfill technical fields opportunistically instead of creating a second source of truth.

## Adding a New Part

1. Assign a unique `PART_ID` key (e.g. `MY_PART_REV2`) — use `SCREAMING_SNAKE_CASE`.
2. Fill all core fields. Add `electrical`, `interfaces`, `software_identifiers`, and `board_pinout` when they materially apply.
3. Use `"verified": false` if any dimension or board mapping is estimated.
4. Set `source_url` to the official datasheet or product page, with distributor pages as a fallback.
5. For boards and devkits, add `software_identifiers` and `board_pinout` whenever official documentation or framework metadata exists.
6. Add a note in `key_notes` explaining what is estimated and how to verify it.
7. Commit the updated `parts.json` in the same commit as the first project file that uses the new part data.

If adding a part that is already in the register but a different revision or voltage variant, create a new `PART_ID` with a suffix (e.g. `HLK_5M12` for the 12V variant).

## Board Pinout Workflow

For development boards and controller boards:

1. Capture the official board page or datasheet URL in `source_url`.
2. Add `board_pinout.image_url` if the vendor publishes a pinout PDF or image.
3. Add `software_identifiers` from PlatformIO board manifests or framework variant files when available.
4. Build a `board_pinout.pins` list that maps silkscreen labels to GPIO numbers, aliases, capabilities, and warnings.
5. Mark the entry unverified if the pin map depends on unofficial or clone-specific documentation.

This gives agents and future tooling both a readable reference and a programmatic definition.

## Unverified Entries

Entries with `"verified": false` have dimensions estimated from family-series data, community sources, or prior art. They are safe for initial planning but must be confirmed from an official datasheet before committing to final PCB layout or enclosure manufacturing.

For boards, `"verified": false` also covers pinout images or GPIO mappings derived from unofficial board diagrams or clone-specific pages.

Any SCAD or BOM file using an unverified entry should include a comment:
```
// UNVERIFIED — confirm HLK_30M05 dimensions before manufacturing
```

## Parts Included

| PART_ID | Name | L × W × H (mm) | Category | Verified |
|---------|------|-----------------|----------|----------|
| `D1_MINI_V4` | Wemos LOLIN D1 Mini v4 | 34.2 × 25.6 × 10.0 | microcontroller | ✅ |
| `HLK_30M05` | Hi-Link HLK-30M05 30W 5V 6A | 57.5 × 33.6 × 22.5 | ac_dc_psu | ⚠️ estimated |
| `HLK_20M05` | Hi-Link HLK-20M05 20W 5V 4A | 56.0 × 32.0 × 22.5 | ac_dc_psu | ✅ |
| `HLK_5M05` | Hi-Link HLK-5M05 5W 5V 1A | 38.0 × 23.0 × 18.0 | ac_dc_psu | ✅ |
| `IC_74AHCT125_DIP14` | 74AHCT125 Quad Buffer DIP-14 | 19.05 × 6.35 × 4.57 | level_shifter_ic | ✅ |
| `JST_SM_2P5_3PIN` | JST SM 2.5mm 3-pin Connector | 9.5 × 6.0 × 6.0 | connector | ⚠️ estimated |
| `SK6812_RGBW_60` | SK6812 RGBW LED Strip 60 LED/m | 1000 × 10 × 1.5 per m | led_strip | ✅ |
