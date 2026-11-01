#!/usr/bin/env python3
"""Audit the approved E3 KiCad XML netlist and export a pad-to-net CSV.

The script intentionally checks an immutable Git blob ID. If the approved XML
changes, update the expected topology only after a separate schematic review.
This is a source/netlist audit, not a KiCad PCB DRC.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NETLIST = ROOT / "cad/project_modification/gost_e3_final/reports/kicad10/netlist_current.xml"
CSV_OUT = NETLIST.parent / "e3_pad_net_map.csv"
EXPECTED_GIT_BLOB_SHA = "b24384b2e1b39068b3a11c9e11554cd4dc406b57"

EXPECTED_COMPONENT_VALUES = {
    "A1": "Датчик метана Joy-IT SEN-MQ4-V2",
    "C1": "47 000 000 пФ, 16 В",
    "C2": "100 000 пФ",
    "C3": "47 000 000 пФ, 16 В",
    "DA1": "NE555N",
    "HA1": "HCM1206X",
    "HL1": "Красный светодиод",
    "HL2": "Зелёный светодиод",
    "R1": "160 кОм",
    "R2": "13 кОм",
    "R3": "2 кОм",
    "R4": "8,2 кОм",
    "R5": "8,2 кОм",
    "R6": "0,22 кОм",
    "R7": "0,22 кОм",
    "SA1": "Включение звукового сигнала",
    "VD1": "КД510А",
    "VT1": "КТ3102Б",
    "XS1": "~",
}

EXPECTED_NETS = {
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

FOOTPRINTS = {
    "A1": ("Connector_Molex:Molex_PicoBlade_53261-0471_1x04-1MP_P1.25mm_Horizontal", "SELECTED / check physical pin 1"),
    "C1": ("Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", "CANDIDATE / verify dimensions and polarity"),
    "C2": ("Capacitor_SMD:C_0805_2012Metric", "CANDIDATE"),
    "C3": ("Capacitor_THT:CP_Radial_D5.0mm_P2.00mm", "CANDIDATE / verify dimensions and polarity"),
    "DA1": ("Package_DIP:DIP-8_W7.62mm", "CANDIDATE / NE555P PDIP-8; check temperature range"),
    "HA1": ("GazoE3:HCM1206X_P7.6mm", "CUSTOM / verify polarity"),
    "HL1": ("LED_THT:LED_D5.0mm", "CANDIDATE / pad 1 = cathode"),
    "HL2": ("LED_THT:LED_D5.0mm", "CANDIDATE / pad 1 = cathode"),
    "R1": ("Resistor_SMD:R_0805_2012Metric", "CANDIDATE"),
    "R2": ("Resistor_SMD:R_0805_2012Metric", "CANDIDATE"),
    "R3": ("Resistor_SMD:R_0805_2012Metric", "CANDIDATE"),
    "R4": ("Resistor_SMD:R_0805_2012Metric", "CANDIDATE"),
    "R5": ("Resistor_SMD:R_0805_2012Metric", "CANDIDATE"),
    "R6": ("Resistor_SMD:R_0805_2012Metric", "CANDIDATE"),
    "R7": ("Resistor_SMD:R_0805_2012Metric", "CANDIDATE"),
    "SA1": ("GazoE3:NKK_AS11AP_SPST_P5.08mm", "CUSTOM / pad 1=terminal 1, pad 2=terminal 3"),
    "VD1": ("Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal", "CANDIDATE / pad 1 = cathode"),
    "VT1": ("", "BLOCKED / measure KT3102B metal-glass leads"),
    "XS1": ("Connector_Molex:Molex_PicoBlade_53261-0271_1x02-1MP_P1.25mm_Horizontal", "SELECTED / check cable polarity"),
}

NOTES = {
    "A1": "Joy-IT module is external to main PCB. Symbol pins: 1=VCC, 2=DOUT, 3=AOUT, 4=GND. Verify the Molex pin-1 orientation on the physical module.",
    "DA1": "NE555P PDIP-8 candidate. Approved schematic symbol is NE555D SOIC-8; the pin numbering is retained, but verify package pinout.",
    "HA1": "HA1.1 is connected to VD1 cathode and must correspond to the positive buzzer lead for the approved output polarity. Check the golden + mark on the sample.",
    "SA1": "NKK AS11AP SPST uses physical terminals 1 and 3. Footprint pad 1 maps terminal 1; pad 2 maps terminal 3.",
    "VT1": "Approved symbol pin 1=B, pin 2=C, pin 3=E. Do not infer the KT1-7 lead coordinates from a TO-92 footprint.",
}


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def parse_netlist(path: Path) -> tuple[dict[str, str], dict[str, set[tuple[str, str]]]]:
    root = ET.parse(path).getroot()
    components: dict[str, str] = {}
    nets: dict[str, set[tuple[str, str]]] = {}
    for comp in root.findall("./components/comp"):
        ref = comp.attrib["ref"]
        value = comp.findtext("value", default="")
        components[ref] = value
    for net in root.findall("./nets/net"):
        name = net.attrib["name"]
        nodes = {
            (node.attrib["ref"], node.attrib["pin"])
            for node in net.findall("./node")
        }
        nets[name] = nodes
    return components, nets


def compare(expected: dict, actual: dict, title: str) -> list[str]:
    errors: list[str] = []
    if set(expected) != set(actual):
        errors.append(
            f"{title} keys mismatch: missing={sorted(set(expected)-set(actual))}, "
            f"unexpected={sorted(set(actual)-set(expected))}"
        )
        return errors
    for key in sorted(expected):
        if expected[key] != actual[key]:
            errors.append(
                f"{title} mismatch at {key}: expected={expected[key]}, actual={actual[key]}"
            )
    return errors


def write_csv(path: Path, nets: dict[str, set[tuple[str, str]]]) -> int:
    rows = []
    for net, nodes in nets.items():
        for ref, pin in nodes:
            footprint, status = FOOTPRINTS.get(ref, ("", "UNRESOLVED"))
            rows.append({
                "Ref": ref,
                "SymbolPin": pin,
                "Net": net,
                "Footprint": footprint,
                "FootprintStatus": status,
                "PhysicalNote": NOTES.get(ref, ""),
            })
    rows.sort(key=lambda item: (item["Ref"], int(item["SymbolPin"])))
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["Ref", "SymbolPin", "Net", "Footprint", "FootprintStatus", "PhysicalNote"],
        )
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-csv", action="store_true", help="write e3_pad_net_map.csv")
    args = parser.parse_args()

    if not NETLIST.is_file():
        print(f"ERROR: missing approved netlist: {NETLIST}", file=sys.stderr)
        return 2

    data = NETLIST.read_bytes()
    actual_sha = git_blob_sha(data)
    if actual_sha != EXPECTED_GIT_BLOB_SHA:
        print(
            f"ERROR: approved XML blob changed. expected={EXPECTED_GIT_BLOB_SHA}, actual={actual_sha}. "
            "Review the schematic/netlist before updating this audit.",
            file=sys.stderr,
        )
        return 2

    try:
        components, nets = parse_netlist(NETLIST)
    except (ET.ParseError, KeyError) as exc:
        print(f"ERROR: cannot parse netlist: {exc}", file=sys.stderr)
        return 2

    errors = compare(EXPECTED_COMPONENT_VALUES, components, "Component")
    errors += compare(EXPECTED_NETS, nets, "Net")
    forbidden_refs = {"U2", "P1", "RHYS", "VT2", "R8", "R9"}
    present_forbidden = forbidden_refs & set(components)
    if present_forbidden:
        errors.append(f"Alternative-branch references found in approved E3: {sorted(present_forbidden)}")

    node_count = sum(len(nodes) for nodes in nets.values())
    if len(components) != 19 or len(nets) != 15 or node_count != 47:
        errors.append(
            f"Count mismatch: components={len(components)}, nets={len(nets)}, pins={node_count}; "
            "expected 19 / 15 / 47"
        )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"PASS: approved E3 netlist blob {actual_sha}")
    print(f"PASS: {len(components)} components, {len(nets)} nets, {node_count} connected symbol pins.")
    print("PASS: /AOUT remains a single A1.3 pad; Net-(SA1-B) remains isolated from Earth.")
    print("PASS: no U2/P1/RHYS/VT2/R8/R9 alternative-branch components.")
    if args.write_csv:
        count = write_csv(CSV_OUT, nets)
        print(f"WROTE: {CSV_OUT} ({count} pad-to-net rows).")
    else:
        print("Use --write-csv to export the pad-to-net map.")
    print("NOTE: not a KiCad footprint check, PCB DRC, or physical assembly approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
