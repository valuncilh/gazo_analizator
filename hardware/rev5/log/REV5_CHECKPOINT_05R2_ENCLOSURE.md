# Rev5 checkpoint 05R2 — Variant B Turtle enclosure adapted to Stage04R2

Date: 2026-11-07  
Branch: `design/rev5-stage05r2-usbc-long-edge`  
Source: Stage04R2 long-edge USB-C PCB

## Completed

- Promoted Stage04R2 as the active PCB baseline after discovering it was newer than the Stage04R1/Stage05R1 continuation.
- Preserved Stage04R2 PCB and schematic as immutable source files in OneDrive.
- Reused the existing Variant B Turtle R3 enclosure instead of designing a new enclosure from scratch.
- Reconciled 22 shared footprint origins/rotations against the old board reference: 22/22 match after coordinate transform; max position delta ≈2.01e-14 mm.
- Built a new provisional PCB mechanical STEP reference by reusing the old user-supplied 59×45 board STEP, removing obsolete XS1 solid and adding simplified J1/R8/R9 envelopes. This is not a native KiCad STEP export.
- Adapted USB-C to the +X long case wall, separate from A1; removed obsolete nose cable inlet, XS1 access divider and floor cable channel.
- Preserved the R3 lid, M2 bosses, brackets, wall-mount ears, sensor support rails and MQ-4 side vent geometry.
- Generated STEP/STL parts and open/closed/exploded assemblies, review drawings, validation reports, scripts and FreeCAD import macro.

## Geometry values

- PCB: 59×45×1.6 mm; case-oriented projection 45×59 mm; board bottom Z=6.4 mm.
- Four M2 holes preserved, 52×37 mm pitch.
- USB aperture 9.8×4.2 mm, bezel 12×6.4 mm, 9.2 mm tunnel; centre at Y=33.0 mm/Z=9.565 mm on +X wall.
- Nominal mating-face-to-inner-wall gap 3.05 mm from simplified connector envelope.
- MQ-4 side-vent geometric area 515.2 mm²; openings remain unblocked in the current geometry.

## Checks performed

- 34/34 CadQuery/OpenCascade geometry checks PASS.
- 4/4 STL mesh topology checks PASS (watertight, consistent winding, one connected component).
- Simplified PCB STEP round-trip valid, 21 solids.
- STEP assembly re-import valid; housing compound 4 solids, full assembly 33 solids.

## Artifacts

- OneDrive Stage05R2: https://1drv.ms/f/c/24fda6920aa8c92a/IgDPFgSptzpLQJyZHScUdd5oASWy8KHSvaSuY83UYVDvcps
- ZIP SHA-256: `d193ba3e0f0099174fef39ea11ab826372ee4247ced9bd35d95b780c029e4f61`
- Manifest SHA-256: `b79d40b15dc7898bb8f23b7d16f8899195b2ae7e1a1dae9565abdd22ed6ade3c`

## Not done

- Native KiCad Refill/ERC/DRC/3D Viewer.
- Exact USB4105 supplier model or physical plug fit.
- Native KiCad PCB STEP export.
- Native FreeCAD recompute or FCStd output. FreeCAD runtime was unavailable; an import macro is provided.
- Printing, physical assembly, gas response, sensor thermal and other hardware tests.

## Next action

Verify exact USB4105 geometry, complete native KiCad checks/export, replace the simplified PCB reference with native KiCad STEP, run the FreeCAD macro/recompute/save FCStd, then inspect mechanical fit. Preserve the MQ-4 gas-exchange path. Schematic research remains independent; any electrical change must propagate to PCB and case.

**Status:** preliminary mechanical design candidate, not a manufacturing release.