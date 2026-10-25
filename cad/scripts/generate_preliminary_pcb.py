#!/usr/bin/env python3
"""Generate an explicitly preliminary, unrouted KiCad 9 PCB placement draft."""
from pathlib import Path
import math
import re
import uuid

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "cad/kicad/gazo_analizator_preliminary.kicad_pcb"
NS = uuid.UUID("e2afedc9-48ec-45c2-8a88-7d2c3c42e77b")
COUNTER = 0
NETS = ["", "GND", "+5V", "SENSE", "UREF", "DOUT", "RESET", "VT1_BASE",
        "VT2_BASE", "TIMER_CT", "TIMER_DISCH", "TIMER_CTRL", "OUT", "HL1_A", "HL2_A",
        "SOUND_CTL", "SA1_LED_RETURN", "BUZZ_COL"]
NETNO = {name: i for i, name in enumerate(NETS)}

def q(value):
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'

def ident(key):
    global COUNTER
    COUNTER += 1
    return str(uuid.uuid5(NS, f"{key}-{COUNTER}"))

def netexpr(name):
    if not name or name not in NETNO or NETNO[name] == 0:
        return ""
    return f" (net {NETNO[name]} {q(name)})"

def line(x1, y1, x2, y2, layer="F.Fab", key="line", width=0.12):
    return (f'(fp_line (start {x1:g} {y1:g}) (end {x2:g} {y2:g}) '
            f'(stroke (width {width:g}) (type default)) (layer {q(layer)}) '
            f'(uuid {q(ident(key))}))')

def rect(x1, y1, x2, y2, layer="F.Fab", key="rect", width=0.12):
    return [
        line(x1, y1, x2, y1, layer, key, width),
        line(x2, y1, x2, y2, layer, key, width),
        line(x2, y2, x1, y2, layer, key, width),
        line(x1, y2, x1, y1, layer, key, width),
    ]

def circle(radius, layer="F.SilkS", key="circle", width=0.12):
    return (f'(fp_circle (center 0 0) (end {radius:g} 0) '
            f'(stroke (width {width:g}) (type default)) (fill none) '
            f'(layer {q(layer)}) (uuid {q(ident(key))}))')

def pth(number, x, y, net, shape="circle", size=1.8, drill=0.9, padtype="thru_hole"):
    return dict(n=str(number), typ=padtype, shape=shape, x=x, y=y,
                w=size, h=size, drill=drill, layers='"*.Cu" "*.Mask"', net=net)

def smd(number, x, y, net, w=1.0, h=1.2):
    return dict(n=str(number), typ="smd", shape="rect", x=x, y=y,
                w=w, h=h, drill=None, layers='"F.Cu" "F.Paste" "F.Mask"', net=net)

def pad(p):
    result = (f'(pad {q(p["n"])} {p["typ"]} {p["shape"]} '
              f'(at {p["x"]:g} {p["y"]:g}) (size {p["w"]:g} {p["h"]:g})')
    if p["drill"] is not None:
        result += f' (drill {p["drill"]:g})'
    result += f' (layers {p["layers"]}){netexpr(p["net"])})'
    return result

