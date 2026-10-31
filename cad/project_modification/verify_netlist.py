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
REFERENCE = ROOT / "data" / "project_modification_reference.md"
PIN_RE = re.compile(r"^([A-Za-z#][A-Za-z0-9#]*)\.([0-9]+)$")


def parse_reference(
    path: Path,
) -> tuple[
    Counter[frozenset[str]],
    frozenset[str],
    dict[str, frozenset[str]],
]:
    expected: Counter[frozenset[str]] = Counter()
    expected_nc: set[str] = set()
    in_table = False
    table_rows = 0

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Full netlist reference"):
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
    expected_components: dict[str, frozenset[str]] = {}
    in_components = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Conditional KiCad pin inventory"):
            in_components = True
            continue
        if in_components and line.startswith("## "):
            break
        if not in_components or not line.startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] in {"Reference", "---"}:
            continue
        reference, pin_text = cells
        if reference in expected_components:
            raise ValueError(f"Duplicate component reference in inventory: {reference}")
        pin_numbers = frozenset(number.strip() for number in pin_text.split(","))
        if not pin_numbers or any(not number.isdigit() for number in pin_numbers):
            raise ValueError(f"Malformed pin inventory for {reference}: {pin_text!r}")
        expected_components[reference] = pin_numbers

    if len(expected_components) != 19:
        raise ValueError(
            f"Expected 19 components in inventory, found {len(expected_components)}"
        )
    return expected, frozenset(expected_nc), expected_components


def parse_netlist(
    path: Path,
) -> tuple[
    Counter[frozenset[str]],
    frozenset[str],
    dict[str, frozenset[str]],
]:
    root = ET.parse(path).getroot()
    actual: Counter[frozenset[str]] = Counter()
    actual_nc: set[str] = set()
    seen_pins: set[str] = set()

    # KiCad's component section enumerates every pin belonging to each placed
    # symbol. Require every such pin to occur in exactly one exported net or
    # in the explicit no-connect set below.
    component_pin_map = {
        component.get("ref", ""): frozenset(
            pin.get("num", "")
            for pin in component.findall("./units/unit/pins/pin")
        )
        for component in root.findall("./components/comp")
    }
    if len(component_pin_map) != len(root.findall("./components/comp")):
        raise ValueError("Duplicate or empty component reference in exported netlist")
    component_pins = {
        f"{reference}.{number}"
        for reference, numbers in component_pin_map.items()
        for number in numbers
    }

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

    accounted_pins = seen_pins | actual_nc
    if accounted_pins != component_pins:
        missing = sorted(component_pins - accounted_pins)
        unexpected = sorted(accounted_pins - component_pins)
        raise ValueError(
            "Pin accounting mismatch: "
            f"unaccounted symbol pins={missing}; unexpected pins={unexpected}"
        )

    return actual, frozenset(actual_nc), component_pin_map


def format_members(counter: Counter[frozenset[str]]) -> list[str]:
    return [", ".join(sorted(members)) for members in counter.elements()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("netlist", type=Path, help="KiCad XML netlist exported by kicad-cli")
    parser.add_argument("--reference", type=Path, default=REFERENCE)
    args = parser.parse_args()

    try:
        expected, expected_nc, expected_components = parse_reference(args.reference)
        actual, actual_nc, actual_components = parse_netlist(args.netlist)
    except (OSError, ET.ParseError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    expected_pins = {
        f"{reference}.{number}"
        for reference, numbers in expected_components.items()
        for number in numbers
    }
    component_pins = {
        f"{reference}.{number}"
        for reference, numbers in actual_components.items()
        for number in numbers
    }
    connected_pin_count = sum(len(net) for net in expected.elements())

    if (
        expected != actual
        or expected_nc != actual_nc
        or expected_components != actual_components
        or expected_pins != component_pins
    ):
        print("FAIL: full exported netlist does not match the reference table.")
        print("Expected connected nets:", *format_members(expected), sep="\n  ")
        print("Actual connected nets:", *format_members(actual), sep="\n  ")
        print("Expected NC pins:", ", ".join(sorted(expected_nc)))
        print("Actual NC pins:", ", ".join(sorted(actual_nc)))
        print("Expected component pins:", ", ".join(sorted(expected_pins)))
        print("Actual component pins:", ", ".join(sorted(component_pins)))
        print("Expected component refs:", ", ".join(sorted(expected_components)))
        print("Actual component refs:", ", ".join(sorted(actual_components)))
        return 1

    print(
        "PASS: exact full-netlist match — "
        f"{sum(expected.values())} connected nets, {connected_pin_count} connected pins, "
        f"{len(actual_components)} components and "
        f"{len(component_pins)} total component pins accounted for, "
        f"NC: {', '.join(sorted(expected_nc))}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
