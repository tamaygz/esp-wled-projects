"""
diagram_gen — shared diagram generation toolkit for esp-wled-projects.

Usage (from any project's gen_diagrams.py):
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools'))
    from diagram_gen import blocks, concept, schematic, wiring

Sub-modules
-----------
style       Shared dark-theme palette, fonts, dimension constants
blocks      System block diagrams (matplotlib)
concept     Real-world concept illustrations: side-view, top-down (matplotlib)
schematic   Electrical circuit schematics (schemdraw)
wiring      Physical wiring diagrams with color-coded wires (drawsvg)
"""

from . import style, blocks, concept, schematic, wiring

__all__ = ["style", "blocks", "concept", "schematic", "wiring"]