def footprint(lib, ref, value, x, y, pads, lines, *, attr="through_hole",
              ref_y=-2.5, ref_x=0, val_y=2.5, description=""):
    k = "fp-" + ref
    out = [
        f'(footprint {q(lib)} (layer "F.Cu") (uuid {q(str(uuid.uuid5(NS, k)))}) (at {x:g} {y:g} 0)',
        f' (property "Reference" {q(ref)} (at {ref_x:g} {ref_y:g} 0) (layer "F.SilkS") '
        f'(uuid {q(ident("ref-"+ref))}) (effects (font (size 1 1) (thickness 0.15))))',
        f' (property "Value" {q(value)} (at 0 {val_y:g} 0) (layer "F.Fab") '
        f'(uuid {q(ident("val-"+ref))}) (effects (font (size 1 1) (thickness 0.15))))',
    ]
    if description:
        out.append(
            f' (property "Description" {q(description)} (at 0 0 0) (unlocked yes) '
            f'(layer "F.Fab") (hide yes) (uuid {q(ident("desc-"+ref))}) '
            '(effects (font (size 1.27 1.27) (thickness 0.15))))'
        )
    out.append(f' (attr {attr})')
    # Provisional courtyard includes pad extents and package outlines.
    # Geometry remains TBC and must be verified against the selected data sheets.
    ext_x, ext_y = [], []
    for p in pads:
        ext_x.extend([p["x"] - p["w"] / 2, p["x"] + p["w"] / 2])
        ext_y.extend([p["y"] - p["h"] / 2, p["y"] + p["h"] / 2])
    for primitive in lines:
        if "(fp_circle" in primitive:
            center = re.search(r'\(center\s+([-0-9.]+)\s+([-0-9.]+)\)', primitive)
            end = re.search(r'\(end\s+([-0-9.]+)\s+([-0-9.]+)\)', primitive)
            if center and end:
                cx, cy = float(center.group(1)), float(center.group(2))
                radius = math.hypot(float(end.group(1)) - cx, float(end.group(2)) - cy)
                ext_x.extend([cx - radius, cx + radius])
                ext_y.extend([cy - radius, cy + radius])
        else:
            for coord in re.finditer(r'\((?:start|end)\s+([-0-9.]+)\s+([-0-9.]+)\)', primitive):
                ext_x.append(float(coord.group(1)))
                ext_y.append(float(coord.group(2)))
    if ext_x and ext_y:
        margin = 0.25
        out.extend(" " + item for item in rect(
            min(ext_x) - margin, min(ext_y) - margin,
            max(ext_x) + margin, max(ext_y) + margin,
            "F.CrtYd", "courtyard-" + ref, 0.05
        ))
    out.extend(" " + ln for ln in lines)
    out.extend(" " + pad(p) for p in pads)
    out.append(")")
    return "\n".join(out)

def resistor(ref, value, x, y, a, b):
    return footprint("GazoPreliminary:R_0805_TBC", ref, value, x, y,
        [smd("1", -0.95, 0, a), smd("2", 0.95, 0, b)],
        rect(-1, -0.62, 1, 0.62, "F.Fab", ref), attr="smd",
        ref_y=-1.65, val_y=1.65,
        description="TBC 0805 land pattern. Confirm series, power derating and exact pads.")

def header(ref, value, x, y, nets, description):
    pads = [pth(i+1, 0, (i-(len(nets)-1)/2)*2.54, n,
                "rect" if i == 0 else "circle") for i, n in enumerate(nets)]
    half = len(nets)*1.27 + 0.5
    return footprint(f"GazoPreliminary:PinHeader_1x{len(nets)}_P2.54_TBC",
        ref, value, x, y, pads, rect(-1.4, -half, 1.4, half, "F.SilkS", ref),
        ref_y=-half-1, val_y=half+1, description=description)

def cap(ref, value, x, y, radius, n1, n2, description):
    size_tag = f"{radius:g}".replace(".", "p")
    library_name = f"GazoPreliminary:Capacitor_THT_2.50mm_TBC_R{size_tag}"
    return footprint(library_name, ref, value, x, y,
        [pth("1", -1.25, 0, n1, "rect"), pth("2", 1.25, 0, n2)],
        [circle(radius, "F.Fab", ref),
         line(-radius*.7, -radius*.7, -radius*.2, -radius*.7, "F.SilkS", ref)],
        ref_y=-radius-1, val_y=radius+1, description=description)

