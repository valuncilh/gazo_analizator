# Rev5 engineering checkpoint 03 — USB-C PCB placement candidate

Date: 2026-11-07
Branch: `design/usb-c-pcb-enclosure-r5`
Starting commit: `832145b688db05b3126107ba5dbd747a74820c44`

## Done

- Created a new PCB artifact at Stage03 path; original DRC2 routed board remains immutable.
- Added USB4105 J1 and CC pull-down resistors R8/R9.
- Kept XS1 temporarily. It will be removed only in a later version after its replacement input path is actually connected and checked.
- Preserved all four M2 holes, board outline, 207 routes, 25 vias and 5 copper zones.
- Generated renderings, JSON static audit, hole table, full drill schedule, build/render scripts, SHA manifest and complete ZIP.
- Uploaded individual artifacts and ZIP to the Stage03 OneDrive folder.
- Verified OneDrive folder listing and created view links to folder, ZIP and editable PCB.

## Checks and results

- PCB S-expression balance: PASS.
- UUID uniqueness: 946 UUIDs, zero duplicates.
- Footprints: 26, no duplicate references.
- Routes/vias/zones retained: 207/25/5.
- M2 centers unchanged.
- USB edge datum maps to board Edge.Cuts at Y=123.500 mm.
- Minimum static courtyard clearance: 0.885 mm.
- Minimum new pad-to-existing-track edge clearance: 0.3169 mm.
- No intersections of USB courtyard with existing tracks.

## Exact artifact locations

OneDrive folder:
https://1drv.ms/f/c/24fda6920aa8c92a/IgDAm06P30bhQL4P4ST_QhPPAeOlVd40lZh9Fiod0AYJDjM

PCB:
https://1drv.ms/u/c/24fda6920aa8c92a/IQC87rWVi-XjQohqghzMzB0QAaIV4ggXGasmHesOrV-PHiQ

Complete ZIP:
https://1drv.ms/u/c/24fda6920aa8c92a/IQAlDy0rexlITJ0wN4pNTUEEASRN_l5IGK1uom9vudSFx8E

Local generation directory:
`/mnt/data/work_r5/stage03_pcb_candidate/`

Main PCB:
`pcb/gazo_e3_rev5_usb_c_placement.kicad_pcb`

Source baseline copy:
`reference/gazo_e3_E3_DRC2_repaired.kicad_pcb`

Drawing:
`drawings/PCB_STAGE03_USB_C_PLACEMENT.png`

Audit:
`reports/PCB_STAGE03_STATIC_AUDIT.json`

Scripts:
`scripts/build_stage03_pcb_candidate.py`
`scripts/render_stage03_review.py`

## Not done

- No native KiCad ERC/DRC was run. No zone refill via KiCad was performed.
- Schematic is not yet updated. Full schematic-to-board netlist parity is not established.
- VBUS/GND/CC copper paths and protection are not routed or frozen.
- XS1 remains in candidate as a temporary old input.
- No new PCB STEP or FreeCAD enclosure.

## Next action

User review in KiCad 10.0.7 is requested for placement, connector orientation, 3D shell/body, mechanical cutout direction, and hole table. Then update schematic/power input, route nets, perform native DRC/ERC, export the new PCB STEP, and model the enclosure.
