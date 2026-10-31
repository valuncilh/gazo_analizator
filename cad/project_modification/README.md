# Project modification schematic

This directory holds the separate preliminary KiCad design for the course project. The Original 2022 reference remains in `../original_2022/`; do not copy project changes back into it.

## Design decisions

- A1 is provisionally Joy-IT SEN-MQ4 V1, with an abstract four-pin connector. The symbol's pin numbers are logical labels only; physical pinout and DOUT output details for the exact V1 revision remain unconfirmed.
- The project target is 1000 ppm CH₄. A module adjustment range containing 1000 ppm is not proof of calibration accuracy at that concentration.
- C1 is 47 µF with R4=R5=8.2 kΩ, an independent project choice giving a nominal 555 estimate of about 1.25 Hz. Original 2022 keeps C1=4.7 µF and its calculated 12.47 Hz discrepancy.
- Other topology/values are retained provisionally to make a separate circuit that can be reviewed. Check DOUT loading, sounder drive, component ratings and the complete ≤300 mA supply budget before electrical approval.

## Files and checks

- `project_modification.kicad_sch` and `.kicad_pro` — editable schematic and ERC configuration.
- `exports/project_modification.svg` and `_preview.png` — reviewed visual exports.
- `reports/project_modification_erc.rpt`, `.net`, and `_bom.csv` — local KiCad outputs.
- `verify_netlist.py` checks all 13 full net memberships, 19 references and 47 pins against `data/project_modification_reference.md`.
- `reports/project_modification_verification_2026-10-31.md` records the exact check results and limits.

Rebuild from the repository root with:

```sh
python3 cad/project_modification/generate_schematic.py
kicad-cli sch erc --severity-all -o cad/project_modification/reports/project_modification_erc.rpt cad/project_modification/project_modification.kicad_sch
kicad-cli sch export netlist --format kicadxml -o cad/project_modification/reports/project_modification.net cad/project_modification/project_modification.kicad_sch
kicad-cli sch export bom -o cad/project_modification/reports/project_modification_bom.csv cad/project_modification/project_modification.kicad_sch
python3 -B cad/project_modification/verify_netlist.py cad/project_modification/reports/project_modification.net
```

ERC currently reports 17 footprint-filter warnings because no PCB footprints are assigned; it reports zero errors and no ignored categories. This preliminary schematic has not been approved for PCB routing. No simulation, physical test or gas calibration is implied by these checks.
