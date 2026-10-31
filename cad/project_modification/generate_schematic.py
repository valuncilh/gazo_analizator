#!/usr/bin/env python3
"""Generate the source-only KiCad schematic from the published 2022 diagram.

The output embeds the KiCad library symbols so the schematic remains portable.
No PCB is generated: the source board model and physical footprints are unknown.
"""

from __future__ import annotations

import json
import math
import re
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parent
KICAD_SYMBOLS = Path("/usr/share/kicad/symbols")
PROJECT = "project_modification"
ROOT_UUID = str(uuid.uuid4())
WIRED_NETS = {
    "DOUT", "VT1_B", "RESET", "DISCH", "CT", "CTRL", "OUT",
    "HL1_A", "HA1_P", "HA1_N", "HL2_K",
}
PIN_POINTS: dict[tuple[str, str], tuple[float, float]] = {}


def uid() -> str:
    return str(uuid.uuid4())


def balanced_block(source: str, start: int) -> tuple[str, int]:
    """Return one balanced S-expression, respecting quoted strings."""
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
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
                return source[start : index + 1], index + 1
    raise ValueError("Unbalanced S-expression")


def symbol_definition(lib: str, name: str) -> str:
    source = (KICAD_SYMBOLS / f"{lib}.kicad_sym").read_text(encoding="utf-8")
    marker = f'(symbol "{name}"'
    start = source.find(marker)
    if start < 0:
        raise FileNotFoundError(f"KiCad symbol {lib}:{name} not found")
    block, _ = balanced_block(source, start)
    return re.sub(
        r'^\(symbol\s+"[^"]+"',
        f'(symbol "{lib}:{name}"',
        block,
        count=1,
    )


SYMBOL_IDS = [
    "Connector_Generic:Conn_01x04",
    "Connector_Generic:Conn_01x02",
    "Device:R",
    "Device:C",
    "Device:C_Polarized",
    "Device:LED",
    "Device:D",
    "Transistor_BJT:Q_NPN_BCE",
    "Timer:NE555D",
    "Switch:SW_SPST",
    "power:PWR_FLAG",
]

LIB_SYMBOLS = "\n".join(
    symbol_definition(*symbol_id.split(":", 1)) for symbol_id in SYMBOL_IDS
)


def pin_blocks(symbol_id: str) -> dict[str, tuple[float, float, str]]:
    lib, name = symbol_id.split(":", 1)
    source = (KICAD_SYMBOLS / f"{lib}.kicad_sym").read_text(encoding="utf-8")
    marker = f'(symbol "{name}"'
    start = source.find(marker)
    root, _ = balanced_block(source, start)
    found: dict[str, tuple[float, float, str]] = {}
    cursor = 0
    while True:
        pin_start = root.find("(pin ", cursor)
        if pin_start < 0:
            break
        block, cursor = balanced_block(root, pin_start)
        number = re.search(r'\(number\s+"([^"]+)"', block)
        pin_name = re.search(r'\(name\s+"([^"]*)"', block)
        at = re.search(r"\(at\s+([-+0-9.]+)\s+([-+0-9.]+)\s+([-+0-9.]+)\)", block)
        if number and at:
            found[number.group(1)] = (
                float(at.group(1)),
                float(at.group(2)),
                pin_name.group(1) if pin_name else "",
            )
    return found


def fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def property_block(name: str, value: str, x: float, y: float, hide: bool = False) -> str:
    hidden = "\n\t\t\t(hide yes)" if hide else ""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'''\t\t(property "{name}" "{escaped}"
\t\t\t(at {fmt(x)} {fmt(y)} 0)
\t\t\t(effects (font (size 1.27 1.27)){hidden})
\t\t)'''


def wire(x1: float, y1: float, x2: float, y2: float) -> str:
    return f'''\t(wire
\t\t(pts (xy {fmt(x1)} {fmt(y1)}) (xy {fmt(x2)} {fmt(y2)}))
\t\t(stroke (width 0) (type solid))
\t\t(uuid "{uid()}")
\t)'''


