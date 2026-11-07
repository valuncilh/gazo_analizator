# Rev5 engineering checkpoint 01 — immutable source intake

Date: 2026-11-07  
Branch: `design/usb-c-pcb-enclosure-r5`  
Base commit: `4451222a416302e97e1f25da4e60df7309f7445f`

## Done

- Created the dedicated Rev5 branch without changing the pre-existing engineering branch.
- Materialized the original routed KiCad PCB candidate, second placement PCB snapshot, schematic candidate, PCB STEP, DRC2 report, repair patch, and previous R3 enclosure/sensor packages.
- Calculated SHA-256 for every immutable input.
- Created and uploaded the immutable baseline archive and separate copies of the core PCB, schematic, STEP, and checksum files to OneDrive.
- Added the mandatory source-preservation policy to this branch.
- Confirmed native KiCad CLI and FreeCAD executables are not installed in this preparation environment. CadQuery and OpenCascade bindings are available. No native KiCad DRC/ERC or FreeCAD recompute is claimed.

## Confirmed geometry and PCB contents

- Routed PCB candidate: 23 footprints, 207 segments, 21 vias, 5 zones.
- PCB thickness: 1.6 mm.
- Four Ø2.2 mm NPTH mounting holes:
  - MH1: X=172.0, Y=127.5 mm.
  - MH2: X=224.0, Y=127.5 mm.
  - MH3: X=172.0, Y=164.5 mm.
  - MH4: X=224.0, Y=164.5 mm.
- Board outline: X=168.5…227.5 mm, Y=123.5…168.5 mm. Size 59 × 45 mm.
- Hole pattern: 52 × 37 mm.
- A1: (173.0, 140.0), rotation −90°. XS1: (173.0, 151.21), rotation −90°.
- DRC2 report says native DRC was not rerun after static repairs and zones were not refilled. This file is a routed candidate baseline, not a release-ready DRC-PASS board.

## Not done

- No source PCB file was modified in this checkpoint.
- XS1 is still present in the immutable source.
- No USB-C footprint has yet been placed on the routed board.
- The schematic has not yet been reconciled with the USB-C input.
- No USB-C current protection value has been frozen.
- No Rev5 PCB STEP or FreeCAD enclosure has been generated.
- No native KiCad DRC/ERC or native FreeCAD recompute has been run.

## Checks

- SHA-256 calculated for all source files and archived.
- PCB S-expression static counts verified.
- Exact Edge.Cuts rectangle and M2 hole coordinates read from the PCB file.
- R3 packages retained, not overwritten.
- No claim of native EDA/CAD validation.

## Next

1. Audit all electrical nets and trace connectivity around XS1/VCC/Earth from the routed PCB and schematic.
2. Confirm the GCT USB4105 footprint orientation, actual solder pad mapping, shell anchor slots, board-edge datum, and 3D envelope.
3. Create a new schematic revision with USB-C sink wiring and protection. Preserve the old schematic.
4. Produce a distinct Rev5 PCB placement copy. Remove XS1 only from the new copy, relocate the power-input boundary to USB-C on the opposite short edge, and preserve the four M2 holes and all unrelated nets.
5. Re-route, refill zones, and run native KiCad ERC/DRC on the final saved project.
6. Only after PCB freeze, export a versioned PCB STEP and begin Rev5 FreeCAD enclosure modelling.
