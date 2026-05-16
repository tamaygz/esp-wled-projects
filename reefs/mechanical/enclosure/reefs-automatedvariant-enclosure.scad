// reefs-automatedvariant-enclosure.scad
// Generated 2026-05-16 via enclosure-gen skill
// Project: Reefs — WLED Driftwood Ambient Lighting
//
// Outer dimensions: 150 × 100 × 59 mm  (spec: ≤ 150 × 100 × 60 mm ✓)
// Inner dimensions: 144 × 94 × 56 mm
// Wall: 3 mm · Base floor: 1.5 mm · Lid ceiling: 1.5 mm
//
// Render commands (run from this directory, with YAPPgenerator_v3.scad alongside):
//   Full preview (base + lid side-by-side):
//     openscad --render -o reefs-automatedvariant-full.stl reefs-automatedvariant-enclosure.scad
//   Base only:
//     openscad --render -o reefs-automatedvariant-base.stl reefs-automatedvariant-enclosure.scad -D printLidShell=false
//   Lid only:
//     openscad --render -o reefs-automatedvariant-lid.stl reefs-automatedvariant-enclosure.scad -D printBaseShell=false
//
// Component layout (view from front):
//   Back  wall : IEC C14 inlet 28×48 mm (mains power in)
//   Front wall : USB-C OTA access slot 12×8 mm (centred, ~Z=10 mm)
//   Left  wall : PG9 cable gland (Lamp 1 feed) + 4× vent slots 15×4 mm
//   Right wall : PG9 cable gland (Lamp 2 feed) + 4× vent slots 15×4 mm
//   Lid        : REEFS project label (3-line raised)

// ─────────────────────────────────────────────────────────────────────────────
// Render flags
// ─────────────────────────────────────────────────────────────────────────────
printBaseShell      = true;
printLidShell       = true;
showSideBySide      = true;   // preview only; no effect on .stl output
printerLayerHeight  = 0.2;
renderQuality       = 8;      // 1–32; raise to 16 for print-quality STL

// ─────────────────────────────────────────────────────────────────────────────
// Box dimensions  (virtual-PCB approach: all padding = 0)
//   inner L = pcbLength = 144 mm   outer L = 150 mm
//   inner W = pcbWidth  =  94 mm   outer W = 100 mm
//   inner Z = basePlane + baseWall + lidWall + lidPlane
//           = 1.5 + 30 + 26 + 1.5 = 59 mm outer
// ─────────────────────────────────────────────────────────────────────────────
pcbLength           = 144;    // inner length (back→front / X-axis)
pcbWidth            = 94;     // inner width  (left→right / Y-axis)
pcbThickness        = 1.6;    // PCB thickness placeholder (virtual PCB)
standoffHeight      = 5.0;    // mm above base floor
standoffDiameter    = 7.0;
standoffPinDiameter = 3.0;    // M3 self-threading
standoffHoleSlack   = 0.4;

paddingFront        = 0;
paddingBack         = 0;
paddingRight        = 0;
paddingLeft         = 0;

wallThickness       = 3.0;
basePlaneThickness  = 1.5;
lidPlaneThickness   = 1.5;

// inner wall heights: base 30 + lid 26 = 56 mm total
baseWallHeight      = 30;
lidWallHeight       = 26;
ridgeHeight         = 5.0;   // lid/base overlap ridge — must be ≤ lidWallHeight ✓
ridgeSlack          = 0.3;
roundRadius         = 3.0;   // corner rounding
boxType             = 0;     // 0 = fully rounded

// ─────────────────────────────────────────────────────────────────────────────
// PCB definition (YAPP v3 format — "Main" entry is required)
//   [name, length, width, posx, posy, thickness, standoffHeight,
//    standoffDiameter, standoffPinDiameter, standoffHoleSlack]
// Virtual PCB: fills the entire inner floor (posx=0, posy=0)
// ─────────────────────────────────────────────────────────────────────────────
pcb = [
  ["Main", pcbLength, pcbWidth, 0, 0, pcbThickness,
   standoffHeight, standoffDiameter, standoffPinDiameter, standoffHoleSlack],
];

