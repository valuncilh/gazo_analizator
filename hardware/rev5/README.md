# E3 Rev5 — USB-C PCB and enclosure redesign

**Branch:** `design/usb-c-pcb-enclosure-r5`  
**Base commit:** `4451222a416302e97e1f25da4e60df7309f7445f`  
**Status:** design in progress. Not released for fabrication.

## Design intent

- Replace the 2-pin power connector XS1 with a USB Type-C receptacle used only as a 5 V power input.
- Put the USB-C connector at the short PCB edge opposite sensor connector A1. Keep A1 as the sensor interface.
- Keep the PCB at 59 × 45 × 1.6 mm unless a mechanical/electrical conflict proves that a board outline change is unavoidable.
- Preserve the four M2 mounting holes and their exact 52 × 37 mm pattern.
- Keep the board two-layer and retain existing functional circuitry, topology, and reference designators where practical.
- Design the case only after the PCB outline, connectors, screw coordinates, and component keep-outs have been frozen.
- Retain Variant B Turtle external form and design a simple, accessible FreeCAD model around the final PCB and USB-C connector.
- Use a single full-size lid fixed by four corner fasteners. Do not create side-wall slots or cutouts for the lid. The enclosure side walls must remain continuous except for intentional interfaces and ventilation.
- Put USB-C on a separate case side from the sensor connector.

## Source-of-truth inputs

1. `gazo_e3_E3_DRC2_repaired.kicad_pcb` uploaded by the user. This is the best available routed PCB base. It contains 23 footprints, 207 track segments, 21 vias, and 5 zones.
2. `gazo_e3_implementation(8).kicad_pcb` and the original-coordinate PCB STEP are geometry references. They confirm the 59 × 45 mm outline and M2 pattern, but the KiCad reference file is not a fully routed PCB.
3. `gazo_e3_implementation(2).kicad_sch` is the current uploaded schematic candidate. It must be reconciled with the selected routed PCB and new USB-C input.
4. Variant B Turtle R3 is a mechanical precedent only. Its external outline and PCB/sensor layout are references, not the final Rev5 enclosure.

## Confirmed mechanical datums

- PCB outline: X = 168.5…227.5 mm, Y = 123.5…168.5 mm in the routed DRC2 source coordinate frame.
- PCB thickness: 1.6 mm.
- Holes: MH1 (172.0, 127.5), MH2 (224.0, 127.5), MH3 (172.0, 164.5), MH4 (224.0, 164.5) mm.
- Hole diameter: Ø2.2 mm, NPTH.
- Hole pattern: 52.0 × 37.0 mm.
- A1: (173.0, 140.0), currently on the left short edge.
- XS1: (173.0, 151.21), the power connector to be removed.
- USB-C candidate: GCT USB4105 top-mount horizontal receptacle on the opposite short edge, with PCB-edge alignment derived from the manufacturer footprint and drawing. Final coordinate and orientation are pending pad/courtyard/3D verification.

## Electrical intent

USB-C is a sink-only 5 V input, not a data port. VBUS pins are paralleled to the existing `/VCC` rail. All GND pins and shield are connected to `Earth`. CC1 and CC2 each receive an independent Rd = 5.1 kΩ to `Earth`. D+/D− and SBU pins remain unconnected and are documented as such. Input protection and current limiting must be checked against measured/expected load before release.

## Validation policy

Do not claim native KiCad DRC PASS unless KiCad 10 DRC has actually been run on the saved board with zones refilled. Static geometry/net/track checks are supplemental and must be reported separately. Do not hide or exclude DRC violations merely to obtain a clean report.

Before release, validate:
- schematic ↔ PCB parity and net connectivity
- full USB4105 recommended land pattern and shell stakes
- board outline and copper clearances
- all routing and via clearances
- solder-mask bridge clearances
- THT drill/pad and courtyard clearances
- silkscreen-to-mask and silkscreen-to-courtyard clearance
- unconnected items and dangling tracks
- filled zones and connectivity after refill
- 3D fit of USB-C plug shell and case aperture
- M2 hole table and case boss centers
- STEP/FreeCAD import and final enclosure interference checks

## Next steps

1. Complete the PCB baseline audit and determine the exact VBUS, GND, CC, and existing XS1 trace topology.
2. Replace XS1 with USB-C and add the two CC pull-down resistors. Add required VBUS protection based on the circuit load.
3. Update the schematic and PCB together. Preserve all unrelated nets and the existing M2 pattern.
4. Re-route and verify the whole PCB. Produce the final coordinate/hole schedule.
5. Freeze the PCB and export an authoritative PCB STEP.
6. Build the Rev5 FreeCAD enclosure around the final board and exact connector envelope.
7. Run final KiCad DRC and mechanical checks, package the source/STEP/STL/FCStd outputs, and update the engineering log.
