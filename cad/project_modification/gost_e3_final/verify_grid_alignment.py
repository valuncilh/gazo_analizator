#!/usr/bin/env python3
"""Check the schematic's electrical geometry is aligned to the 1.27 mm grid."""
from __future__ import annotations
import math
import sys
from pathlib import Path
import kicad_sexpr_utils as sx

GRID = 1.27
TOL = 0.02

def on_grid(value: float) -> bool:
    return abs(value - round(value / GRID) * GRID) <= TOL

if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 verify_grid_alignment.py schematic.kicad_sch")
path = Path(sys.argv[1])
root = sx.parse_sexpr(path.read_text(encoding="utf-8"))
if sx.head(root) != "kicad_sch":
    raise SystemExit("FAIL: root token is not kicad_sch")

issues: list[str] = []
wire_points = 0
for wire in sx.kids(root, "wire"):
    points = sx.kids(sx.one(wire, "pts"), "xy")
    for p in points:
        x, y = float(p[1]), float(p[2])
        wire_points += 1
        if not on_grid(x) or not on_grid(y):
            issues.append(f"wire endpoint ({x:.4f}, {y:.4f})")

for kind in ("junction", "label", "global_label", "hierarchical_label", "no_connect"):
    for obj in sx.kids(root, kind):
        at = sx.one(obj, "at")
        if at:
            x, y = float(at[1]), float(at[2])
            if not on_grid(x) or not on_grid(y):
                issues.append(f"{kind} anchor ({x:.4f}, {y:.4f})")

symbol_origins = 0
for sym in sx.kids(root, "symbol"):
    at = sx.one(sym, "at")
    if at:
        x, y = float(at[1]), float(at[2])
        symbol_origins += 1
        if not on_grid(x) or not on_grid(y):
            ref = next((str(p[2]) for p in sx.kids(sym, "property")
                        if len(p) > 2 and str(p[1]) == "Reference"), "?")
            issues.append(f"symbol {ref} origin ({x:.4f}, {y:.4f})")

# Check local coordinates of all used library pins too. If symbol origins and
# pin offsets are both on-grid, every instantiated pin lands on the grid.
lib = sx.one(root, "lib_symbols")
lib_map = {str(s[1]): s for s in sx.kids(lib, "symbol")}
used = {str(sx.one(s, "lib_id")[1]) for s in sx.kids(root, "symbol")}
for lib_id in sorted(used):
    if lib_id not in lib_map:
        issues.append(f"missing embedded library symbol {lib_id}")
        continue
    for unit in sx.kids(lib_map[lib_id], "symbol"):
        for pin in sx.kids(unit, "pin"):
            at = sx.one(pin, "at")
            if at:
                dx, dy = float(at[1]), float(at[2])
                if not on_grid(dx) or not on_grid(dy):
                    number = sx.one(pin, "number")
                    pnum = str(number[1]) if number else "?"
                    issues.append(f"library pin {lib_id}.{pnum} offset ({dx:.4f}, {dy:.4f})")

print(f"Wire endpoints checked: {wire_points}")
print(f"Symbol origins checked: {symbol_origins}")
print(f"Embedded symbol libraries checked: {len(used)}")
if issues:
    for issue in issues[:80]:
        print("OFF GRID:", issue)
    raise SystemExit(f"FAIL: {len(issues)} electrical geometry items are off the {GRID:.2f} mm grid")
print(f"PASS: electrical geometry aligned to {GRID:.2f} mm grid")
