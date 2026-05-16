#!/usr/bin/env python
"""
gen_diagrams.py — curtaincinemalights project diagram generator.

Generates all diagram types for the curtaincinemalights project and saves them
to curtaincinemalights/docs/.

Usage
-----
    # From repo root:
    python curtaincinemalights/gen_diagrams.py [--type all|schematic|blocks|concept|wiring]

    # Or use the shared CLI runner:
    python tools/gen_diagrams.py curtaincinemalights [--type all|schematic|blocks|concept|wiring]
"""

from __future__ import annotations
import argparse
import os
import sys

# ── Bootstrap: resolve repo root and add tools/ to path ──────────────────────
HERE     = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(HERE)
TOOLS    = os.path.join(REPO_DIR, "tools")
DOCS     = os.path.join(HERE, "docs")

sys.path.insert(0, TOOLS)

from diagram_gen import blocks, concept, schematic, wiring  # noqa: E402
from gen_diagrams_config import DIAGRAM_CONFIG as CFG        # noqa: E402


def run_all(types: list[str]) -> None:
    os.makedirs(DOCS, exist_ok=True)

    if "schematic" in types:
        print("[schematic]")
        schematic.draw_level_shifter_circuit(
            os.path.join(DOCS, "schematic-level-shifter.png"))
        schematic.draw_power_circuit(
            os.path.join(DOCS, "schematic-power.png"))

    if "blocks" in types:
        print("[blocks]")
        blocks.draw_system_blocks(CFG,
            os.path.join(DOCS, "concept-system.png"))

    if "concept" in types:
        print("[concept]")
        concept.draw_side_view(
            {"title": "CURTAINCINEMALIGHTS  –  Side View  (not to scale)",
             "wood_label": "ALUM. TRACK"},
            os.path.join(DOCS, "concept-side-view.png"))
        concept.draw_top_view(
            {"title": "CURTAINCINEMALIGHTS  –  Top-Down Floor Plan",
             "lamps": CFG["lamps"],
             "box_pos": CFG["box_pos"]},
            os.path.join(DOCS, "concept-top-view.png"))

    if "wiring" in types:
        print("[wiring]")
        wiring.draw_physical_wiring(
            CFG, os.path.join(DOCS, "wiring-physical"))


def main():
    parser = argparse.ArgumentParser(
        description="Generate diagrams for the curtaincinemalights project.")
    parser.add_argument("--type", default="all",
                        choices=["all", "schematic", "blocks", "concept", "wiring"],
                        help="Diagram type to generate (default: all)")
    args = parser.parse_args()

    if args.type == "all":
        types = ["schematic", "blocks", "concept", "wiring"]
    else:
        types = [args.type]

    print(f"\n→ Generating curtaincinemalights diagrams: {', '.join(types)}\n")
    run_all(types)
    print("\n✓ Done — see curtaincinemalights/docs/\n")


if __name__ == "__main__":
    main()
