# Project modification schematic verification

**Status:** preliminary, separate from Original 2022; not approved for routing or fabrication.

## Environment and reproducible commands

- KiCad CLI version: **10.0.7**.
- ERC: `kicad-cli sch erc --severity-all -o cad/project_modification/reports/project_modification_erc.rpt cad/project_modification/project_modification.kicad_sch`.
- Netlist: `kicad-cli sch export netlist --format kicadxml -o cad/project_modification/reports/project_modification.net cad/project_modification/project_modification.kicad_sch`.
- BOM: `kicad-cli sch export bom -o cad/project_modification/reports/project_modification_bom.csv cad/project_modification/project_modification.kicad_sch`.
- Exact pin/net comparison: `python3 -B cad/project_modification/verify_netlist.py cad/project_modification/reports/project_modification.net`.
- SVG/PNG exports were visually reviewed at full-sheet scale; A1 and the DA1 timing/output area were checked for overlapping labels. The retained PNG was rendered from the retained SVG; a repeat render compared with `magick compare -metric AE` returned zero changed pixels. `git diff --check` passed after SVG whitespace normalization.

## ERC coverage and outcome

The project explicitly sets `single_global_label=warning`, `four_way_junction=warning`, `simulation_model_issue=error`, and `footprint_filter=warning`; `erc_exclusions` is empty. KiCad 10.0.7 reports **0 errors and 17 warnings**, all `footprint_filter` because footprints are intentionally unassigned. The report's `Ignored checks` section says **None**. Thus no ERC category is ignored, but the result is not zero warnings and does not establish electrical operation.

## Netlist and component audit

The checker compares full unordered membership of every net and also the complete component reference list and pin inventory. It requires every pin to occur once in a connected net or the explicit NC set. Result: **PASS** — 13 connected nets, 19 components, all 47 symbol pins accounted for (46 connected and A1.3 intentionally NC). BOM count is 19. A1 pin numbering is only a logical KiCad connector abstraction; it is not Joy-IT physical pinout.

## Design changes and limitations

- Preliminary A1 choice: Joy-IT SEN-MQ4 V1; exact revision, output topology, V1-specific DOUT polarity and total module current remain undocumented in the sources reviewed. The assumed active-low behavior derives from Joy-IT family guidance, not a revision-specific guarantee.
- Project target: 1000 ppm CH₄. Manufacturer adjustment range does not prove calibrated accuracy at 1000 ppm; no physical gas testing is planned.
- C1 changes from Original 4.7 µF to project 47 µF. The nominal estimate is `T≈0.693·(8.2k+2·8.2k)·47µF≈0.801 s`, `f≈1.25 Hz`. This is an independent project choice; the Original values are untouched.
- DOUT drive into the retained 13 kΩ base path, sounder current, component tolerance corners, total supply current ≤300 mA, and supply operation at 4.9/5.1 V remain to be calculated. Heater current ≤180 mA alone does not confirm the whole-device budget.
- The sheet is a visual/electrical transcription for review, not a completed E3 drawing. No PCB, footprint assignment, SPICE run, mechanical fit check or electrical approval has been completed in this step.
