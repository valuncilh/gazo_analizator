# Original 2022 KiCad reference

This directory contains a standalone KiCad transcription of the published external circuit. It preserves the printed values and uses named net labels to represent the connections documented in [`data/original_scheme_reference.md`](../../data/original_scheme_reference.md). The A1 symbol is only a connector: its internal circuitry, exact module, output stage, and footprint are unknown. AOUT is intentionally unconnected.

The A1 pin numbers are conditional KiCad symbol numbers only; they do not establish the physical pin order of the unidentified module. The SVG is a connectivity drawing for this transcription, not a graphical facsimile of the published figure. Further graphic refinement remains open.

The drawing is based on the online reproduction listed as S1 in [`data/source_register.md`](../../data/source_register.md); it has not been checked against a scan of the printed pages. The 1–2 Hz statement conflicts with the frequency calculated from the printed R4, R5, and C1 values. The schematic keeps the printed values unchanged and notes that discrepancy.

Regenerate the schematic using Python 3 and an installed KiCad symbol library, then refresh the retained ERC, netlist, BOM, and SVG artifacts:

```sh
python3 cad/original_2022/generate_schematic.py
mkdir -p cad/original_2022/reports cad/original_2022/exports
kicad-cli sch erc --severity-all -o cad/original_2022/reports/original_2022_erc.rpt cad/original_2022/original_2022.kicad_sch
kicad-cli sch export netlist --format kicadxml -o cad/original_2022/reports/original_2022.net cad/original_2022/original_2022.kicad_sch
kicad-cli sch export bom -o cad/original_2022/reports/original_2022_bom.csv cad/original_2022/original_2022.kicad_sch
kicad-cli sch export svg -o cad/original_2022/exports cad/original_2022/original_2022.kicad_sch
python3 cad/original_2022/verify_netlist.py cad/original_2022/reports/original_2022.net
```

ERC and netlist generation check the KiCad document and represented connectivity, not the physical behavior or safety of the published circuit. No PCB is included: footprints and physical dimensions are not established by the source transcription.
