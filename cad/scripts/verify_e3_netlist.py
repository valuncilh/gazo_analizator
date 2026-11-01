#!/usr/bin/env python3
"""Verify a KiCad XML netlist against the frozen approved E3 topology."""
from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

EXPECTED_COMPONENTS = {
    "A1", "C1", "C2", "C3", "DA1", "HA1", "HL1", "HL2",
    "R1", "R2", "R3", "R4", "R5", "R6", "R7", "SA1", "VD1", "VT1", "XS1",
}
EXPECTED_NETS: dict[str, set[tuple[str, str]]] = {
    "/AOUT": {("A1", "3")},
    "/VCC": {
        ("A1", "1"), ("C3", "1"), ("DA1", "8"), ("HL2", "2"),
        ("R1", "1"), ("R3", "2"), ("R4", "2"), ("XS1", "1"),
    },
    "Earth": {
        ("A1", "4"), ("C1", "2"), ("C2", "2"), ("DA1", "1"),
        ("HL1", "1"), ("VT1", "3"), ("XS1", "2"),
    },
    "Net-(A1-Pin_2)": {("A1", "2"), ("R1", "2"), ("R2", "1")},
    "Net-(DA1-CONT)": {("C2", "1"), ("DA1", "5")},
    "Net-(DA1-DISCH)": {("DA1", "7"), ("R4", "1"), ("R5", "1")},
    "Net-(DA1-OUT)": {("DA1", "3"), ("R6", "1"), ("VD1", "2")},
    "Net-(DA1-THRES)": {("C1", "1"), ("DA1", "2"), ("DA1", "6"), ("R5", "2")},
    "Net-(DA1-~{RST})": {("DA1", "4"), ("R3", "1"), ("VT1", "2")},
    "Net-(HA1-Pin_1)": {("HA1", "1"), ("VD1", "1")},
    "Net-(HA1-Pin_2)": {("HA1", "2"), ("R7", "1"), ("SA1", "1")},
    "Net-(HL1-A)": {("HL1", "2"), ("R6", "2")},
    "Net-(HL2-K)": {("HL2", "1"), ("R7", "2")},
    "Net-(SA1-B)": {("C3", "2"), ("SA1", "2")},
    "Net-(VT1-B)": {("R2", "2"), ("VT1", "1")},
}
EXPECTED_PIN_COUNT = 47


def load_netlist(path: Path) -> tuple[set[str], dict[str, set[tuple[str, str]]]]:
    root = ET.parse(path).getroot()
    components_node = root.find("components")
    nets_node = root.find("nets")
    if components_node is None or nets_node is None:
        raise ValueError("XML must contain <components> and <nets>")
    refs = {node.get("ref", "") for node in components_node.findall("comp")}
    nets: dict[str, set[tuple[str, str]]] = {}
    for net in nets_node.findall("net"):
        name = net.get("name", "")
        if name in nets:
            raise ValueError(f"duplicate net: {name}")
        nets[name] = {
            (node.get("ref", ""), node.get("pin", ""))
            for node in net.findall("node")
        }
    return refs, nets


def validate(refs: set[str], nets: dict[str, set[tuple[str, str]]]) -> list[str]:
    errors: list[str] = []
    if refs != EXPECTED_COMPONENTS:
        errors.append(
            f"component refs mismatch: missing={sorted(EXPECTED_COMPONENTS - refs)}, "
            f"unexpected={sorted(refs - EXPECTED_COMPONENTS)}"
        )
    if set(nets) != set(EXPECTED_NETS):
        errors.append(
            f"net names mismatch: missing={sorted(set(EXPECTED_NETS) - set(nets))}, "
            f"unexpected={sorted(set(nets) - set(EXPECTED_NETS))}"
        )
    for name, expected in EXPECTED_NETS.items():
        actual = nets.get(name)
        if actual is not None and actual != expected:
            errors.append(
                f"{name}: missing={sorted(expected - actual)}, "
                f"unexpected={sorted(actual - expected)}"
            )

    all_nodes = [node for values in nets.values() for node in values]
    duplicates = sorted(node for node, count in Counter(all_nodes).items() if count != 1)
    if duplicates:
        errors.append(f"pins assigned more than once: {duplicates}")
    if len(all_nodes) != EXPECTED_PIN_COUNT:
        errors.append(f"expected {EXPECTED_PIN_COUNT} pin nodes, got {len(all_nodes)}")
    if nets.get("/AOUT") != {("A1", "3")}:
        errors.append("A1.3 must remain the separate /AOUT measurement net")
    if nets.get("Net-(SA1-B)") != {("C3", "2"), ("SA1", "2")}:
        errors.append("C3.2 and SA1.2 must remain the isolated Net-(SA1-B)")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "netlist",
        nargs="?",
        type=Path,
        default=Path(
            "cad/project_modification/gost_e3_final/reports/kicad10/netlist_current.xml"
        ),
    )
    args = parser.parse_args()
    if not args.netlist.is_file():
        print(f"ERROR: netlist not found: {args.netlist}", file=sys.stderr)
        return 2
    try:
        refs, nets = load_netlist(args.netlist)
    except (ET.ParseError, OSError, ValueError) as exc:
        print(f"ERROR: cannot parse netlist: {exc}", file=sys.stderr)
        return 2
    errors = validate(refs, nets)
    if errors:
        print("FAIL: XML-netlist does not match the frozen E3 topology")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: 19 components, 15 nets and 47 pin nodes match the frozen E3 reference.")
    print("PASS: A1.3 remains /AOUT; C3.2/SA1.2 remains isolated.")
    print("NOTE: netlist parity does not prove footprint correctness, copper continuity or DRC.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
