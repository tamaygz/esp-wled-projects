"""
gen_diagrams_config.py — curtaincinemalights project diagram configuration.

Imported automatically by tools/gen_diagrams.py.
"""

from __future__ import annotations

DIAGRAM_CONFIG: dict = {
    "project":    "curtaincinemalights",
    "title":      "CURTAINCINEMALIGHTS  –  ESP8266 WLED Cinema Curtain Sync",

    # Power / control hardware
    "psu":        "Hi-Link HLK-20M05\n5V / 4A",
    "controller": "ESP8266 D1 Mini\nWLED v0.15",
    "shifter":    "74AHCT125\n3.3 → 5V",
    "power_label": "5V / 4A PSU",

    # LED outputs (single output, two virtual segments)
    "outputs": [
        {"name": "CURTAIN", "strip": "SK6812 GRBW\n~180 LEDs · 3 m"},
    ],

    # Smart-home integration
    "integration": "Home\nAssistant",

    # GPIO mapping for wiring diagram
    "gpio_map": [
        {"gpio": 2, "label": "CURTAIN DATA (D4)", "color": "#e53935"},
    ],

    # Concept top-view: LED track position along the curtain wall
    # cx = rough x-position in the room layout (meters from left corner)
    "lamps": [
        {"label": "CURTAIN\nTRACK", "cx": 6.0},
    ],
    "box_pos":    (9.5, 0.8),
    "wood_label": "ALUM. TRACK",
}
