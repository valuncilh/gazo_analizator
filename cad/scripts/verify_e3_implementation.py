#!/usr/bin/env python3
"""Verify the isolated E3 implementation copy against the immutable approved baseline.

This is a source-level consistency check. It does not replace KiCad 10 ERC,
netlist export, footprint library checks, PCB DRC, 3D inspection or physical fit.
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "cad" / "kicad" / "e3_project"
IMPLEMENTATION = PROJECT / "gazo_e3_implementation.kicad_sch"
FP_TABLE = PROJECT / "fp-lib-table"
PAD_MAP = PROJECT / "reports" / "e3_pad_net_map.csv"
STATUS_CSV = PROJECT / "reports" / "footprint_assignment_status.csv"

APPROVED_SCHEMATIC = (
    ROOT / "cad" / "project_modification" / "gost_e3_final"
    / "gazo_analizator_E3_GOST_itog.kicad_sch"
)
APPROVED_NETLIST = (
    ROOT / "cad" / "project_modification" / "gost_e3_final"
    / "reports" / "kicad10" / "netlist_current.xml"
)
EXPECTED_SCHEMATIC_BLOB = "2e17299ba8a9aeeb0ce5e6c06562fe4e0fd84ba0"
EXPECTED_NETLIST_BLOB = "b24384b2e1b39068b3a11c9e11554cd4dc406b57"

EXPECTED_FOOTPRINTS = {
    "A1": "Connector_Molex:Molex_PicoBlade_53261-0471_1x04-1MP_P1.25mm_Horizontal",
    "C1": "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm",
    "C2": "Capacitor_SMD:C_0805_2012Metric",
    "C3": "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm",
    "DA1": "Package_DIP:DIP-8_W7.62mm",
    "HA1": "GazoE3:HCM1206X_P7.6mm",
    "HL1": "LED_THT:LED_D5.0mm",
    "HL2": "LED_THT:LED_D5.0mm",
    "R1": "Resistor_SMD:R_0805_2012Metric",
    "R2": "Resistor_SMD:R_0805_2012Metric",
    "R3": "Resistor_SMD:R_0805_2012Metric",
    "R4": "Resistor_SMD:R_0805_2012Metric",
    "R5": "Resistor_SMD:R_0805_2012Metric",
    "R6": "Resistor_SMD:R_0805_2012Metric",
    "R7": "Resistor_SMD:R_0805_2012Metric",
    "SA1": "GazoE3:NKK_AS11AP_SPST_P5.08mm",
    "VD1": "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal",
    "VT1": "GazoE3:KT3102B_KT1-7_DWG_DRAFT",
    "XS1": "Connector_Molex:Molex_PicoBlade_53261-0271_1x02-1MP_P1.25mm_Horizontal",
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def extract_sexpr(text: str, start: int) -> str:
    depth = 0
    quoted = False
    escaped = False
    for pos in range(start, len(text)):
        char = text[pos]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : pos + 1]
            if depth < 0:
                raise ValueError(f"Unexpected closing parenthesis at offset {pos}")
    raise ValueError(f"Unclosed S-expression starting at offset {start}")


def get_symbol_instances(text: str) -> dict[str, dict[str, str]]:
    instances: dict[str, dict[str, str]] = {}
    cursor = 0
    while True:
        start = text.find("(symbol", cursor)
        if start < 0:
            break
        block = extract_sexpr(text, start)
        cursor = start + len(block)
        if '(lib_id "' not in block:
            continue
        ref_match = re.search(r'\\(property "Reference" "([^"]+)"', block)
        if not ref_match:
            continue
        ref = ref_match.group(1)
        fp_match = re.search(r'\\(property "Footprint" "([^"]*)"', block)
        lib_match = re.search(r'\\(lib_id "([^"]+)"', block)
        if ref in instances:
            raise ValueError(f"Duplicate symbol reference: {ref}")
        instances[ref] = {
            "footprint": fp_match.group(1) if fp_match else "",
            "lib_id": lib_match.group(1) if lib_match else "",
        }
    return instances


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def main() -> int:
    errors: list[str] = []
    required = [
        IMPLEMENTATION,
        FP_TABLE,
        PAD_MAP,
        STATUS_CSV,
        APPROVED_SCHEMATIC,
        APPROVED_NETLIST,
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")
    if errors:
        print("\\n".join(errors), file=sys.stderr)
        return 1

    schematic_sha = git_blob_sha(APPROVED_SCHEMATIC)
    netlist_sha = git_blob_sha(APPROVED_NETLIST)
    if schematic_sha != EXPECTED_SCHEMATIC_BLOB:
        errors.append(
            f"Approved E3 schematic changed: expected {EXPECTED_SCHEMATIC_BLOB}, got {schematic_sha}"
        )
    if netlist_sha != EXPECTED_NETLIST_BLOB:
        errors.append(
            f"Approved XML-netlist changed: expected {EXPECTED_NETLIST_BLOB}, got {netlist_sha}"
        )

    implementation_text = IMPLEMENTATION.read_text(encoding="utf-8")
    instances = get_symbol_instances(implementation_text)
    expected_refs = set(EXPECTED_FOOTPRINTS)
    actual_refs = set(instances)
    if actual_refs != expected_refs:
        errors.append(
            "Implementation ref mismatch: "
            f"missing={sorted(expected_refs - actual_refs)}, "
            f"unexpected={sorted(actual_refs - expected_refs)}"
        )
    for ref, expected_fp in EXPECTED_FOOTPRINTS.items():
        actual_fp = instances.get(ref, {}).get("footprint", "")
        if actual_fp != expected_fp:
            errors.append(f"{ref}: expected footprint {expected_fp!r}, got {actual_fp!r}")

    fp_table = FP_TABLE.read_text(encoding="utf-8")
    if '${KIPRJMOD}/../footprints/GazoE3.pretty' not in fp_table:
        errors.append("Project-local GazoE3 library URI is incorrect.")

    pad_rows = load_csv(PAD_MAP)
    if len(pad_rows) != 47:
        errors.append(f"Expected 47 pad-to-net rows, got {len(pad_rows)}")
    refs_in_map = {row["Ref"] for row in pad_rows}
    if refs_in_map != expected_refs:
        errors.append(
            "Pad-map reference mismatch: "
            f"missing={sorted(expected_refs - refs_in_map)}, "
            f"unexpected={sorted(refs_in_map - expected_refs)}"
        )
    for row in pad_rows:
        ref = row["Ref"]
        if ref in EXPECTED_FOOTPRINTS and row["Footprint"] != EXPECTED_FOOTPRINTS[ref]:
            errors.append(
                f"Pad-map footprint mismatch for {ref} pin {row['SymbolPin']}: "
                f"{row['Footprint']!r}"
            )

    by_pin_net = {(row["Ref"], row["SymbolPin"]): row["Net"] for row in pad_rows}
    protected = {
        ("A1", "3"): "/AOUT",
        ("C3", "2"): "Net-(SA1-B)",
        ("SA1", "2"): "Net-(SA1-B)",
        ("VT1", "1"): "Net-(VT1-B)",
        ("VT1", "2"): "Net-(DA1-~{RST})",
        ("VT1", "3"): "Earth",
        ("VD1", "1"): "Net-(HA1-Pin_1)",
        ("VD1", "2"): "Net-(DA1-OUT)",
    }
    for key, expected_net in protected.items():
        if by_pin_net.get(key) != expected_net:
            errors.append(
                f"Protected net changed at {key[0]}.{key[1]}: "
                f"expected {expected_net!r}, got {by_pin_net.get(key)!r}"
            )

    status_rows = load_csv(STATUS_CSV)
    status_refs = {row["Ref"] for row in status_rows}
    if status_refs != expected_refs or len(status_rows) != 19:
        errors.append(
            "Footprint status register must contain exactly the 19 E3 references."
        )

    if errors:
        print("FAIL: E3 implementation source checks")
        print("\\n".join(f"- {item}" for item in errors), file=sys.stderr)
        return 1

    print("PASS: immutable approved E3 schematic and XML-netlist blob IDs.")
    print("PASS: implementation copy contains exactly 19 E3 refs with expected footprint assignments.")
    print("PASS: project-local GazoE3 library path is relative and resolvable from e3_project.")
    print("PASS: 47 pad-to-net rows cover the 19 E3 refs.")
    print("PASS: /AOUT, Net-(SA1-B), VT1 pin map and VD1 pad map remain unchanged.")
    print("PASS: footprint assignment status register contains 19 refs.")
    print("NOTE: source-level only. KiCad 10 ERC, fresh XML export, footprint checks and PCB DRC remain pending.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
