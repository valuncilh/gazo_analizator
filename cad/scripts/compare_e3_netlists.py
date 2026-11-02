#!/usr/bin/env python3
"""Compare a fresh E3 implementation XML-netlist with the immutable approved E3.

This checks component references/values and the complete logical net topology.
It does not validate footprints, pad geometry, copper routing or physical fit.
"""
from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE = (
    ROOT
    / "cad/project_modification/gost_e3_final/reports/kicad10/netlist_current.xml"
)

FORBIDDEN_REFS = {"U2", "P1", "RHYS", "VT2", "R8", "R9"}
PROTECTED_NETS = {
    "/AOUT": {("A1", "3")},
    "Net-(SA1-B)": {("C3", "2"), ("SA1", "2")},
}
EXPECTED_COUNTS = {"components": 19, "nets": 15, "pins": 47}


def load_netlist(path: Path) -> tuple[dict[str, str], dict[str, set[tuple[str, str]]], dict[str, str]]:
    root = ET.parse(path).getroot()
    if root.tag != "export":
        raise ValueError(f"{path}: root tag is {root.tag!r}, expected 'export'")

    components: dict[str, str] = {}
    footprints: dict[str, str] = {}
    for comp in root.findall("./components/comp"):
        ref = comp.get("ref")
        if not ref:
            raise ValueError(f"{path}: component without ref")
        if ref in components:
            raise ValueError(f"{path}: duplicate component ref {ref}")
        components[ref] = comp.findtext("value", default="").strip()
        fields = {
            field.get("name", ""): (field.text or "").strip()
            for field in comp.findall("./fields/field")
        }
        footprints[ref] = fields.get("Footprint", "")

    nets: dict[str, set[tuple[str, str]]] = {}
    for net in root.findall("./nets/net"):
        name = net.get("name")
        if not name:
            raise ValueError(f"{path}: net without name")
        if name in nets:
            raise ValueError(f"{path}: duplicate net {name}")
        nodes: set[tuple[str, str]] = set()
        for node in net.findall("./node"):
            ref, pin = node.get("ref"), node.get("pin")
            if not ref or not pin:
                raise ValueError(f"{path}: malformed node in net {name}")
            nodes.add((ref, pin))
        nets[name] = nodes

    return components, nets, footprints


def compare_maps(label: str, expected: dict, actual: dict) -> list[str]:
    errors: list[str] = []
    if set(expected) != set(actual):
        errors.append(
            f"{label} keys differ: missing={sorted(set(expected) - set(actual))}, "
            f"unexpected={sorted(set(actual) - set(expected))}"
        )
        return errors
    for key in sorted(expected):
        if expected[key] != actual[key]:
            errors.append(
                f"{label} mismatch at {key}: expected={expected[key]!r}, "
                f"actual={actual[key]!r}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare implementation XML-netlist to approved E3 topology."
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=DEFAULT_BASELINE,
        help="Approved E3 XML-netlist. Defaults to the committed immutable baseline.",
    )
    parser.add_argument(
        "--candidate",
        type=Path,
        required=True,
        help="Fresh XML-netlist exported from gazo_e3_implementation.kicad_sch.",
    )
    parser.add_argument(
        "--require-footprints",
        action="store_true",
        help="Also require a non-empty Footprint field for all 19 implementation components.",
    )
    args = parser.parse_args()

    for path in (args.baseline, args.candidate):
        if not path.is_file():
            print(f"ERROR: missing netlist: {path}", file=sys.stderr)
            return 2

    try:
        base_components, base_nets, _ = load_netlist(args.baseline)
        cand_components, cand_nets, cand_footprints = load_netlist(args.candidate)
    except (ET.ParseError, OSError, ValueError) as exc:
        print(f"ERROR: cannot parse XML-netlist: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    errors += compare_maps("component values", base_components, cand_components)
    errors += compare_maps("net topology", base_nets, cand_nets)

    pin_count = sum(len(nodes) for nodes in cand_nets.values())
    counts = {
        "components": len(cand_components),
        "nets": len(cand_nets),
        "pins": pin_count,
    }
    if counts != EXPECTED_COUNTS:
        errors.append(f"count mismatch: expected={EXPECTED_COUNTS}, actual={counts}")

    forbidden = FORBIDDEN_REFS & set(cand_components)
    if forbidden:
        errors.append(f"forbidden legacy references present: {sorted(forbidden)}")

    for net_name, expected_nodes in PROTECTED_NETS.items():
        actual_nodes = cand_nets.get(net_name)
        if actual_nodes != expected_nodes:
            errors.append(
                f"protected net {net_name}: expected={sorted(expected_nodes)}, "
                f"actual={sorted(actual_nodes or set())}"
            )

    if args.require_footprints:
        empty = sorted(ref for ref, footprint in cand_footprints.items() if not footprint)
        if empty:
            errors.append(f"missing Footprint fields for: {empty}")

    if errors:
        print("FAIL: implementation XML-netlist does not match approved E3.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("PASS: component references and values match approved E3.")
    print("PASS: all 15 nets and 47 connected pins match approved E3.")
    print("PASS: /AOUT remains isolated at A1.3.")
    print("PASS: Net-(SA1-B) remains exactly C3.2 <-> SA1.2.")
    print("PASS: no legacy U2/P1/RHYS/VT2/R8/R9 references.")
    if args.require_footprints:
        print("PASS: all 19 implementation components have non-empty Footprint fields.")
    else:
        print("NOTE: footprint fields were not required by this topology comparison.")
    print("NOTE: this is an XML-netlist comparison, not a footprint geometry check or PCB DRC.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
