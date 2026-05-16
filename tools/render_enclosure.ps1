# Render an enclosure: base STL, lid STL, plus 2 preview PNGs per part.
#
# Usage (from any cwd):
#   pwsh tools/render_enclosure.ps1 -Project reefs -ScadName reefs-automatedvariant-enclosure
#
# Outputs into <project>/mechanical/enclosure/:
#   <stem>-base.stl
#   <stem>-lid.stl
#   <stem>-base-iso.png   (isometric, perspective)
#   <stem>-base-top.png   (top-down, orthogonal)
#   <stem>-lid-iso.png
#   <stem>-lid-top.png
#
# Requires OpenSCAD on PATH or at the default install path.

[CmdletBinding()]
param(
  [Parameter(Mandatory)] [string] $Project,
  [Parameter(Mandatory)] [string] $ScadName,      # filename stem of the .scad (without extension)
  [string] $OpenScad   = "C:\Program Files\OpenSCAD\openscad.exe",
  [int]    $ImgW       = 1400,
  [int]    $ImgH       = 1000,
  [string] $ColorScheme = "Tomorrow"
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path "$PSScriptRoot\..").Path
$encDir   = Join-Path $repoRoot "$Project\mechanical\enclosure"
$scad     = Join-Path $encDir "$ScadName.scad"

if (-not (Test-Path $scad))      { throw "SCAD not found: $scad" }
if (-not (Test-Path $OpenScad))  { throw "OpenSCAD not found at: $OpenScad" }

$stem = $ScadName -replace '-enclosure$',''   # e.g. reefs-automatedvariant
$base = Join-Path $encDir "$stem-base.stl"
$lid  = Join-Path $encDir "$stem-lid.stl"

function Invoke-OpenScad {
  param([string[]] $ScadArgs, [string] $Label)
  $errF = Join-Path $env:TEMP "openscad-$Label-$([guid]::NewGuid().ToString('N')).log"
  $outF = "$errF.out"
  Write-Host "[$Label] openscad $($ScadArgs -join ' ')"
  $p = Start-Process -FilePath $OpenScad -ArgumentList $ScadArgs -Wait -NoNewWindow `
       -PassThru -RedirectStandardError $errF -RedirectStandardOutput $outF
  if ($p.ExitCode -ne 0) {
    Write-Host (Get-Content $errF -Raw)
    throw "[$Label] OpenSCAD failed (exit $($p.ExitCode))"
  }
  Remove-Item $errF, $outF -ErrorAction SilentlyContinue
}

# --- STL renders ---
Invoke-OpenScad -Label "base-stl" -ScadArgs @(
  "--render","-o",$base,$scad,"-D","printLidShell=false"
)
Invoke-OpenScad -Label "lid-stl"  -ScadArgs @(
  "--render","-o",$lid,$scad,"-D","printBaseShell=false"
)

# --- Preview PNGs ---
# We render directly from the .scad with single-shell flags so the camera
# auto-fits to just the part being shown.
#
# Camera: --camera=tx,ty,tz,rx,ry,rz,dist
#   iso: rotation (55, 0, 25), with --viewall to auto-fit distance
#   top: rotation (0, 0, 0)  + ortho projection

function Render-Png {
  param([string] $Out, [string[]] $ShellFlag, [string[]] $CameraArgs, [string] $Label)
  $a = @(
    "-o",$Out,$scad,
    "--imgsize=$ImgW,$ImgH",
    "--colorscheme=$ColorScheme",
    "--viewall","--autocenter"
  ) + $CameraArgs + @("-D",$ShellFlag[0])
  Invoke-OpenScad -Label $Label -ScadArgs $a
}

# Isometric (perspective): rotation 55,0,25
$iso = @("--camera=0,0,0,55,0,25,0","--projection=perspective")
# Top-down (orthogonal): rotation 0,0,0
$top = @("--camera=0,0,0,0,0,0,0",  "--projection=orthogonal")

Render-Png -Out (Join-Path $encDir "$stem-base-iso.png") -ShellFlag @("printLidShell=false")  -CameraArgs $iso -Label "base-iso"
Render-Png -Out (Join-Path $encDir "$stem-base-top.png") -ShellFlag @("printLidShell=false")  -CameraArgs $top -Label "base-top"
Render-Png -Out (Join-Path $encDir "$stem-lid-iso.png")  -ShellFlag @("printBaseShell=false") -CameraArgs $iso -Label "lid-iso"
Render-Png -Out (Join-Path $encDir "$stem-lid-top.png")  -ShellFlag @("printBaseShell=false") -CameraArgs $top -Label "lid-top"

Write-Host ""
Write-Host "Done. Artifacts in $encDir :"
Get-ChildItem $encDir -Filter "$stem-*" | Where-Object { $_.Extension -in ".stl",".png" } |
  Sort-Object Name | ForEach-Object { "  {0,-40} {1,12:N0} bytes" -f $_.Name, $_.Length } |
  Write-Host
