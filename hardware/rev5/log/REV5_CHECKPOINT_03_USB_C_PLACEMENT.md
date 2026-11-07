# Rev5 engineering checkpoint 03R1 — USB-C PCB placement audit correction

Date: 2026-11-07
Branch: `design/usb-c-pcb-enclosure-r5`
Starting commit: `832145b688db05b3126107ba5dbd747a74820c44`

## Done

- Created the Stage03 USB-C PCB candidate from the immutable routed DRC2 baseline.
- Added USB4105 J1 and CC pull-down resistors R8/R9.
- Kept XS1 temporarily. It will be removed only after the new input path is complete and checked.
- Preserved all four M2 holes, board outline, 207 routes, **21 physical vias** and 5 copper zones.
- Generated renderings, JSON static audit, hole table, proposed drill schedule, build/render scripts, SHA manifest and full ZIP.
- Uploaded the raw PCB and complete bundle to OneDrive.
- Verified OneDrive folder contents and created view links.

## Audit correction R1

The first Stage03 audit script used the broad prefix token `(via`. This matched 21 physical top-level `(via ...)` objects plus four DRC rule settings named `(vias not_allowed)`, reporting 25 by mistake. The corrected parser matches exact top-level via blocks. Direct count is 21 in both source and candidate.

The PCB file itself is byte-identical to the first Stage03 board. SHA-256 remains `ee73c41b8612b430947aaaffa848d30d5a6a46b0dfcfc78702200968f5eb1537`.

## Verified results

- PCB S-expression balance: PASS.
- UUID uniqueness: 946, zero duplicates.
- Footprints: 26, no duplicate references.
- Routes/vias/zones retained: 207/21/5.
- Four M2 centers unchanged.
- USB edge datum maps to Edge.Cuts at Y=123.500 mm.
- Minimum static courtyard clearance: 0.885 mm.
- Minimum new pad-to-existing-track edge gap: 0.3169 mm.
- No intersections of USB courtyard with existing tracks.
- Corrected ZIP integrity checked with no corrupt entries.

## Exact artifacts

OneDrive folder:
https://1drv.ms/f/c/24fda6920aa8c92a/IgD9TMKIfuSgQa_O5KN5br94ATrWzH_ylvcmSph4diZcSJg

PCB:
https://1drv.ms/u/c/24fda6920aa8c92a/IQCzsC2WfO1qQJQvzRn-aAclAT1bQYZMinb9vIwQqvtia24

Corrected ZIP:
https://1drv.ms/u/c/24fda6920aa8c92a/IQC7gkvDHw_XQpgaaWC95G_bAXE4XZnOtcgD5lZMVie5jjY

## Not done

- No native KiCad ERC/DRC was run. No zone refill via KiCad.
- Schematic not yet updated. Full schematic-to-board netlist parity not established.
- VBUS/GND/CC copper routes and input protection not complete.
- XS1 remains.
- No new PCB STEP or FreeCAD enclosure.

## Next

1. Inspect the Stage03R1 board in KiCad 10.0.7. Check USB-C orientation, shell stakes, 3D clearance and case side.
2. Create the schematic revision with USB-C and independent CC1/CC2 resistors.
3. Check sensor heater startup/steady current and choose input protection.
4. Route the new input, refill zones and run native KiCad DRC/ERC.
5. Export the new PCB STEP, then model the FreeCAD enclosure around that geometry.
