# Rev5 Stage05R2 — Variant B enclosure adapted to Stage04R2 USB-C long-edge PCB

**Branch:** `design/rev5-stage05r2-usbc-long-edge`  
**Status:** preliminary mechanical CAD candidate. Not a fabrication release.

## OneDrive work package

- [Open MAI_GAZ_actor Stage05R2 folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgDPFgSptzpLQJyZHScUdd5oASWy8KHSvaSuY83UYVDvcps)
- Package ZIP: `Gazo_E3_Rev5_Stage05R2_USB_C_Long_Edge_Enclosure.zip`
- ZIP SHA-256: `c3f30d029f9ea571c3d5b0b1def44688390c210f19110d0d646f1067e1874bbf`
- SHA manifest: `SHA256SUMS_STAGE05R2.txt` (94 source/deliverable file hashes)
- Manifest SHA-256: `b79d40b15dc7898bb8f23b7d16f8899195b2ae7e1a1dae9565abdd22ed6ade3c`

## Source baseline

- PCB: Stage04R2 `gazo_e3_rev5_usb_c_power_R2.kicad_pcb`
- PCB SHA-256: `4aed2951d60049d60ea458a58818b156909e0ff416e0e592e7b0da4ce62fe0b0`
- Schematic SHA-256: `f4ecc00b30d8aa52d9f21f3e29bafa825ae219cdc2f13c8c2dc7e27aa8bacd5d`
- Existing enclosure source: Variant B Turtle R3. No new independent case concept was created.

## Mechanical changes

- Adapted the existing Variant B Turtle R3 case to the Stage04R2 long-edge USB-C orientation.
- USB-C exits the +X long wall, separate from A1 sensor connector side.
- Removed obsolete nose/front power-cable inlet, XS1 access divider and floor cable channel.
- Preserved common lid, four M2 bosses, corner brackets, wall-mount ears, sensor rails and MQ-4 chamber side ventilation.
- Provisional USB opening: 9.8×4.2 mm, 12×6.4 mm bezel, 9.2 mm tunnel. Nominal mating-face-to-inner-wall gap 3.05 mm from simplified connector envelope.
- Retained an open gas-exchange path around the Joy-IT SEN-MQ4-V2 sensing element. Vent area is a geometric estimate only; no gas-response performance is claimed.

## Generated files

- STEP/STL: integrated base, common lid, left/right sensor supports.
- STEP: open, closed and exploded assemblies, plus simplified PCB and sensor reference models.
- FreeCAD import macro: `cad/freecad/Import_Stage05R2_VariantB.FCMacro`.
- CadQuery source, mechanical views, reports, renders, checkpoint, recovery notes and SHA manifest.

## Checks actually performed

- 22/22 common footprint origin/rotation alignments between prior case board reference and Stage04R2 after coordinate transform (maximum position delta about 2.01e-14 mm).
- Simplified PCB STEP round-trip: 21 valid solids. It is not a native KiCad STEP export.
- CadQuery/OpenCascade enclosure geometry checks: 34/34 PASS.
- STEP assembly re-import: housing compound 4 solids; full assembly 33 solids.
- STL topology: 4/4 PASS — watertight, consistent winding, one connected component.

## Not done / limitations

- Exact GCT USB4105 supplier STEP or physical connector/plug check is still required. The current connector body is a simplified envelope; the aperture remains provisional.
- Native KiCad 10.0.7 Refill All Zones, ERC/DRC and 3D Viewer are not run.
- No native PCB STEP export.
- FreeCAD runtime was unavailable; no `.FCStd` files are claimed. The macro creates documents on FreeCAD 1.1.x.
- Internal SEN-MQ4-V2 sensor/Molex positions remain estimates. The outer 41×25×21 mm module envelope is documented.
- No printing, physical assembly, sensor gas-response, temperature, IP, vibration or acoustic tests.

## Next

1. Verify exact USB4105 model/plug fit and update the aperture/tunnel.
2. Complete native KiCad checks and export native PCB STEP.
3. Replace simplified PCB reference, run FreeCAD macro/recompute/save FCStd and inspect fits.
4. Continue independent schematic architecture redesign research, including Russian component candidates. Any electrical change must propagate schematic → PCB → STEP → enclosure.
5. Keep the MQ-4 gas-exchange path open.

Binary CAD/EDA files are stored in OneDrive. This GitHub folder is the versioned pointer/checkpoint, not a claim that binary project files are committed to Git.
## Exact USB4105 3D model integration

The OneDrive package also includes `cad/freecad/Import_Stage05R2_VariantB_ExactUSB.FCMacro` and `README_FREECAD_EXACT_USB.md`. The macro searches the installed official KiCad 3D library for `USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.step` and replaces the one known simplified J1 body only when exactly one envelope match exists. Otherwise it explicitly retains the simplified fallback.

- [ExactUSB FreeCAD macro in OneDrive](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s899718b29019442fb2fddba1b8dda7f0)
- [ExactUSB macro README in OneDrive](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s59b4ce9cb84f4a2ea24cd6405d85ca08)
- [USB4105 model provenance note](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s08fe1ff39f8b4f7297f0160a4e26978c)

The exact model macro has **not** been executed in FreeCAD in this environment. The exact J1 STEP import, BREP recompute, USB wall/aperture match and physical plug clearance remain pending on a machine with FreeCAD 1.1.x and the KiCad 3D library installed. Do not treat the case aperture as frozen.