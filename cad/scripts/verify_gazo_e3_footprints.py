#!/usr/bin/env python3
"""Source-level checks for GazoE3 custom footprint pad maps.

This script is not a substitute for KiCad 10 library loading, footprint checks,
PCB DRC, or physical inspection of the purchased components.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / "cad" / "kicad" / "footprints" / "GazoE3.pretty"

EXPECTED = {
    "HCM1206X_P7.6mm.kicad_mod": {
        "1": (-3.8, 0.0),
        "2": (3.8, 0.0),
    },
    "NKK_AS11AP_SPST_P5.08mm.kicad_mod": {
        "1": (0.0, -2.54),
        "2": (0.0, 2.54),
    },
}
PAD_RE = re.compile(
    r'\(pad\s+"(?P<num>\d+)"\s+\w+\s+\w+\s+'
    r'\(at\s+(?P<x>-?\d+(?:\.\d+)?)\s+(?P<y>-?\d+(?:\.\d+)?)'
)


def main() -> int:
    errors: list[str] = []
    for filename, expected in EXPECTED.items():
        path = LIB / filename
        if not path.is_file():
            errors.append(f"Missing footprint: {path}")
            continue
        source = path.read_text(encoding="utf-8")
        actual = {
            m.group("num"): (float(m.group("x")), float(m.group("y")))
            for m in PAD_RE.finditer(source)
        }
        if actual != expected:
            errors.append(f"{filename}: pad map mismatch. expected={expected}, actual={actual}")
        if "(attr through_hole)" not in source:
            errors.append(f"{filename}: not marked through_hole")
        if len(actual) != len(expected):
            errors.append(f"{filename}: duplicate or missing pad numbers")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS: custom GazoE3 source footprint files and pad-number maps are consistent.")
    print("NOTE: no KiCad 10 validation or physical fit approval is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
