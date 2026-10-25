#!/usr/bin/env python3
"""Static validation and provisional BOM for the placement-only KiCad board."""
import csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PCB = ROOT / "cad/kicad/gazo_analizator_preliminary.kicad_pcb"
OUT = ROOT / "cad/output"
OUT.mkdir(parents=True, exist_ok=True)
PARTS = [
("J1","XS1 5V input","PowerIn_1x2_P5.08_TBC","Connector body/pitch/current rating TBC"),
("J2","AMP-B052 signal S/V/G","PinHeader_1x3_P2.54_TBC","External module connector"),
("J3","AMP-B052 heater E/H/G","PinHeader_1x3_P2.54_TBC","E tied to +5V to enable heater"),
("U2","TLV7041-Q1","SOT23-5_TBC","Verify TI land pattern and pin1"),
("R1","160 kOhm","0805_TBC","Confirm series and derating"),
("R2","10 kOhm","0805_TBC","Confirm series and derating"),
("R3","2 kOhm","0805_TBC","Confirm series and derating"),
("R4","8.2 kOhm","0805_TBC","RC timer value conflicts with 1-2 Hz source text"),
("R5","8.2 kOhm","0805_TBC","RC timer value conflicts with 1-2 Hz source text"),
("R6","220 Ohm","0805_TBC","Check LED current and resistor power"),
("R7","220 Ohm","0805_TBC","Check LED current and resistor power"),
("R8","2.2 kOhm","0805_TBC","Open-drain pull-up"),
("RHYS","100 kOhm","0805_TBC","Hysteresis feedback"),
("R9","560 Ohm","0805_TBC","Check output loading"),
("VT1","KT3102GM VT1","KT26_TBC","Exact manufacturer pinout/saturation not confirmed"),
("VT2","KT3102GM VT2","KT26_TBC","Exact manufacturer pinout/saturation not confirmed"),
("DA1","KR1006VI1","2101.8-1_TBC","Confirm vendor drawing"),
("C1","4.7 uF","THT_2.50_TBC","Do not change until frequency conflict is resolved"),
("C2","100 nF","THT_2.50_TBC","Exact K10-17A body not confirmed"),
("C3","47 uF","THT_2.50_TBC","Exact K50-35 body not confirmed"),
("C4","100 nF U2 bypass","0805_TBC","Confirm dielectric/tolerance"),
("HL1","Red LED 5 mm","LED5_TBC","Confirm KIPD42B footprint/polarity"),
("HL2","Green LED 5 mm","LED5_TBC","Confirm KIPD42B footprint/polarity"),
("VD1","KD510A","Axial7.62_TBC","Confirm dimensions/polarity"),
("HA1","JL World HCM1205X","Buzzer7.6_TBC","OD12 x 9.5mm, lead pitch 7.6mm"),
("P1","10 kOhm trim potentiometer","External1x3_TBC","Physical potentiometer not selected"),
("J4","SA1 DPDT switch header","2PoleHeader_TBC","Physical switch not selected"),
("H1-H4","M3 clearance holes","NPTH3.2_TBC","Verify screws and case bosses"),
]
def balanced(text):
    d, quoted, escaped = 0, False, False
    for ch in text:
        if quoted:
            if escaped: escaped = False
            elif ch == "\\": escaped = True
            elif ch == '"': quoted = False
        else:
            if ch == '"': quoted = True
            elif ch == "(": d += 1
            elif ch == ")": d -= 1
            if d < 0: return False
    return d == 0 and not quoted
def main():
    if not PCB.is_file(): raise SystemExit(f"PCB file not found: {PCB}")
    text = PCB.read_text(encoding="utf-8")
    if not balanced(text): raise SystemExit("Unbalanced KiCad PCB S-expression")
    found = re.findall(r'\(property "Reference" "([^"]+)"', text)
    missing = [r for r in ["J1","J2","J3","U2","VT1","DA1","VT2","HA1","H1","H2","H3","H4"] if r not in found]
    if missing: raise SystemExit("Missing footprint refs: " + ", ".join(missing))
    if "NOT FOR FABRICATION" not in text or "NO COPPER ROUTING" not in text:
        raise SystemExit("Missing preliminary warnings")
    tracks = len(re.findall(r'\((?:segment|via)\b', text))
    fp_table = ROOT / "cad/kicad/fp-lib-table"
    fp_root = ROOT / "cad/kicad/footprints/GazoPreliminary.pretty"
    fp_files = sorted(fp_root.glob("*.kicad_mod")) if fp_root.is_dir() else []
    if not fp_table.is_file():
        raise SystemExit("Missing KiCad custom footprint library table.")
    if len(fp_files) < 10:
        raise SystemExit(f"Too few custom footprints generated: {len(fp_files)}")
    no_courtyard = [p.name for p in fp_files if '(layer "F.CrtYd")' not in p.read_text(encoding="utf-8")]
    if no_courtyard:
        raise SystemExit("Custom footprints missing provisional courtyard: " + ", ".join(no_courtyard))
    with (OUT/"preliminary_bom.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w=csv.writer(f); w.writerow(["Reference","Value","Provisional footprint","Open verification item"]); w.writerows(PARTS)
    with (OUT/"preliminary_placements.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w=csv.writer(f); w.writerow(["Reference","Value","Status"]); w.writerows([[r,v,"PRELIMINARY, verify in KiCad"] for r,v,fp,note in PARTS])
    summary={"pcb_file":"cad/kicad/gazo_analizator_preliminary.kicad_pcb","board_size_mm":[72,50,1.6],"references_found":len(found),"bom_rows":len(PARTS),"custom_footprints":len(fp_files),"custom_footprints_with_courtyard":len(fp_files)-len(no_courtyard),"segments_and_vias":tracks,"routing_status":"UNROUTED","manufacturing_status":"NOT FOR FABRICATION","limitations":["KT3102GM pinout not manufacturer-verified","TBC passive/connector footprints remain","No KiCad schematic/ERC netlist parity","Do not issue Gerber/drill from this draft"]}
    (OUT/"preliminary_cad_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (OUT/"preliminary_cad_summary.md").write_text("# CAD static check\n\n**PRELIMINARY / NOT FOR FABRICATION**\n\n"+f"- Board size: 72 x 50 x 1.6 mm\n- References found: {len(found)}\n- BOM rows: {len(PARTS)}\n- Custom footprint files: {len(fp_files)}\n- Footprints with provisional F.CrtYd: {len(fp_files)-len(no_courtyard)}\n- Copper tracks/vias: {tracks}\n- Routing is not started; DRC unconnected warnings are expected.\n- Exact footprints, pinouts and schematic parity remain open.\n",encoding="utf-8")
    print(f"Static PCB check passed. References={len(found)}, BOM rows={len(PARTS)}, footprints={len(fp_files)}, tracks={tracks}.")
if __name__=="__main__": main()
