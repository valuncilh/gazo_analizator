# Rev5 Stage05R1 — USB-C copper routing candidate

**Branch:** `design/rev5-stage05-usbc-routing-r1`  
**Status:** routed candidate. Not a fabrication release.

## OneDrive working package

- [Open MAI_GAZ_actor Stage05R1 folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgAgXbcAlTe0QL9uANXJdqSpATBVvYnUDeqEwvsW4NEXSsY)
- [Download Stage05R1 package ZIP](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sec5ba7e03c40486783deb16d01dd8787)
- Editable PCB: `gazo_e3_rev5_usb_c_power_R2_routed_candidate.kicad_pcb`
- Stage04R1 source PCB SHA-256: `78840a0598cb7c21e2f556c656f200bf174126a7d0d94fdd7e42a084c783e162`
- Stage05R1 output PCB SHA-256: `3104cb4586c7380c1fde19ac9c895258d0de1e725fa75c4b5ec246cc6ac284f9`
- Stage05R1 package ZIP SHA-256: `30439da1fbe47a807b26c77a37506e4f62faed7b742fa2b26f9600cef810dd52`

## Changes

- Rotated R8 and R9 by 180° while preserving pad numbers, values and nets. CC pad 2 faces J1; Earth pad 1 faces the B.Cu ground plane.
- Added 11 F.Cu segments and 2 Earth vias.
- Routed J1.A5 to R8.2 (CC1) and J1.B5 to R9.2 (CC2).
- Routed J1.A9/B4 to the existing `/VCC` trunk. The existing A4/B9 connection remains.
- Connected both USB-C ground pad pairs to nearby shell-stake pads and connected R8/R9 Earth pads to separate B.Cu vias.
- Preserved the Stage04 electrical topology; no schematic edits were made in this copper-only stage.

## Static results

- 25 footprints, no duplicate references.
- 904 UUIDs, no duplicates.
- 207 original track segments retained; 11 added (218 total).
- 21 original vias retained; 2 added (23 total).
- Relevant pad-to-net mappings, VBUS trunk endpoint and Earth-zone polygon containment checked.
- No source-level foreign-track, segment-pair, foreign-pad, via-to-foreign-pad or via-to-foreign-via clearance flags below 0.20 mm in the performed checks.
- A separate via-clearance script checks each new via against every foreign-net pad and existing via. Both new vias returned zero flags below 0.20 mm.

## Not done

- Native KiCad 10.0.7 Refill All Zones, ERC/DRC and 3D Viewer are not run.
- New Earth-via plane connectivity is intended but not confirmed until native zone refill.
- No input protection/current limiter chosen because exact SEN-MQ4-V2 total current remains unspecified in available product documentation.
- No 1.5 A/3 A USB-C current capability assumed from passive Rd alone.
- No new PCB STEP or FreeCAD enclosure update.

## Next

Open the Stage05 PCB in KiCad 10.0.7, refill zones, run native DRC/ERC, review connector orientation and ground-plane connectivity, then decide load current/source class and input protection. Freeze PCB before updating the Variant B Turtle enclosure. Keep the MQ-4 gas-exchange path open.

Binary CAD/EDA files are stored in OneDrive. This GitHub directory is the versioned text pointer, not a claim that the binary PCB is stored in Git.