def led(ref, value, x, y, na, nk, *, ref_y=-3.6):
    return footprint("GazoPreliminary:LED_D5.0mm_P2.54_TBC", ref, value, x, y,
        [pth("1", -1.27, 0, na, "rect"), pth("2", 1.27, 0, nk)],
        [circle(2.5, "F.SilkS", ref), line(-2.5, 0, -1.7, 0, "F.Fab", ref)],
        ref_y=ref_y, val_y=3.6,
        description="5mm LED placeholder. Verify exact KIPD42B package and polarity.")

def transistor(ref, value, x, y, nc, nb, ne, role):
    return footprint("GazoPreliminary:KT26_KT3102GM_PINOUT_TBC", ref, value, x, y,
        [pth("1", -2.5, 0, nc, "rect", 1.7, .8),
         pth("2", 0, 0, nb, "circle", 1.7, .8),
         pth("3", 2.5, 0, ne, "circle", 1.7, .8)],
        rect(-3.1, -2, 3.1, 2, "F.Fab", ref) +
        [line(-1, -2, 1, -2, "F.SilkS", ref)],
        ref_y=-3.2, val_y=3.2,
        description=f"KT-26 placeholder for {role}. Pin order C/B/E is provisional, verify exact manufacturer's drawing.")

def build_board():
    parts = [
        header("J2", "A1 SIGNAL S/V/G", 104.5, 113, ["SENSE", "+5V", "GND"],
               "Amperka AMP-B052 signal-side pads S/V/G."),
        header("J3", "A1 HEATER E/H/G", 104.5, 125, ["+5V", "+5V", "GND"],
               "Amperka AMP-B052 heater pads E/H/G, E pulled high to enable heater."),
        footprint("GazoPreliminary:PowerIn_1x2_P5.08_TBC", "J1", "XS1 5V INPUT", 168.2, 111,
            [pth("1", 0, -2.54, "+5V", "rect", 2, 1), pth("2", 0, 2.54, "GND", "circle", 2, 1)],
            rect(-3, -4, 3, 4, "F.SilkS", "J1"), ref_y=-5.2, val_y=5.2,
            description="Connector body, pin pitch and current rating TBC."),
        footprint("GazoPreliminary:TLV7041Q_SOT23-5_TBC", "U2", "TLV7041-Q1", 115.5, 115,
            [smd("1", -1.15, -.95, "DOUT", .95, .50),
             smd("2", -1.15, 0, "GND", .95, .50),
             smd("3", -1.15, .95, "UREF", .95, .50),
             smd("4", 1.15, .95, "SENSE", .95, .50),
             smd("5", 1.15, -.95, "+5V", .95, .50)],
            rect(-1.5, -1, 1.5, 1, "F.Fab", "U2"), attr="smd",
            ref_y=-2.15, val_y=2.15,
            description="SOT-23-5 TBC. Pin map 1 OUT,2 GND,3 UREF,4 S,5 VCC; verify TI land pattern."),
        resistor("R1", "160k", 120.5, 110.5, "+5V", "DOUT"),
        resistor("R8", "2.2k", 120.5, 114.5, "+5V", "DOUT"),
        resistor("RHYS", "100k", 124, 119, "DOUT", "UREF"),
        resistor("R2", "10k", 126.5, 114.5, "DOUT", "VT1_BASE"),
        transistor("VT1", "KT3102GM / VT1", 132, 115.5, "RESET", "VT1_BASE", "GND", "RESET control"),
        resistor("R3", "2k", 138.5, 114.5, "+5V", "RESET"),
        header("P1", "10k POT TBC", 114, 135.5, ["+5V", "UREF", "GND"],
               "External potentiometer pad header. The physical potentiometer is not selected."),
    ]
    da_pads = [
        pth("1", -3.75, -3.75, "GND", "rect", 1.7, .8),
        pth("2", -3.75, -1.25, "TIMER_CT", "circle", 1.7, .8),
        pth("3", -3.75, 1.25, "OUT", "circle", 1.7, .8),
        pth("4", -3.75, 3.75, "RESET", "circle", 1.7, .8),
        pth("5", 3.75, 3.75, "TIMER_CTRL", "circle", 1.7, .8),
        pth("6", 3.75, 1.25, "TIMER_CT", "circle", 1.7, .8),
        pth("7", 3.75, -1.25, "TIMER_DISCH", "circle", 1.7, .8),
        pth("8", 3.75, -3.75, "+5V", "circle", 1.7, .8),
    ]
    parts.append(footprint("GazoPreliminary:KR1006VI1_2101.8-1_P2.50x7.50_TBC",
        "DA1", "KR1006VI1", 142, 123.5, da_pads,
        rect(-5, -3.75, 5, 3.75, "F.Fab", "DA1") +
        [line(-1, -3.75, 1, -3.75, "F.SilkS", "DA1")],
        ref_y=-5, val_y=5,
        description="Custom package placeholder based on passport 2101.8-1. Verify exact vendor drawing."))
    parts += [
        resistor("R4", "8.2k", 149, 112.5, "+5V", "TIMER_DISCH"),
        resistor("R5", "8.2k", 149, 117, "TIMER_DISCH", "TIMER_CT"),
        cap("C1", "4.7uF TBC", 155, 115, 3, "TIMER_CT", "GND",
            "Timing cap conflicts with source text stating 1-2Hz. Package and polarity TBC."),
        cap("C2", "100nF TBC", 147.2, 132.5, 2, "TIMER_CTRL", "GND",
            "K10-17A exact package not confirmed."),
        cap("C3", "47uF TBC", 163.5, 119, 3.4, "+5V", "GND",
            "K50-35 exact body/voltage/pitch not confirmed."),
        footprint("GazoPreliminary:C_0805_TBC", "C4", "100nF U2 bypass", 119.1, 118,
            [smd("1", -.95, 0, "+5V"), smd("2", .95, 0, "GND")],
            rect(-1, -.62, 1, .62, "F.Fab", "C4"), attr="smd",
            ref_y=-1.65, val_y=1.65, description="U2 local bypass. Verify dielectric and tolerance."),
        resistor("R6", "220R", 141.5, 134.5, "OUT", "HL1_A"),
        led("HL1", "RED 5mm TBC", 141.5, 140.5, "HL1_A", "GND"),
        resistor("R7", "220R", 152, 132.5, "+5V", "HL2_A"),
        led("HL2", "GREEN 5mm TBC", 152, 140.5, "HL2_A", "SA1_LED_RETURN", ref_y=4.5),
    ]
    sa_pads = [
        pth("1", -1.27, -2.54, "SOUND_CTL", "rect"),
        pth("2", -1.27, 0, "OUT"),
        pth("3", -1.27, 2.54, None),
        pth("4", 1.27, -2.54, "GND", "rect"),
        pth("5", 1.27, 0, "SA1_LED_RETURN"),
        pth("6", 1.27, 2.54, None),
    ]
    parts.append(footprint("GazoPreliminary:SA1_DPDT_2Pole_2.54_TBC", "J4", "SA1 DPDT SWITCH", 108.0, 135.0,
        sa_pads, rect(-3.1, -4, 3.1, 4, "F.SilkS", "J4"),
        ref_y=-5.2, val_y=5.2,
        description="External DPDT switch header. Physical switch and pin map TBC."))
    parts += [
        resistor("R9", "560R", 158.5, 126.5, "SOUND_CTL", "VT2_BASE"),
        transistor("VT2", "KT3102GM / VT2", 164.5, 129.5, "BUZZ_COL", "VT2_BASE", "GND", "buzzer driver"),
        footprint("GazoPreliminary:Diode_Axial_P7.62_TBC", "VD1", "KD510A TBC", 149.6, 136.2,
            [pth("1", -3.81, 0, "BUZZ_COL", "rect"), pth("2", 3.81, 0, "+5V")],
            rect(-2.7, -1, 2.7, 1, "F.Fab", "VD1") +
            [line(1.2, -1, 1.2, 1, "F.SilkS", "VD1", .15)],
            ref_x=-1.5, ref_y=1.5, val_y=2.2, description="KD510A package and polarity marking TBC."),
        footprint("GazoPreliminary:Buzzer_HCM1205X_P7.6_TBC", "HA1", "JL WORLD HCM1205X", 161.2, 139,
            [pth("1", -3.8, 0, "+5V", "rect", 1.7, .9), pth("2", 3.8, 0, "BUZZ_COL", "circle", 1.7, .9)],
            [circle(6, "F.SilkS", "HA1", .15), circle(4, "F.Fab", "HA1")],
            ref_y=-7.2, val_y=7.2, description="JL World HCM1205X OD12x9.5mm, pitch7.6mm, lead dia0.6mm."),
    ]
    for ref, x, y in [("H1",103.5,103.5),("H2",168.5,103.5),("H3",103.5,146.5),("H4",169.5,147.0)]:
        parts.append(footprint("GazoPreliminary:MountingHole_M3_TBC",ref,"M3_CLR",x,y,
            [pth("",0,0,None,"circle",3.2,3.2,"np_thru_hole")],
            [circle(1.6,"F.Fab",ref)],attr="through_hole exclude_from_bom exclude_from_pos_files",
            ref_y=-2.3,val_y=2.3,description="M3 clearance placeholder; confirm screw/boss tolerances."))

    layers = '''(layers
      (0 "F.Cu" signal "top_cu") (2 "B.Cu" signal "bottom_cu")
      (9 "F.Adhes" user "F.Adhesive") (11 "B.Adhes" user "B.Adhesive")
      (13 "F.Paste" user) (15 "B.Paste" user)
      (5 "F.SilkS" user "F.Silkscreen") (7 "B.SilkS" user "B.Silkscreen")
      (1 "F.Mask" user) (3 "B.Mask" user)
      (17 "Dwgs.User" user "User.Drawings") (19 "Cmts.User" user "User.Comments")
      (21 "Eco1.User" user "User.Eco1") (23 "Eco2.User" user "User.Eco2")
      (25 "Edge.Cuts" user) (27 "Margin" user)
      (31 "F.CrtYd" user "F.Courtyard") (29 "B.CrtYd" user "B.Courtyard")
      (35 "F.Fab" user) (33 "B.Fab" user)
    )'''
    out = [
        "(kicad_pcb", '(version 20241229)', '(generator "gazo_preliminary_generator")',
        '(generator_version "9.0")', '(general (thickness 1.6) (legacy_teardrops no))',
        '(paper "A4")',
        '(title_block (title "gazo_analizator - preliminary control PCB") (date "2026-10-25") (rev "PRELIMINARY 0.1") (comment 1 "NOT FOR FABRICATION") (comment 2 "UNROUTED placement draft with TBC footprints"))',
        layers, '(setup (pad_to_mask_clearance 0) (allow_soldermask_bridges_in_footprints no) (tenting front back))'
    ]
    out.extend(f"(net {i} {q(name)})" for i, name in enumerate(NETS))
    out.extend(parts)
    edges = [("bottom",(100,100),(172,100)),("right",(172,100),(172,150)),
             ("top",(172,150),(100,150)),("left",(100,150),(100,100))]
    for key, (x1,y1), (x2,y2) in edges:
        out.append(f'(gr_line (start {x1} {y1}) (end {x2} {y2}) (stroke (width 0.15) (type default)) (layer "Edge.Cuts") (uuid {q(ident("edge-"+key))}))')
    out.append(f'(gr_text "PRELIMINARY / NOT FOR FABRICATION" (at 136 148 0) (layer "Cmts.User") (uuid {q(ident("notice-prelim"))}) (effects (font (size 1.3 1.3) (thickness 0.25))))')
    out.append(f'(gr_text "NO COPPER ROUTING - CONNECTIVITY WARNINGS EXPECTED" (at 136 146 0) (layer "Cmts.User") (uuid {q(ident("notice-routing"))}) (effects (font (size 0.9 0.9) (thickness 0.18))))')
    out.append(")")
    return "\n".join(out) + "\n"

