# Checkpoint VLAR — Stage05R5R2 corrected PCB installed / USB-C detail

Дата: 2026-11-08.  
Ветка: `design/usb-c-pcb-enclosure-r5`.  
Статус: static CAD validation complete; native FreeCAD/physical connector verification pending.

## User-provided sources

- Corrected main PCB STL SHA-256: `0a6489358d9ff5d8a8fbd0f9e5916dcffeefa2e925c6cb4ce9a08b2220c7703b`.
- Exact SEN-MQ4-V2 STEP SHA-256: `d064355fa01dd6ed99a5886260bc3dadf1f246ba39076c1bb64b40fadc283ee7`.
- Stage04R3 KiCad PCB reference SHA-256: `ac120c090f22f84342e3be6635b659c08afdf5558355b38c02d2e7035dfdc671`.

## Implemented

1. Inserted the complete corrected PCB STL mesh into the main case frame using a proper 90-degree rotation/translation:
   `X=2.7+y_STL; Y=64.0-x_STL; Z=8.0+z_STL`.
2. Extracted four real PCB mounting holes and matched them to the four M2 support bosses with nominal centre positions (6.7,8.5), (6.7,60.5), (43.7,8.5), (43.7,60.5) mm.
3. Compacted the main enclosure to 50.8×69×27.2 mm.
4. Removed two simplified cuboid J1 placeholders from the PCB mesh.
5. Added a separate 16-solid USB4105-family visual BREP with rounded metal shell, 8.34×2.56 mm mating cavity guidance, central tongue and 12 contacts. This is not an exact supplier STEP model or frozen order suffix.
6. Recut the +X housing wall with a plain 9.4×3.6 mm R1.7 rounded opening. No bezel/trim/insert.
7. Moved the A1 cable aperture to the corrected +Y PCB-edge datum.
8. Kept the independently screw-mounted remote sensor module and exact sensor STEP.

## Validation

- 38/38 BREP/layout/clearance/mechanical checks PASS.
- STEP round-trip 12/12 PASS.
- Four enclosure STL parts 4/4 watertight.
- Corrected PCB mesh: 3319 components, 85214 facets, winding consistent, non-watertight as a single mesh.
- Sensor module: 189 exact STEP solids, exact board-hole pattern and head projection checks.
- ZIP CRC PASS, 54 entries / 45 manifest file hashes. ZIP SHA-256: `3657170fd33f151edff0ae570b49526113ba1bcc761c39b1cbe0d00b33bcaa58`.

## Limitations

- PCB is included as a mesh in GLB and FreeCAD documents. BREP-only STEP does not carry the PCB tessellation.
- FreeCAD macro syntax checked only. No native FreeCAD recompute or FCStd artifacts generated yet.
- USB4105 visual BREP is family-level. Exact suffix, official ordered STEP and physical plug depth/clearance remain unconfirmed.
- No printing, wall mounting pull-out, heat, gas-response, ingress or cable harness test performed.

## OneDrive

Folder: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s43e86e3cd2554478a3df742657a181a8  
ZIP: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sc21342f6d56843a29c551f0a3fd855f6  
GLB: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sf8263a6cc1934c44b4296f94f10a0ed3  
FreeCAD macro: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s0bb718d2d183470cbba71423e23361e1
