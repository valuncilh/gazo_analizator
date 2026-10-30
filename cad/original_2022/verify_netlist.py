#!/usr/bin/env python3
"""Compare every exported KiCad net against the reference contact table."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "data" / "original_scheme_reference.md"
PIN_RE = re.compile(r"^([A-Za-z#][A-Za-z0-9#]*)\.([0-9]+)$")


def parse_reference(path: Path) -> tuple[Counter[frozenset[str]], frozenset[str]]:
    expected: Counter[frozenset[str]] = Counter()
    expected_nc: set[str] = set()
    in_table = False
    table_rows = 0

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Контрольная таблица KiCad netlist"):
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] in {"Сеть", "---"}:
            continue
        net_name, members_text = cells
        members: set[str] = set()
        for token in members_text.split(","):
            match = PIN_RE.fullmatch(token.strip())
            if not match:
                raise ValueError(f"Malformed pin reference in reference table: {token!r}")
            members.add(f"{match.group(1)}.{match.group(2)}")
        if not members:
            raise ValueError(f"Empty reference net row: {net_name}")
        table_rows += 1
        if net_name == "NC":
            expected_nc.update(members)
        else:
            expected[frozenset(members)] += 1

    if table_rows != 14:
        raise ValueError(f"Expected 14 reference rows (13 nets + NC), found {table_rows}")
    return expected, frozenset(expected_nc)


def parse_netlist(path: Path) -> tuple[Counter[frozenset[str]], frozenset[str]]:
    root = ET.parse(path).getroot()
    actual: Counter[frozenset[str]] = Counter()
    actual_nc: set[str] = set()
    seen_pins: set[str] = set()

    for net in root.findall("./nets/net"):
        name = net.get("name", "")
        nodes = net.findall("node")
        members = {f"{node.get('ref')}.{node.get('pin')}" for node in nodes}
        if any(member.endswith(".None") for member in members):
            raise ValueError(f"Net {name!r} contains a node without a pin number")
        duplicate_pins = seen_pins.intersection(members)
        if duplicate_pins:
            raise ValueError(f"Pins occur in more than one net: {sorted(duplicate_pins)}")
        seen_pins.update(members)

        if name.startswith("unconnected-") or any(
            "no_connect" in (node.get("pintype") or "") for node in nodes
        ):
            actual_nc.update(members)
        else:
            actual[frozenset(members)] += 1

    return actual, frozenset(actual_nc)


def format_members(counter: Counter[frozenset[str]]) -> list[str]:
    return [", ".join(sorted(members)) for members in counter.elements()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("netlist", type=Path, help="KiCad XML netlist exported by kicad-cli")
    parser.add_argument("--reference", type=Path, default=REFERENCE)
    args = parser.parse_args()

    expected, expected_nc = parse_reference(args.reference)
    actual, actual_nc = parse_netlist(args.netlist)
    connected_pin_count = sum(len(net) for net in expected.elements())

    if expected != actual or expected_nc != actual_nc:
        print("FAIL: full exported netlist does not match the reference table.")
        print("Expected connected nets:", *format_members(expected), sep="\n  ")
        print("Actual connected nets:", *format_members(actual), sep="\n  ")
        print("Expected NC pins:", ", ".join(sorted(expected_nc)))
        print("Actual NC pins:", ", ".join(sorted(actual_nc)))
        return 1

    print(
        "PASS: exact full-netlist match — "
        f"{sum(expected.values())} connected nets, {connected_pin_count} connected pins, "
        f"NC: {', '.join(sorted(expected_nc))}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