// ─────────────────────────────────────────────────────────────────────────────
// ESP32 DevKit 38-pin standoffs
//   Board: ~30 × 51 mm   Hole pattern: 45 × 23 mm (centre-to-centre)
//   Orientation: USB-C end toward FRONT wall (high X)
//   Placement: centred on inner width (Y=47 mm), offset toward front
//              Front standoffs at X=126, back standoffs at X=81
//   USB-C port approx location: X≈129 mm from back, Y≈47 mm, Z≈10 mm
//   → aligns with USB-C slot on front wall at (fromBack=47, fromLeft=10)
//
//   Coords are yappCoordPCB (0,0) = inner back-left corner
// ─────────────────────────────────────────────────────────────────────────────
pcbStands = [
  // Back-left hole
  [81,  35, standoffHeight, 0, standoffDiameter, standoffPinDiameter,
   standoffHoleSlack, yappBoth, yappPin, yappBackLeft,   yappCoordPCB],
  // Back-right hole
  [81,  58, standoffHeight, 0, standoffDiameter, standoffPinDiameter,
   standoffHoleSlack, yappBoth, yappPin, yappBackRight,  yappCoordPCB],
  // Front-left hole  (close to front wall for USB-C alignment)
  [126, 35, standoffHeight, 0, standoffDiameter, standoffPinDiameter,
   standoffHoleSlack, yappBoth, yappPin, yappFrontLeft,  yappCoordPCB],
  // Front-right hole
  [126, 58, standoffHeight, 0, standoffDiameter, standoffPinDiameter,
   standoffHoleSlack, yappBoth, yappPin, yappFrontRight, yappCoordPCB],
];

// ─────────────────────────────────────────────────────────────────────────────
// Lid connectors — 4 × M3 corner screws
//   M3 screw Ø3, flat head Ø6, 3.2 mm insert hole (self-threading M3 or
//   4.2 mm for M3 heat-set insert — adjust insertDiam as needed)
// ─────────────────────────────────────────────────────────────────────────────
connectors = [
  // [posx, posy, standHeight, screwDiam, screwHeadDiam, insertDiam, outsideDiam, corner, coord]
  [5, 5, 12, 3, 6, 3.2, 8, yappAllCorners, yappCoordBoxInside],
];

