# Stage03 — USB-C placement candidate review

## Changed

- Created a new PCB file from the immutable routed DRC2 source.
- Added GCT USB4105 J1 and two 5.1 kΩ 0805 CC pull-down resistor footprints R8/R9.
- Added USB-C pin-net assignments and shell pads. D+/D−/SBU remain NC.
- Kept XS1 as temporary legacy power input; no final power-source replacement is claimed.
- Preserved 59×45 mm outline, four M2 holes, all pre-existing track segments, vias and copper zones.

## Static verification

- S-expression structural balance: PASS.
- UUID uniqueness: 946/946, no duplicates.
- Footprint/reference count: 26, no duplicate references.
- Track segments/vias/zones unchanged vs source: 207/25/5.
- M2 centers unchanged: PASS.
- USB PCB-edge datum equals Edge.Cuts Y=123.500: PASS.
- USB electrical pad assignment: static inspection PASS.
- Courtyard collision pairs below 0.25 mm: 0.
- Minimum courtyard clearance: 0.885 mm.
- Minimum new pad-edge to old track-edge clearance: 0.3169 mm.
- Existing track crossings through USB courtyard: 0.

## Not done

- Native KiCad DRC/ERC and zone refill.
- Schematic update and full netlist parity.
- Copper routing VBUS/GND/CC.
- Final power protection/current selection.
- Removal of XS1 from a future completed revision.
- New board STEP and FreeCAD enclosure.

## User review requested

Open the Stage03 board in KiCad 10.0.7 and inspect:
1. USB-C orientation and the side of the case where it exits.
2. The two CC resistors and their clearance to the buzzer/LED.
3. The four shell stakes and two locating holes.
4. 3D Viewer connector shell projection.
5. Board hole table against any mechanical STEP/reference.

Run Refill All Zones and native DRC locally if possible. Send the DRC report or a screenshot of the PCB Editor/3D Viewer. Do not modify or save over the immutable baseline; use a copy of Stage03.