def extract_sexpr(text, start):
    depth, quoted, escaped = 0, False, False
    for index in range(start, len(text)):
        ch = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
        else:
            if ch == '"':
                quoted = True
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return text[start:index + 1]
    raise ValueError(f"Unterminated footprint S-expression at {start}")


def write_footprint_library(board):
    library_root = OUT.parent / "footprints" / "GazoPreliminary.pretty"
    library_root.mkdir(parents=True, exist_ok=True)
    # Remove old generated files first. Package-specific IDs can change between
    # generator revisions, and stale library files must not survive a rebuild.
    for stale in library_root.glob("*.kicad_mod"):
        stale.unlink()
    matches = list(re.finditer(r'\(footprint "GazoPreliminary:([^"]+)"', board))
    seen = set()
    for match in matches:
        lib_name = match.group(1)
        if lib_name in seen:
            continue
        seen.add(lib_name)
        block = extract_sexpr(board, match.start())
        old_header = f'(footprint "GazoPreliminary:{lib_name}"'
        new_header = f'(footprint "{lib_name}"'
        if old_header not in block:
            raise ValueError(f"Footprint header mismatch for {lib_name}")
        block = block.replace(old_header, new_header, 1)
        # Board-only pad net assignments are not legal library footprint data.
        block = re.sub(r'\s+\(net \d+ "[^"]*"\)', "", block)
        block = re.sub(r'(\(property "Reference" )"[^"]+"',
                       r'\1"REF**"', block, count=1)
        block = re.sub(r'(\(property "Value" )"[^"]+"',
                       lambda m: m.group(1) + q(lib_name), block, count=1)
        (library_root / f"{lib_name}.kicad_mod").write_text(block + "\n", encoding="utf-8")
    if not seen:
        raise RuntimeError("No GazoPreliminary footprints found in generated PCB")
    dollar = chr(36)
    uri = dollar + "{KIPRJMOD}/footprints/GazoPreliminary.pretty"
    table = OUT.parent / "fp-lib-table"
    table.write_text(
        '(fp_lib_table\n'
        '  (version 7)\n'
        f'  (lib (name "GazoPreliminary")(type "KiCad")(uri "{uri}")'
        '(options "")(descr "Preliminary custom footprints; verify TBC dimensions"))\n'
        ')\n',
        encoding="utf-8"
    )
    print(f"Generated KiCad custom library with {len(seen)} footprints: {library_root}")
    return len(seen)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    board = build_board()
    depth, quoted, escaped = 0, False, False
    for ch in board:
        if quoted:
            if escaped: escaped = False
            elif ch == "\\": escaped = True
            elif ch == '"': quoted = False
        else:
            if ch == '"': quoted = True
            elif ch == "(": depth += 1
            elif ch == ")": depth -= 1
            if depth < 0: raise SystemExit("Unbalanced S-expression: negative depth")
    if depth != 0 or quoted: raise SystemExit(f"Unbalanced S-expression: depth={depth}")
    for ref in ["J1","J2","J3","U2","VT1","DA1","VT2","HA1","H1","H2","H3","H4"]:
        if f'(property "Reference" "{ref}"' not in board:
            raise SystemExit(f"Missing footprint reference {ref}")
    OUT.write_text(board, encoding="utf-8")
    footprint_count = write_footprint_library(board)
    print(f"Generated {OUT} ({len(board)} chars).")
    print(f"Generated {footprint_count} custom footprints. PRELIMINARY / UNROUTED / NOT FOR FABRICATION.")

if __name__ == "__main__": main()