// ─────────────────────────────────────────────────────────────────────────────
// BACK wall — IEC C14 mains inlet (28 × 48 mm)
//   Centre Y = pcbWidth/2 = 47 mm  (centred on 94 mm inner width)
//   Centre Z = 25 mm from inner floor  (bottom=1 mm, top=49 mm < 56 mm ✓)
// ─────────────────────────────────────────────────────────────────────────────
cutoutsBack = [
  // IEC C14 panel-mount inlet: 28 mm wide × 48 mm tall
  // [fromBack (Y), fromLeft (Z), width, height, radius, shape, depth, angle, coord, origin]
  [47, 25, 28, 48, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
];

// ─────────────────────────────────────────────────────────────────────────────
// FRONT wall — USB-C OTA access (12 × 8 mm slot)
//   Centre Y = 47 mm (centred on front wall)
//   Centre Z = 10 mm (ESP32 USB-C port height above inner floor:
//              standoffHeight 5 + pcbThickness 1.6 + port_centre 3.4 ≈ 10)
// ─────────────────────────────────────────────────────────────────────────────
cutoutsFront = [
  // USB-C access slot — 12 mm wide × 8 mm tall (generous for cable clearance)
  [47, 10, 12, 8, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
];

// ─────────────────────────────────────────────────────────────────────────────
// LEFT wall — PG9 Lamp 1 cable gland + 4 ventilation slots
//   PG9: Ø16 mm (radius 8), centre at X=72 (mid-wall), Z=25
//   Vents: 4 × (15 × 4 mm) slots at Z=20, avoiding PG9 footprint (X=64–80)
// ─────────────────────────────────────────────────────────────────────────────
cutoutsLeft = [
  // Ventilation slot 1 — PSU convection (rear quarter)
  [15,  20, 15, 4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  // Ventilation slot 2
  [40,  20, 15, 4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  // PG9 cable gland — Lamp 1 (SK6812 power + data)
  [72,  25, 0,  0, 8, yappCircle,    0, 0, yappCoordBoxInside, yappCenter],
  // Ventilation slot 3
  [104, 20, 15, 4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  // Ventilation slot 4 (front quarter)
  [129, 20, 15, 4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
];

// ─────────────────────────────────────────────────────────────────────────────
// RIGHT wall — PG9 Lamp 2 cable gland + 4 ventilation slots (mirror of left)
// ─────────────────────────────────────────────────────────────────────────────
cutoutsRight = [
  // Ventilation slot 1
  [15,  20, 15, 4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  // Ventilation slot 2
  [40,  20, 15, 4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  // PG9 cable gland — Lamp 2 (SK6812 power + data)
  [72,  25, 0,  0, 8, yappCircle,    0, 0, yappCoordBoxInside, yappCenter],
  // Ventilation slot 3
  [104, 20, 15, 4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  // Ventilation slot 4
  [129, 20, 15, 4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
];

cutoutsLid   = [];
cutoutsBase  = [];

// ─────────────────────────────────────────────────────────────────────────────
// Labels — lid project title (3 lines) + face connector identification
//
// Coordinate system for labels: yappCoordBox (default)
//   Origin = outer front-left-bottom corner
//   Lid: posx = left→right (0…outerL), posy = front→back (0…outerW)
//   Walls: posx = horizontal along face, posy = vertical from base
//
// Lid outer: 150 × 100 mm → center (75, 50)
// Line spacing = 1.6 × 10 = 16 mm → lines at y=66, 50, 36
//
// Face label formula (BoxInside → BoxBox):
//   posx  = cutout_fromBack + wallThickness
//   posy  = (cutout_fromLeft ± hole_r_or_h2 ± gap_2mm ± font_2mm) + basePlaneThickness
// ─────────────────────────────────────────────────────────────────────────────
labelsPlane = [

  // ── Lid: project title ──────────────────────────────────────────────────
  // Line 1: project name  (size 10, bold, raised -0.6 mm)
  [75, 66, 0, -0.6, yappLid,
   "Liberation Sans:style=Bold", 10, "REEFS",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  // Line 2: subtitle  (size 6, regular)
  [75, 50, 0, -0.4, yappLid,
   "Liberation Sans", 6, "WLED v0.15  |  SK6812 RGBW",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  // Line 3: spec summary  (size 4)
  [75, 36, 0, -0.3, yappLid,
   "Liberation Sans", 4, "2x 60-LED Lamps  |  5V 10A PSU",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],

  // ── Back wall: IEC C14 label ─────────────────────────────────────────────
  // Cutout BoxInside: Y=47, Z=25, h=48 → top=49
  // Above: (49 + 2 + 2) + 1.5 = 54.5  posx = 47+3 = 50
  [50, 54.5, 0, -0.4, yappBack,
   "Liberation Sans:style=Bold", 4, "POWER IN",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],

  // ── Front wall: USB-C OTA label ─────────────────────────────────────────
  // Cutout BoxInside: Y=47, Z=10, h=8 → top=14
  // Above: (14 + 2 + 2) + 1.5 = 19.5  posx = 47+3 = 50
  [50, 19.5, 0, -0.4, yappFront,
   "Liberation Sans", 4, "OTA",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],

  // ── Left wall: Lamp 1 PG9 label ─────────────────────────────────────────
  // Cutout BoxInside: X=72, Z=25, r=8 → top=33
  // Above: (33 + 2 + 2) + 1.5 = 38.5  posx = 72+3 = 75
  [75, 38.5, 0, -0.4, yappLeft,
   "Liberation Sans", 4, "LAMP 1",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],

  // ── Right wall: Lamp 2 PG9 label ────────────────────────────────────────
  // Same geometry as left wall PG9
  [75, 38.5, 0, -0.4, yappRight,
   "Liberation Sans", 4, "LAMP 2",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],

];

// ─────────────────────────────────────────────────────────────────────────────
// Unused features (leave as empty arrays — do not remove)
// ─────────────────────────────────────────────────────────────────────────────
snapJoins     = [];
boxMounts     = [];
lightTubes    = [];
pushButtons   = [];
displayMounts = [];

// ─────────────────────────────────────────────────────────────────────────────
// YAPP library — MUST be the very last line
// Shared library lives at tools/yapp/YAPPgenerator_v3.scad (repo root)
// Path is relative: reefs/mechanical/enclosure/ → ../../../tools/yapp/
// ─────────────────────────────────────────────────────────────────────────────
include <../../../tools/yapp/YAPPgenerator_v3.scad>
