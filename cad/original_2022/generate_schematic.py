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
PROJECT = "original_2022"
ROOT_UUID = str(uuid.uuid4())


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
    field_offset = 15 if symbol_id == "Timer:NE555D" else 7.62
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
{property_block("Reference", reference, x, y - field_offset)}
{property_block("Value", value, x, y + field_offset)}
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


# Original gas module interface. The AOUT pin is explicitly left unused.
add("A1", "Connector_Generic:Conn_01x04", "MQ-4 module (model unknown)", 25, 65,
    {"1": "VCC", "2": "DOUT", "3": None, "4": "GND"})
add("R1", "Device:R", "160 kΩ", 57, 42, {"1": "VCC", "2": "DOUT"})
add("R2", "Device:R", "13 kΩ", 77, 65, {"1": "DOUT", "2": "VT1_B"})
add("VT1", "Transistor_BJT:Q_NPN_BCE", "КТ3102Б", 105, 65,
    {"1": "VT1_B", "2": "RESET", "3": "GND"})
add("R3", "Device:R", "2 kΩ", 124, 42, {"1": "VCC", "2": "RESET"})

# Original NE555N astable timer and component values.
add("DA1", "Timer:NE555D", "NE555N", 157, 65,
    {"1": "GND", "2": "CT", "3": "OUT", "4": "RESET",
     "5": "CTRL", "6": "CT", "7": "DISCH", "8": "VCC"},
    datasheet="http://www.ti.com/lit/ds/symlink/ne555.pdf")
add("R4", "Device:R", "8.2 kΩ", 191, 35, {"1": "VCC", "2": "DISCH"})
add("R5", "Device:R", "8.2 kΩ", 215, 55, {"1": "DISCH", "2": "CT"})
add("C1", "Device:C_Polarized", "4.7 µF 16 V", 244, 65,
    {"1": "CT", "2": "GND"})
add("C2", "Device:C", "100 n (as printed)", 158, 105,
    {"1": "CTRL", "2": "GND"})
add("C3", "Device:C_Polarized", "47 µF 16 V", 268, 35,
    {"1": "VCC", "2": "GND"})

# Original direct output stage: no added VT2/R9 driver.
add("R6", "Device:R", "220 Ω", 150, 140, {"1": "OUT", "2": "HL1_A"})
add("HL1", "Device:LED", "Red LED", 177, 140, {"1": "GND", "2": "HL1_A"})
add("VD1", "Device:D", "КД510А", 211, 122, {"1": "HA1_P", "2": "OUT"})
add("HA1", "Connector_Generic:Conn_01x02", "HCM1206X or equivalent", 244, 110,
    {"1": "HA1_P", "2": "HA1_N"})
add("SA1", "Switch:SW_SPST", "Sound enable", 255, 150,
    {"1": "HA1_N", "2": "GND"})
add("HL2", "Device:LED", "Green LED", 208, 150,
    {"1": "HL2_K", "2": "VCC"})
add("R7", "Device:R", "220 Ω", 237, 150,
    {"1": "HA1_N", "2": "HL2_K"})
add("XS1", "Connector_Generic:Conn_01x02", "5 V input", 25, 155,
    {"1": "VCC", "2": "GND"})
add("#FLG01", "power:PWR_FLAG", "PWR_FLAG", 45, 155, {"1": "VCC"})
add("#FLG02", "power:PWR_FLAG", "PWR_FLAG", 45, 165, {"1": "GND"})


TEXTS = [
    '''\t(text "SOURCE TRANSCRIPTION: Kuznetsov, Radio 11/2022, pp. 46–48. A1 internals unknown; AOUT unused."
\t\t(at 38 12 0) (effects (font (size 1.27 1.27))) (uuid "{}"))'''.format(uid()),
    '''\t(text "C2 is marked ‘100 н’ in the reproduced drawing; unit remains unverified."
\t\t(at 38 18 0) (effects (font (size 1.27 1.27))) (uuid "{}"))'''.format(uid()),
    '''\t(text "NE555 estimate: 12.47 Hz from printed values; article states 1–2 Hz. Original values unchanged."
\t\t(at 38 24 0) (effects (font (size 1.27 1.27))) (uuid "{}"))'''.format(uid()),
]


def generate() -> None:
    schematic = f'''(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "{ROOT_UUID}")
\t(paper "A4")
\t(title_block
\t\t(title "Original 2022 — household gas leak alarm")
\t\t(date "2026-10-31")
\t\t(rev "Source transcription")
\t\t(company "Course project reference")
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
        "meta": {"filename": f"{PROJECT}.kicad_pro", "version": 1},
        "schematic": {},
    }
    (ROOT / f"{PROJECT}.kicad_pro").write_text(
        json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    generate()
