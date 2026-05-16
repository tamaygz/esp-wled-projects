// ============================================================
// curtaincinemalights — YAPP_Box v3 enclosure
// ESP8266 D1 Mini v4 + Hi-Link HLK-20M05 (5V 4A)
//
// Component dimensions from tools/parts-register/parts.json:
//   D1_MINI_V4  : 34.2 × 25.6 × 10.0 mm  (verified ✅)
//   HLK_20M05   : 56.0 × 32.0 × 22.5 mm  (verified ✅)
//   JST_SM_2P5_3PIN : pocket 9.5 × 6.0 mm (⚠️ estimated body)
//
// Layout (inner, top-down view):
//   X (front → back): 0 ────────────── 100 mm
//   Y (left  → right): 0 ─────────── 40 mm
//
//   Front zone (x = 0–38): D1 Mini  (34.2 mm × 25.6 mm), centered in Y
//   Back  zone (x = 42–100): HLK-20M05 (56 mm × 32 mm), centered in Y
//
// Outer envelope: ~106 × 46 × 44 mm
// ============================================================
include <../../../tools/yapp/YAPPgenerator_v3.scad>

// ---- Box dimensions (inner) -----------------------------------
pcbLength  = 100;   // X axis: front-to-back
pcbWidth   =  40;   // Y axis: left-to-right
pcbThickness = 1.6; // dummy — no real PCB (components direct-fit)

wallThickness     = 3.0;
basePlaneThickness = 1.5;
lidPlaneThickness  = 1.5;
baseWallHeight    = 25;   // HLK-20M05 height 22.5 mm + 2.5 mm clearance
lidWallHeight     = 10;   // lid shell depth
ridgeHeight       = 6.0;  // >= wallThickness * 1.8 = 5.4; use 6.0
ridgeSlack        = 0.3;
ridgeGap          = 0.5;
roundRadius       = 3.0;
boxType           = 0;

// ---- Standoff settings (shared params) -----------------------
standoffHeight      = 5.0;
standoffDiameter    = 5.0;
standoffPinDiameter = 2.5;
standoffHoleSlack   = 0.2;
pcbThick            = 1.6;

// ---- PCB (dummy — no PCB, both components direct-fit) ---------
pcb = [
  ["Main", pcbLength, pcbWidth, 0, 0, pcbThick,
   standoffHeight, standoffDiameter, standoffPinDiameter, standoffHoleSlack],
];

// ---- No standoffs (D1 Mini and HLK-20M05 have no mounting holes) ----
// Both components are held by friction-fit side walls:
//   D1 Mini  : friction-fit pocket at front; USB-C faces front wall
//   HLK-20M05: friction-fit pocket at back; DIP pins face left wall
// A small printed 1.5mm rib at y=28mm and y=8mm retains D1 Mini laterally.
// (Rib not modeled in YAPP — add if D1 Mini shifts during assembly.)
pcbStands = [];

// ---- Lid closure: snap-on (no screws) ------------------------
// Two snap-joins per long wall (yappSymmetric mirrors each entry
// about the wall midline). ridgeHeight=6.0 provides adequate snap depth.
connectors = [];

snapJoins = [
  // [posX, width, wall1, wall2, centering, symmetric]
  [30, 12, yappLeft, yappRight, yappCenter, yappSymmetric],
];

// ============================================================
// CUTOUTS
// Coordinate convention with yappCoordBoxInside + yappCenter:
//   cutoutsFront/Back  : [posY_fromLeft, posZ_fromFloor, w, h, r, shape, ...]
//   cutoutsLeft/Right  : [posX_fromFront, posZ_fromFloor, w, h, r, shape, ...]
// All measurements refer to the cutout CENTER.
// ============================================================

// ---- FRONT wall: USB-C slot for D1 Mini OTA/flashing --------
// D1 Mini centered in Y at 20mm; USB-C center ~5mm from floor
// Slot: 9.0 mm wide × 3.5 mm high (from D1_MINI_V4 register)
cutoutsFront = [
  [20, 5.0, 9.0, 3.5, 0.5, yappRoundedRect, 0, 0, yappCoordBoxInside, yappCenter],
];

// ---- BACK wall: mains cable entry, Ø9 mm hole ---------------
// Cable jacket diameter ~9mm for H05VV-F 3×0.75; center at mid-height
cutoutsBack = [
  [20, 14, 0, 0, 4.5, yappCircle, 0, 0, yappCoordBoxInside, yappCenter],  // Ø9 cable hole
];

// ---- LEFT wall: JST SM 3-pin panel-mount pocket -------------
// Pocket traps the female JST SM connector body from inside.
// Pocket: 9.5 × 6.0 mm (from JST_SM_2P5_3PIN register ⚠️).
// Positioned at x=75 (near HLK output terminals, back-half of box).
cutoutsLeft = [
  [75, 14, 9.5, 6.0, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],  // JST SM pocket
  // Vent slots for PSU heat dissipation
  [55, 20, 12, 3, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [72, 20, 12, 3, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [89, 20, 12, 3, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
];

// ---- RIGHT wall: vent slots (mirror of left, no connector) --
cutoutsRight = [
  [55, 20, 12, 3, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [72, 20, 12, 3, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [89, 20, 12, 3, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
];

cutoutsLid  = [];
cutoutsBase = [];

// ---- Labels (raised engraving) --------------------------------
labelsPlane = [
  // Lid: project name (large) + strip / controller info (small)
  [53, 26, 0, -0.6, yappLid,
   "Liberation Sans:style=Bold", 9, "CURTAIN CINEMA",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  [53, 14, 0, -0.4, yappLid,
   "Liberation Sans", 5, "WLED v0.15  |  SK6812 RGBW",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  // Back wall: mains entry label
  [21, 22, 0, -0.4, yappBack,
   "Liberation Sans:style=Bold", 4, "MAINS",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  // Front wall: OTA label
  [21, 11, 0, -0.4, yappFront,
   "Liberation Sans", 4, "OTA",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  // Left wall: LED strip output label
  [74, 22, 0, -0.4, yappLeft,
   "Liberation Sans", 4, "LED STRIP",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
];

// ---- Not used in this design ----------------------------------
boxMounts     = [];
lightTubes    = [];
pushButtons   = [];
displayMounts = [];
imagesPlane   = [];

// ---- Generate geometry ----------------------------------------
YAPPgenerate();