def label(name: str, x: float, y: float, angle: int) -> str:
    justify = "right bottom" if angle == 180 else "left bottom"
    escaped = name.replace("\\", "\\\\").replace('"', '\\"')
    return f'''\t(label "{escaped}"
\t\t(at {fmt(x)} {fmt(y)} {angle})
\t\t(effects (font (size 1.27 1.27)) (justify {justify}))
\t\t(uuid "{uid()}")
\t)'''


def no_connect(x: float, y: float) -> str:
    return f'''\t(no_connect (at {fmt(x)} {fmt(y)}) (uuid "{uid()}"))'''


def placement(
    reference: str,
    symbol_id: str,
    value: str,
    x: float,
    y: float,
    pin_nets: dict[str, str | None],
    angle: int = 0,
    footprint: str = "",
    datasheet: str = "~",
    reference_position: tuple[float, float] | None = None,
    value_position: tuple[float, float] | None = None,
) -> list[str]:
    # KiCad's default electrical grid is 50 mil (1.27 mm). Keep symbol origins
    # on that grid so all library pin and wire endpoints land exactly on-grid.
    x = round(x / 1.27) * 1.27
    y = round(y / 1.27) * 1.27
    pins = pin_blocks(symbol_id)
    missing = set(pin_nets) - set(pins)
    if missing:
        raise ValueError(f"{reference}: missing pins {sorted(missing)} in {symbol_id}")
    instance_id = uid()
    lines: list[str] = []

    # Keep field text outside symbols; large IC fields get wider separation.
    field_offset = 7.62
    if reference_position is None:
        reference_position = (x, y - field_offset)
    if value_position is None:
        value_position = (x, y + field_offset)
    lines.append(
        f'''\t(symbol
\t\t(lib_id "{symbol_id}")
\t\t(at {fmt(x)} {fmt(y)} {angle})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{instance_id}")
{property_block("Reference", reference, *reference_position)}
{property_block("Value", value, *value_position)}
{property_block("Footprint", footprint, x, y, hide=True)}
{property_block("Datasheet", datasheet, x, y, hide=True)}'''
    )
    for pin_number in sorted(pins, key=lambda item: (not item.isdigit(), int(item) if item.isdigit() else item)):
        lines.append(
            f'''\t\t(pin "{pin_number}" (uuid "{uid()}"))'''
        )
    lines.append(
        f'''\t\t(instances
\t\t\t(project "{PROJECT}"
\t\t\t\t(path "/{ROOT_UUID}" (reference "{reference}") (unit 1))
\t\t\t)
\t\t)
\t)'''
    )

    radians = math.radians(angle)
    for pin_number, net_name in pin_nets.items():
        px, py, _ = pins[pin_number]
        gx = x + px * math.cos(radians) - py * math.sin(radians)
        gy = y - (px * math.sin(radians) + py * math.cos(radians))
        if net_name is None:
            lines.append(no_connect(gx, gy))
            continue
        if net_name in WIRED_NETS:
            PIN_POINTS[(reference, pin_number)] = (gx, gy)
            continue
        # A short wire stub plus a local label makes each connection visible and
        # keeps this transcription independent of guessed internal A1 circuitry.
        if abs(px) > abs(py):
            dx = 5.08 if px > 0 else -5.08
            dy = 0.0
        else:
            dx = 0.0
            dy = 5.08 if py > 0 else -5.08
        # Rotate the outward direction with the symbol.
        odx = dx * math.cos(radians) - dy * math.sin(radians)
        ody = -(dx * math.sin(radians) + dy * math.cos(radians))
        ex, ey = gx + odx, gy + ody
        lines.append(wire(gx, gy, ex, ey))
        label_angle = 180 if odx < 0 else 0
        lines.append(label(net_name, ex, ey, label_angle))
    return lines


OBJECTS: list[str] = []


