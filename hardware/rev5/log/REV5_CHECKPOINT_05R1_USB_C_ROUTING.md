# Rev5 checkpoint 05R1 — USB-C copper routing candidate

Date: 2026-11-07  
Branch: `design/rev5-stage05-usbc-routing-r1`  
Source: Stage04R1 USB-C power-input replacement

## Completed

- Preserved the Stage04R1 PCB and the later standalone Stage04 schematic snapshot.
- Rotated R8/R9 by 180° with pad numbering and electrical nets unchanged.
- Added 11 F.Cu segments for CC1, CC2, the second VBUS pad pair and USB-C Earth returns.
- Added two Earth vias located inside the existing B.Cu Earth zone polygon.
- Preserved 207 source track segments and 21 source vias. Stage05 has 218 track segments and 23 vias.
- Created an editable PCB, builder scripts, static audit, net assignment table, overview/detail drawings and package ZIP in OneDrive.

## Artifact references

- OneDrive folder: https://1drv.ms/f/c/24fda6920aa8c92a/IgAgXbcAlTe0QL9uANXJdqSpATBVvYnUDeqEwvsW4NEXSsY
- Stage05 ZIP: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sec5ba7e03c40486783deb16d01dd8787
- Updated ZIP SHA-256: `30439da1fbe47a807b26c77a37506e4f62faed7b742fa2b26f9600cef810dd52`
- Output PCB SHA-256: `3104cb4586c7380c1fde19ac9c895258d0de1e725fa75c4b5ec246cc6ac284f9`

## Checks actually performed

- S-expression structural parse.
- Footprint/reference and UUID uniqueness.
- USB-C and R8/R9 pad-to-net assignments.
- VBUS route termination on an existing `/VCC` track endpoint.
- Earth via containment in the B.Cu Earth zone polygon.
- Source-level foreign-net track, segment-pair, pad and via clearance checks.
- A separate via-to-foreign-pad and via-to-foreign-via check. Both new Earth vias returned zero flags below 0.20 mm.
- SHA-256 manifest and ZIP integrity.

## Not done

- Native KiCad ERC/DRC and zone refill.
- KiCad 3D Viewer inspection.
- STEP export or FreeCAD enclosure fit.
- Final load-current qualification and USB-C current-source negotiation.
- Fuse/PTC/TVS/current-limit part selection.

## Next action

Use KiCad 10.0.7 to refill zones and run ERC/DRC, inspect 3D connector fit and the two new Earth vias. Then establish the exact load envelope and USB source class before selecting protection. Freeze PCB before exporting STEP and adapting the existing enclosure. Keep the MQ-4 sensor gas-exchange opening unobstructed.

**Status:** source-level routing candidate; not a fabrication release.