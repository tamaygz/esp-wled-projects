// reefs-automatedvariant-enclosure.scad
// Project: Reefs — WLED Driftwood Ambient Lighting
//
// Outer dimensions: 150 x 100 x 59 mm  (spec: <= 150 x 100 x 60 mm OK)
// Inner dimensions: 144 x 94 x 56 mm
// Wall: 3 mm  Base floor: 1.5 mm  Lid ceiling: 1.5 mm
//
// Shared library: tools/yapp/YAPPgenerator_v3.scad
//
// Render commands (from this directory):
//   Base only:
//     openscad --render -o reefs-automatedvariant-base.stl reefs-automatedvariant-enclosure.scad -D "printLidShell=false"
//   Lid only:
//     openscad --render -o reefs-automatedvariant-lid.stl reefs-automatedvariant-enclosure.scad -D "printBaseShell=false"
//
// NOTE: include comes FIRST so our variable definitions below override the
// library defaults (OpenSCAD "last assignment wins").
// YAPPgenerate() is called explicitly to bypass the library's if(debug) guard.

include <../../../tools/yapp/YAPPgenerator_v3.scad>

// ---- Render flags ----
printBaseShell      = true;
printLidShell       = true;
showSideBySide      = true;
printerLayerHeight  = 0.2;
renderQuality       = 8;

// ---- Box dimensions (virtual-PCB approach, all padding=0) ----
// inner L = 144 mm  outer L = 150 mm
// inner W =  94 mm  outer W = 100 mm
// inner Z = 1.5 + 30 + 26 + 1.5 = 59 mm outer
pcbLength           = 144;
pcbWidth            = 94;
pcbThickness        = 1.6;
standoffHeight      = 5.0;
standoffDiameter    = 7.0;
standoffPinDiameter = 3.0;
standoffHoleSlack   = 0.4;

paddingFront        = 0;
paddingBack         = 0;
paddingRight        = 0;
paddingLeft         = 0;

wallThickness       = 3.0;
basePlaneThickness  = 1.5;
lidPlaneThickness   = 1.5;
baseWallHeight      = 30;
lidWallHeight       = 26;
// ridgeHeight must be >= wallThickness * 1.8 for snapJoins (YAPP wallToRidgeRatio)
ridgeHeight         = 6.0;
ridgeSlack          = 0.3;
ridgeGap            = 0.5;
roundRadius         = 3.0;
boxType             = 0;

// ---- PCB (YAPP v3 format) ----
pcb = [
  ["Main", pcbLength, pcbWidth, 0, 0, pcbThickness,
   standoffHeight, standoffDiameter, standoffPinDiameter, standoffHoleSlack],
];

// ---- ESP32 DevKit 38-pin standoffs (4x M3) ----
// Board ~30x51 mm, hole pattern 45x23 mm centre-to-centre
// Orientation: USB-C toward FRONT (high X)
pcbStands = [
  [81,  35, standoffHeight, 0, standoffDiameter, standoffPinDiameter,
   standoffHoleSlack, yappBaseOnly, yappPin, yappBackLeft,   yappCoordPCB],
  [81,  58, standoffHeight, 0, standoffDiameter, standoffPinDiameter,
   standoffHoleSlack, yappBaseOnly, yappPin, yappBackRight,  yappCoordPCB],
  [126, 35, standoffHeight, 0, standoffDiameter, standoffPinDiameter,
   standoffHoleSlack, yappBaseOnly, yappPin, yappFrontLeft,  yappCoordPCB],
  [126, 58, standoffHeight, 0, standoffDiameter, standoffPinDiameter,
   standoffHoleSlack, yappBaseOnly, yappPin, yappFrontRight, yappCoordPCB],
];

// ---- Lid closure: SNAP-ON (no screws) ----
// 4 snap-joins centred on the two long walls (yappSymmetric mirrors each entry
// about the wall midline). Width 15 mm per snap. Tool-free open/close.
connectors = [];

// ---- BACK wall: Schuko captive mains lead entry (Ø8 mm) + 2x M3 clamp bosses ----
// Round Ø8 mm hole for the cable jacket; flanked by two Ø3.2 mm screw holes
// (12 mm pitch each side of centre) for a printed external cable clamp that
// compresses the cable jacket with two M3 × 8 screws into brass inserts.
cutoutsBack = [
  [47, 30, 0, 0, 4, yappCircle, 0, 0, yappCoordBoxInside, yappCenter],  // Ø8 cable hole
  [35, 30, 0, 0, 1.6, yappCircle, 0, 0, yappCoordBoxInside, yappCenter],  // clamp screw L
  [59, 30, 0, 0, 1.6, yappCircle, 0, 0, yappCoordBoxInside, yappCenter],  // clamp screw R
];

// ---- FRONT wall: USB-C OTA slot (12x8 mm) ----
cutoutsFront = [
  [47, 10, 12, 8, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
];

// ---- LEFT wall: Lamp1 JST SM panel-mount pocket + 4 vent slots ----
// Pocket = rectangular 9.5 x 6 mm cutout that traps the female JST SM body
// from inside; the cable hole on the outside is narrower than the connector
// shoulders so it cannot pull through.
cutoutsLeft = [
  [15,  20, 15,  4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [40,  20, 15,  4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [72,  25, 9.5, 6, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],  // JST SM pocket
  [104, 20, 15,  4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [129, 20, 15,  4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
];

// ---- RIGHT wall: Lamp2 JST SM panel-mount pocket + 4 vent slots (mirror) ----
cutoutsRight = [
  [15,  20, 15,  4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [40,  20, 15,  4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [72,  25, 9.5, 6, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],  // JST SM pocket
  [104, 20, 15,  4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
  [129, 20, 15,  4, 0, yappRectangle, 0, 0, yappCoordBoxInside, yappCenter],
];

cutoutsLid   = [];
cutoutsBase  = [];

// ---- Labels ----
labelsPlane = [
  // Lid: project title (3 lines, raised engraving)
  [75, 66, 0, -0.6, yappLid,
   "Liberation Sans:style=Bold", 10, "REEFS",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  [75, 50, 0, -0.4, yappLid,
   "Liberation Sans", 6, "WLED v16  |  SK6812 RGBW",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  [75, 36, 0, -0.3, yappLid,
   "Liberation Sans", 4, "2x 60-LED Lamps  |  5V 10A PSU",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  // Back wall: mains entry label
  [50, 54.5, 0, -0.4, yappBack,
   "Liberation Sans:style=Bold", 4, "MAINS",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  // Front wall: USB-C OTA label
  [50, 19.5, 0, -0.4, yappFront,
   "Liberation Sans", 4, "OTA",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  // Left wall: Lamp 1 PG9 label
  [75, 38.5, 0, -0.4, yappLeft,
   "Liberation Sans", 4, "LAMP 1",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
  // Right wall: Lamp 2 PG9 label
  [75, 38.5, 0, -0.4, yappRight,
   "Liberation Sans", 4, "LAMP 2",
   0, yappTextLeftToRight, yappTextHAlignCenter, yappTextVAlignCenter],
];

// ---- Snap-on lid joins ----
// posx=40 on each long wall, mirrored to posx=110 via yappSymmetric => 4 snaps total.
// Width 15 mm. Requires ridgeHeight >= wallThickness * 1.8 (= 5.4 mm); we use 6.0.
snapJoins = [
  [40, 15, yappLeft, yappRight, yappCenter, yappSymmetric],
];
boxMounts     = [];
lightTubes    = [];
pushButtons   = [];
displayMounts = [];
imagesPlane   = [];

// ---- Generate geometry (bypasses library if(debug) guard) ----
YAPPgenerate();