# Rev5 Stage 02R1 — USB4105 placement

Status: static placement proposal only. No copper rerouting or native DRC pass.

- Connector: GCT USB4105, horizontal top-mount, footprint origin X=198.000 mm, Y=127.175 mm, rotation 180°.
- Footprint PCB-edge datum local Y=+3.675 mm transforms exactly to global Y=123.500 mm.
- Board: 59 × 45 × 1.6 mm.
- Four M2 holes retained at (172,127.5), (224,127.5), (172,164.5), (224,164.5), Ø2.2 mm NPTH.
- R8/R9: 5.1 kΩ 0805 at (196.25,134.50) and (199.25,134.50), both rotation 90°. Pad 2 is upper and faces USB-C. R8.2 is CC2, R9.2 is CC1. Pad 1 is Earth.

USB-C is on a separate long board edge from A1. The geometrically opposite short edge is obstructed by the buzzer/LED courtyard corridor. The final case orientation must make the USB-C aperture a separate wall from the sensor/annunciator interface.

## Corrected geometry checks

The first Stage 02 calculation contained a duplicate transform in the 0805 courtyard template. Its clearance claims are superseded. Stage 02R1 fixes the transform. The original ZIP remains preserved in OneDrive as superseded.

- Courtyard collisions below 0.25 mm: 0.
- Minimum candidate courtyard clearance: 0.860 mm.
- R8 to R9: 1.050 mm.
- R9 to R6: 0.870 mm.
- R9 to R7: 1.071 mm.
- Existing tracks intersecting USB courtyard: 0.
- Existing F.Cu track clearance flags at USB pads: 0.
- Existing F.Cu track clearance flags at R8/R9 pads: 0.
- Existing tracks intersecting R8/R9 courtyards: 0.
- Drill schedule: 29 existing holes + 2 USB locator holes + 4 shell stake slots = 35 proposed features.

## Files

Complete generator, SVG/PNG review, JSON audit, CSVs and SHA-256 manifest:

[Open Stage 02R1 folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgBUjMa7o1GZRKMwXr-iLH4hASQkkyOK6vWCT9Bu4TfnNjM)

[Download Stage 02R1 ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQDAWMaNvP3mRa2qagX9FJv2ASr4eo9tBjtxCLmf4kpHgzo)

[Superseded initial Stage 02 ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQCw7H518QuNQLbxuy2AHctKAdab34OpDaGagY_4e76kk1E)

## Not done

The routed baseline PCB is unchanged. XS1 remains. The schematic, USB VBUS/GND/CC routes, native KiCad ERC/DRC, PCB STEP and FreeCAD case are not complete.

## Next

Create a new versioned PCB working copy. Add J1/R8/R9 while preserving the source. Reconcile the schematic and electrical nets. Complete USB power routing. Remove XS1 only from the new checked revision. Run native KiCad checks before starting the FreeCAD enclosure.
