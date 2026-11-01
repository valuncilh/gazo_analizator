#!/usr/bin/env python3
"""Heuristic check that visible reference/value text boxes do not cross wires."""
from pathlib import Path
import sys
import kicad_sexpr_utils as g

if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 verify_text_clearance.py schematic.kicad_sch")
path = Path(sys.argv[1])
root = g.parse_sexpr(path.read_text(encoding="utf-8"))
segments = []
for wire in g.kids(root, "wire"):
    pts = [(float(p[1]), float(p[2])) for p in g.kids(g.one(wire, "pts"), "xy")]
    segments.extend(zip(pts, pts[1:]))

fields = []
conflicts = []
for symbol in g.kids(root, "symbol"):
    props = {str(p[1]): str(p[2]) for p in g.kids(symbol, "property") if len(p) > 2}
    ref = props.get("Reference", "?")
    for prop in g.kids(symbol, "property"):
        name = str(prop[1])
        if name not in ("Reference", "Value"):
            continue
        effects = g.one(prop, "effects")
        if g.one(prop, "hide") or (effects and g.one(effects, "hide")):
            continue
        value = str(prop[2])
        at = g.one(prop, "at")
        if not at:
            continue
        x, y = float(at[1]), float(at[2])
        angle = float(at[3]) if len(at) > 3 else 0.0
        font = g.one(effects, "font") if effects else None
        size = g.one(font, "size") if font else None
        fs = float(size[1]) if size else 1.5
        # Conservative approximate bounds for default KiCad vector-font text.
        width = max(1.5, len(value) * fs * 0.53)
        height = fs * 1.4
        # KiCad property fields may be rotated. Use their axis-aligned rotated bounds.
        if abs((angle % 180.0) - 90.0) < 1e-5:
            width, height = height, width
        box = (x - width / 2, y - height / 2, x + width / 2, y + height / 2)
        fields.append((ref, name, value, box))
        for (x1, y1), (x2, y2) in segments:
            if abs(y1 - y2) < 1e-5:
                hit = box[1] <= y1 <= box[3] and not (max(x1, x2) < box[0] or min(x1, x2) > box[2])
            elif abs(x1 - x2) < 1e-5:
                hit = box[0] <= x1 <= box[2] and not (max(y1, y2) < box[1] or min(y1, y2) > box[3])
            else:
                hit = False
            if hit:
                conflicts.append((ref, name, value, (x1, y1, x2, y2)))

overlaps = []
for i, first in enumerate(fields):
    for second in fields[i + 1:]:
        a, b = first[3], second[3]
        if not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1]):
            overlaps.append((first[:3], second[:3]))

print(f"Visible fields checked: {len(fields)}")
print(f"Text-wire intersections: {len(conflicts)}")
print(f"Text-text intersections: {len(overlaps)}")
for item in conflicts:
    print("WIRE CONFLICT:", item)
for item in overlaps:
    print("TEXT OVERLAP:", item)
if conflicts or overlaps:
    raise SystemExit("FAIL: possible text clearance collision")
print("PASS: no estimated text collisions")
