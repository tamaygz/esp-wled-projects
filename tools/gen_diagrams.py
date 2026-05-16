#!/usr/bin/env python
"""
gen_diagrams.py — CLI runner for the diagram_gen toolkit.

Usage
-----
    python tools/gen_diagrams.py <project> [--type all|schematic|blocks|concept|wiring]

Examples
--------
    python tools/gen_diagrams.py reefs
    python tools/gen_diagrams.py reefs --type schematic
    python tools/gen_diagrams.py reefs --type concept

The project must have a gen_diagrams_config.py at its root that exports a
DIAGRAM_CONFIG dict (see _template/gen_diagrams_config.py for the full schema).

If no config file is found, a minimal default config is used so the runner
always produces something useful even for new/empty projects.
"""

from __future__ import annotations
import argparse
import importlib.util
import os
import sys


# ── Bootstrap: make diagram_gen importable ────────────────────────────────────
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.dirname(TOOLS_DIR)
sys.path.insert(0, TOOLS_DIR)

from diagram_gen import blocks, concept, schematic, wiring  # noqa: E402


# ── Default config ─────────────────────────────────────────────────────────────
DEFAULT_CONFIG = {
    "project":    "unnamed",
    "title":      "Lighting Project",
    "psu":        "5 V PSU",
    "controller": "ESP32\nWLED firmware",
    "shifter":    "74AHCT125\n3.3→5V shift",
    "outputs": [
        {"name": "LAMP 1", "strip": "SK6812 RGBW\n60 LEDs"},
    ],
    "integration": "Home\nAssistant",
    "lamps": [
        {"label": "LAMP 1", "cx": 6.0},
    ],
    "gpio_map": [
        {"gpio": 16, "label": "DATA 1", "color": "#43a047"},
    ],
}


# ── Config loader ──────────────────────────────────────────────────────────────
def load_config(project: str) -> dict:
    project_dir = os.path.join(REPO_ROOT, project)
    config_path = os.path.join(project_dir, "gen_diagrams_config.py")

    if not os.path.isdir(project_dir):
        sys.exit(f"Error: project directory not found: {project_dir}")

    if os.path.isfile(config_path):
        spec = importlib.util.spec_from_file_location("cfg", config_path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cfg = getattr(mod, "DIAGRAM_CONFIG", {})
        print(f"  config:    loaded {config_path}")
    else:
        cfg = {}
        print(f"  config:    no gen_diagrams_config.py found — using defaults")

    merged = {**DEFAULT_CONFIG, **cfg}
    merged["_project_dir"] = project_dir
    return merged


# ── Generators ────────────────────────────────────────────────────────────────
def run_schematic(cfg: dict) -> None:
    docs = os.path.join(cfg["_project_dir"], "docs")
    schematic.draw_level_shifter_circuit(os.path.join(docs, "schematic-level-shifter.png"))
    schematic.draw_power_circuit(os.path.join(docs, "schematic-power.png"))


def run_blocks(cfg: dict) -> None:
    docs = os.path.join(cfg["_project_dir"], "docs")
    blocks.draw_system_blocks(cfg, os.path.join(docs, "concept-system.png"))


def run_concept(cfg: dict) -> None:
    docs = os.path.join(cfg["_project_dir"], "docs")
    concept.draw_side_view(
        {"title": f"{cfg['title']}  —  Side View  (not to scale)",
         "wood_label": cfg.get("wood_label", "DRIFTWOOD")},
        os.path.join(docs, "concept-side-view.png"))

    lamp_cfg = {
        "title":    f"{cfg['title']}  —  Top-Down Floor Plan",
        "lamps":    cfg.get("lamps", DEFAULT_CONFIG["lamps"]),
        "box_pos":  cfg.get("box_pos", (9.5, 0.8)),
    }
    concept.draw_top_view(lamp_cfg, os.path.join(docs, "concept-top-view.png"))


def run_wiring(cfg: dict) -> None:
    docs = os.path.join(cfg["_project_dir"], "docs")
    wiring.draw_physical_wiring(cfg, os.path.join(docs, "wiring-physical"))


GENERATORS = {
    "schematic": run_schematic,
    "blocks":    run_blocks,
    "concept":   run_concept,
    "wiring":    run_wiring,
}


# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Generate diagrams for an esp-wled-project.")
    parser.add_argument("project",
                        help="Project subfolder name (e.g. reefs)")
    parser.add_argument("--type", default="all",
                        choices=["all"] + list(GENERATORS.keys()),
                        help="Diagram type(s) to generate (default: all)")
    args = parser.parse_args()

    print(f"\n→ Generating diagrams for: {args.project}  (type={args.type})\n")
    cfg = load_config(args.project)

    if args.type == "all":
        for name, fn in GENERATORS.items():
            print(f"[{name}]")
            fn(cfg)
    else:
        fn = GENERATORS[args.type]
        print(f"[{args.type}]")
        fn(cfg)

    print(f"\n✓ Done — check {args.project}/docs/")


if __name__ == "__main__":
    main()
