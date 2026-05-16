wallThickness=2.8; basePlaneThickness=1.6; lidPlaneThickness=1.6;
pcbLength=100; pcbWidth=60; pcbThickness=1.6;
standoffHeight=5; standoffDiameter=7; standoffPinDiameter=2.4; standoffHoleSlack=0.4;
paddingFront=1; paddingBack=1; paddingRight=1; paddingLeft=1;
baseWallHeight=10; lidWallHeight=10; ridgeHeight=3; ridgeSlack=0.2; roundRadius=3;
printBaseShell=true; printLidShell=true; boxType=0;
pcb=[["Main",pcbLength,pcbWidth,0,0,pcbThickness,standoffHeight,standoffDiameter,standoffPinDiameter,standoffHoleSlack]];
pcbStands=[]; connectors=[]; cutoutsBase=[]; cutoutsLid=[]; cutoutsFront=[]; cutoutsBack=[]; cutoutsLeft=[]; cutoutsRight=[]; snapJoins=[]; boxMounts=[]; lightTubes=[]; pushButtons=[]; displayMounts=[]; labelsPlane=[];
include <c:\Users\Tamay\vscode\esp-wled-projects\reefs\mechanical\enclosure\..\..\..\tools\yapp\YAPPgenerator_v3.scad>
