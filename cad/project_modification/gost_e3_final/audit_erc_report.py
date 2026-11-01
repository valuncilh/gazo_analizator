#!/usr/bin/env python3
"""Classify native KiCad ERC output without suppressing any rules.

For this schematic, only footprint assignment warnings (package selection has
not been frozen yet) and the intentional isolated AOUT measurement label are
accepted as documented non-electrical warnings. Any electrical, geometric,
connectivity, or library warning fails the review.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 audit_erc_report.py reports/kicad10/erc.rpt")
path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="replace")
rule_counts = Counter(re.findall(r"^\[([a-zA-Z0-9_]+)\]:", text, re.M))
errors = len(re.findall(r"^\s*;\s*error\s*$", text, re.M | re.I))
warnings = len(re.findall(r"^\s*;\s*warning\s*$", text, re.M | re.I))

allowed = {"footprint_filter", "isolated_pin_label"}
unexpected = {rule: count for rule, count in rule_counts.items() if rule not in allowed}
# The current drawing contains exactly these 17 symbols without a frozen
# physical package assignment. Do not silently accept new footprint warnings.
allowed_footprint_refs = {
    "A1", "XS1", "R1", "R2", "R3", "R4", "R5", "R6", "R7",
    "C1", "C2", "C3", "DA1", "VD1", "HA1", "HL1", "HL2",
}
footprint_refs = set(re.findall(r"\[footprint_filter\]:[^\n]*\n\s*;\s*warning\s*\n\s*@\([^\n]*\):\s*Символ\s+([^\s\[]+)", text))

print(f"ERC errors: {errors}")
print(f"ERC warnings: {warnings}")
for rule, count in sorted(rule_counts.items()):
    print(f"  {rule}: {count}")

failed = errors > 0 or bool(unexpected)
if rule_counts.get("isolated_pin_label", 0) != 1 or "AOUT" not in text:
    failed = True
    print("FAIL: expected exactly one documented isolated-pin warning for AOUT")
if warnings != sum(rule_counts.values()):
    failed = True
    print("FAIL: ERC warning severity count does not match rule count")
if footprint_refs != allowed_footprint_refs:
    failed = True
    print("FAIL: footprint_filter warning references differ from the documented 17 unresolved packages")
    print(f"  Missing expected: {sorted(allowed_footprint_refs - footprint_refs)}")
    print(f"  Unexpected: {sorted(footprint_refs - allowed_footprint_refs)}")

if failed:
    if unexpected:
        print("UNRESOLVED ERC RULES:")
        for rule, count in sorted(unexpected.items()):
            print(f"  {rule}: {count}")
    raise SystemExit("FAIL: ERC contains errors or warnings beyond the documented AOUT/footprint items")

print("PASS: no electrical, grid, dangling-wire, local/global-label, or library-mismatch warnings")
print("NOTE: footprint_filter warnings remain until physical packages are selected")
print("NOTE: isolated_pin_label on AOUT is intentional and remains a separate measurement net")
