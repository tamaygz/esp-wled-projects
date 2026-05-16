"""
gen_diagrams_config.py — Reefs project diagram configuration.

Imported automatically by tools/gen_diagrams.py.
"""

from __future__ import annotations

DIAGRAM_CONFIG: dict = {
    "project":    "reefs",
    "title":      "REEFS  –  ESP32 WLED Ambient Lighting",

    # Power / control hardware
    "psu":        "Honeywell PSU\n5V / 10A",
    "controller": "ESP32-WROOM-32\nWLED v16+",
    "shifter":    "74AHCT125\n3.3 → 5V",
    "power_label": "5V / 10A PSU",

    # LED outputs
    "outputs": [
        {"name": "LAMP 1", "strip": "SK6812 GRBW\n60 LEDs · 1 m"},
        {"name": "LAMP 2", "strip": "SK6812 GRBW\n60 LEDs · 1 m"},
    ],

    # Smart-home integration
    "integration": "Home\nAssistant",

    # GPIO mapping for wiring diagram
    "gpio_map": [
        {"gpio": 16, "label": "LAMP 1 DATA", "color": "#43a047"},
        {"gpio": 17, "label": "LAMP 2 DATA", "color": "#26c6da"},
    ],

    # Concept top-view: lamp positions (cx = x along the wall)
    "lamps": [
        {"label": "LAMP 1", "cx": 3.0},
        {"label": "LAMP 2", "cx": 8.5},
    ],
    "box_pos": (9.5, 0.8),
    "wood_label": "DRIFTWOOD",
}