def add(*args, **kwargs) -> None:
    OBJECTS.extend(placement(*args, **kwargs))


# Arrange the signal path from the sensor through RESET, timer, then indicators.
# A1 is provisional Joy-IT SEN-MQ4 V1. Connector pin numbers are abstract only.
add("A1", "Connector_Generic:Conn_01x04", "Joy-IT SEN-MQ4 V1 (provisional)", 34, 67.38,
    {"1": "VCC", "2": "DOUT", "3": None, "4": "GND"},
    reference_position=(34, 57), value_position=(39, 82))
add("R1", "Device:R", "160 kΩ", 55, 63.57, {"1": "VCC", "2": "DOUT"})
add("R2", "Device:R", "13 kΩ", 85, 71.19, {"1": "DOUT", "2": "VT1_B"})
add("VT1", "Transistor_BJT:Q_NPN_BCE", "КТ3102Б", 108, 75,
    {"1": "VT1_B", "2": "RESET", "3": "GND"})
add("R3", "Device:R", "2 kΩ", 125, 66.11, {"1": "VCC", "2": "RESET"})

# Project timer modification: 47 uF targets about 1.25 Hz with R4=R5=8.2 kOhm.
add("DA1", "Timer:NE555D", "NE555N", 140, 75,
    {"1": "GND", "2": "CT", "3": "OUT", "4": "RESET",
     "5": "CTRL", "6": "CT", "7": "DISCH", "8": "VCC"},
    datasheet="http://www.ti.com/lit/ds/symlink/ne555.pdf",
    reference_position=(158, 49), value_position=(158, 106))
add("R4", "Device:R", "8.2 kΩ", 185, 68.65, {"1": "VCC", "2": "DISCH"},
    reference_position=(197, 66), value_position=(197, 71))
add("R5", "Device:R", "8.2 kΩ", 185, 76.27, {"1": "DISCH", "2": "CT"},
    reference_position=(197, 74), value_position=(197, 79))
add("C1", "Device:C_Polarized", "47 µF 16 V", 207, 83.89,
    {"1": "CT", "2": "GND"},
    reference_position=(207, 76), value_position=(203, 110))
add("C2", "Device:C", "100 n (as printed)", 140, 50.8,
    {"1": "CTRL", "2": "GND"}, angle=180,
    reference_position=(121, 47), value_position=(121, 55))
# Keep the supply capacitor next to the input connector and power flags so
# its role is visually clear instead of leaving it isolated at the sheet edge.
add("C3", "Device:C_Polarized", "47 µF 16 V", 71, 111,
    {"1": "VCC", "2": "GND"},
    reference_position=(71, 96), value_position=(84, 115))

# Original direct output stage: no added VT2/R9 driver.
add("R6", "Device:R", "220 Ω", 162, 75,
    {"1": "OUT", "2": "HL1_A"}, angle=90)
add("HL1", "Device:LED", "Red LED", 174, 75,
    {"1": "GND", "2": "HL1_A"}, angle=180)
add("VD1", "Device:D", "КД510А", 184, 100, {"1": "HA1_P", "2": "OUT"},
    reference_position=(180, 105), value_position=(180, 112))
add("HA1", "Connector_Generic:Conn_01x02", "HCM1206X or equivalent", 220, 100,
    {"1": "HA1_P", "2": "HA1_N"}, value_position=(239, 116))
add("SA1", "Switch:SW_SPST", "Sound enable", 235, 102.54,
    {"1": "HA1_N", "2": "GND"})
add("HL2", "Device:LED", "Green LED", 185, 130,
    {"1": "HL2_K", "2": "VCC"})
add("R7", "Device:R", "220 Ω", 165, 130,
    {"1": "HA1_N", "2": "HL2_K"}, angle=90)
add("XS1", "Connector_Generic:Conn_01x02", "5 V input", 34, 137,
    {"1": "VCC", "2": "GND"})
