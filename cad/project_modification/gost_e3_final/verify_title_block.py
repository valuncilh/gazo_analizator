#!/usr/bin/env python3
"""Validate KiCad title_block comment indices (KiCad uses 1..9)."""
from pathlib import Path
import sys
import kicad_sexpr_utils as g

if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 verify_title_block.py schematic.kicad_sch")

path = Path(sys.argv[1])
root = g.parse_sexpr(path.read_text(encoding="utf-8"))
if g.head(root) != "kicad_sch":
    raise SystemExit("FAIL: root token is not kicad_sch")

title_blocks = g.kids(root, "title_block")
if len(title_blocks) != 1:
    raise SystemExit(f"FAIL: expected one title_block section, found {len(title_blocks)}")

comments = g.kids(title_blocks[0], "comment")
indices = []
for comment in comments:
    if len(comment) != 3:
        raise SystemExit(f"FAIL: malformed title-block comment: {comment}")
    try:
        index = int(str(comment[1]))
    except ValueError:
        raise SystemExit(f"FAIL: non-integer title-block comment index: {comment[1]}")
    if not 1 <= index <= 9:
        raise SystemExit(f"FAIL: KiCad title-block comment indices must be 1..9, got {index}")
    indices.append(index)

if len(indices) != len(set(indices)):
    raise SystemExit(f"FAIL: duplicate title-block comment index: {indices}")

print(f"Title-block comments: PASS ({indices if indices else 'none'})")
