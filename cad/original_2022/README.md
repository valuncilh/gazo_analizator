# Original 2022 KiCad reference

This directory contains a standalone KiCad transcription of the published external circuit. It preserves the printed values and uses named net labels to represent the connections documented in [`data/original_scheme_reference.md`](../../data/original_scheme_reference.md). The A1 symbol is only a connector: its internal circuitry, exact module, output stage, and footprint are unknown. AOUT is intentionally unconnected.

The drawing is based on the online reproduction listed as S1 in [`data/source_register.md`](../../data/source_register.md); it has not been checked against a scan of the printed pages. The 1–2 Hz statement conflicts with the frequency calculated from the printed R4, R5, and C1 values. The schematic keeps the printed values unchanged and notes that discrepancy.

Regenerate the schematic using Python 3 and an installed KiCad symbol library:

```sh
python3 cad/original_2022/generate_schematic.py
kicad-cli sch erc --severity-all cad/original_2022/original_2022.kicad_sch
kicad-cli sch export netlist --format kicadxml -o /tmp/original_2022.net cad/original_2022/original_2022.kicad_sch
kicad-cli sch export bom -o /tmp/original_2022_bom.csv cad/original_2022/original_2022.kicad_sch
```

ERC and netlist generation check the KiCad document and represented connectivity, not the physical behavior or safety of the published circuit. No PCB is included: footprints and physical dimensions are not established by the source transcription.