add("#FLG01", "power:PWR_FLAG", "PWR_FLAG", 52, 137, {"1": "VCC"})
add("#FLG02", "power:PWR_FLAG", "PWR_FLAG", 52, 147, {"1": "GND"})


def pin_point(reference: str, number: str) -> tuple[float, float]:
    return PIN_POINTS[(reference, number)]


def route(*points: tuple[float, float]) -> None:
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        if x1 == x2 and y1 == y2:
            continue
        if x1 != x2 and y1 != y2:
            raise ValueError(f"Non-orthogonal wire path: {(x1, y1)} -> {(x2, y2)}")
        OBJECTS.append(wire(x1, y1, x2, y2))


# Explicit source-signal wiring. VCC/GND remain named power labels.
route(pin_point("A1", "2"), pin_point("R1", "2"), pin_point("R2", "1"))
route(pin_point("R2", "2"), pin_point("VT1", "1"))
route(pin_point("VT1", "2"), pin_point("R3", "2"), pin_point("DA1", "4"))
route(pin_point("DA1", "7"), pin_point("R4", "2"))
# R4.2 and R5.1 share the same grid point; no zero-length wire is needed.
route(pin_point("DA1", "6"), pin_point("DA1", "2"),
      pin_point("R5", "2"), pin_point("C1", "1"))
route(pin_point("DA1", "5"), pin_point("C2", "1"))
route(pin_point("DA1", "3"), pin_point("R6", "1"))
route(pin_point("R6", "2"), pin_point("HL1", "2"))
out_x, out_y = pin_point("DA1", "3")
sound_x, sound_y = pin_point("VD1", "2")
route((out_x, out_y), (out_x, sound_y), (sound_x, sound_y))
route(pin_point("VD1", "1"), pin_point("HA1", "1"))
route(pin_point("HA1", "2"), pin_point("SA1", "1"))
ha1_n_x, ha1_n_y = pin_point("HA1", "2")
r7_n_x, r7_n_y = pin_point("R7", "1")
route(pin_point("HA1", "2"), (ha1_n_x, r7_n_y - 5.08),
      (r7_n_x, r7_n_y - 5.08), pin_point("R7", "1"))
route(pin_point("R7", "2"), pin_point("HL2", "1"))


TEXTS = [
    '''\t(text "PROJECT MODIFICATION: target CH4 alarm threshold 1000 ppm; calibration is not verified."
\t\t(at 14 170 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{}"))'''.format(uid()),
    '''\t(text "A1 is provisional Joy-IT SEN-MQ4 V1; pin numbering is abstract and physical pinout unknown."
\t\t(at 14 176 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{}"))'''.format(uid()),
    '''\t(text "Timer estimate: about 1.25 Hz with R4=R5=8.2 kΩ and C1=47 µF; no hardware verification."
\t\t(at 14 182 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{}"))'''.format(uid()),
]


def generate() -> None:
    schematic = f'''(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{ROOT_UUID}")
\t(paper "A4")
\t(title_block
\t\t(title "Project modification — methane gas leak alarm")
\t\t(date "2026-10-31")
\t\t(rev "Preliminary design")
\t\t(company "Course project — separate design")
\t)
\t(lib_symbols
{LIB_SYMBOLS}
\t)
{chr(10).join(OBJECTS)}
{chr(10).join(TEXTS)}
\t(sheet_instances (path "/" (page "1")))
)\n'''
    (ROOT / f"{PROJECT}.kicad_sch").write_text(schematic, encoding="utf-8")
    project = {
        "board": {},
        "erc": {
            "erc_exclusions": [],
            "meta": {"version": 0},
            "rule_severities": {
                "footprint_filter": "warning",
                "four_way_junction": "warning",
                "simulation_model_issue": "error",
                "single_global_label": "warning",
            },
        },
        "meta": {"filename": f"{PROJECT}.kicad_pro", "version": 1},
        "schematic": {},
    }
    (ROOT / f"{PROJECT}.kicad_pro").write_text(
        json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    generate()
