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

## Immutable source baseline

The original PCB, schematic, board STEP, DRC reports, repair patch, and previous enclosure/sensor packages have been archived without modification.

- [Open immutable baseline folder on OneDrive](https://1drv.ms/f/c/24fda6920aa8c92a/IgAnVFgpfc9WQK9nWuSqdRp3AbaSeJAc8tlWTGNKwYewT6k)
- [Download complete immutable baseline ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQBHREov1F1bSay7DkcBEFrQAWv0sY4f9sOWANQYgvgHAPk)

The folder also contains individual source files and `SHA256SUMS.txt`. Do not overwrite or delete these inputs. The mandatory rule is documented in [SOURCE_PRESERVATION_POLICY.md](SOURCE_PRESERVATION_POLICY.md).

## Source-of-truth inputs

1. `gazo_e3_E3_DRC2_repaired.kicad_pcb` — routed PCB candidate, 23 footprints, 207 track segments, 21 vias, 5 copper zones.
2. `gazo_e3_implementation(8).kicad_pcb` — second PCB snapshot and placement geometry reference, with the same outline and hole pattern but without routes/zones.
3. `gazo_e3_implementation(2).kicad_sch` — uploaded schematic candidate. It must be reconciled with the chosen routed PCB and the new USB-C input.
4. `gazo_e3_implementation.step` — previous PCB STEP export. This is an immutable mechanical reference, not a Rev5 export.
5. R3 Turtle and sensor packages — preserved references only. The Rev5 enclosure must be regenerated against the frozen Rev5 PCB STEP.

## Confirmed mechanical datums

- PCB outline in routed source coordinate frame: X = 168.5…227.5 mm, Y = 123.5…168.5 mm.
- PCB size: 59 × 45 mm. Thickness: 1.6 mm.
- Four mounting holes Ø2.2 mm, NPTH:
  - MH1: (172.0, 127.5) mm.
  - MH2: (224.0, 127.5) mm.
  - MH3: (172.0, 164.5) mm.
  - MH4: (224.0, 164.5) mm.
- Pattern: 52 × 37 mm.
- A1: (173.0, 140.0), rotation −90°, sensor interface.
- XS1: (173.0, 151.21), rotation −90°, old power input to be removed only from the new Rev5 working copy.

## Electrical intent

USB-C is a sink-only 5 V input, not a data port. VBUS pins are paralleled to the existing `/VCC` rail. GND pins and shield connect to the ground return. CC1 and CC2 each receive an independent Rd = 5.1 kΩ to ground. D+/D− and SBU pins remain unconnected and explicitly documented. Input protection and current limit must be checked against the actual load before release.

## Validation policy

Do not claim native KiCad DRC PASS unless KiCad DRC has actually been run on the saved project after zones are refilled. Static geometry/connectivity checks are supplemental and must be reported separately. Do not hide or exclude DRC violations merely to obtain a clean report.

Before release, validate:
- schematic ↔ PCB parity and net connectivity
- USB4105 manufacturer-recommended land pattern, shell stakes, pin map and 3D envelope
- board outline and copper clearances
- routing and via clearances
- solder-mask and silkscreen clearances
- THT drill/pad and courtyard clearances
- unconnected items and dangling tracks
- filled zones and connectivity after refill
- USB-C plug fit and case aperture
- M2 hole table and case boss centers
- STEP/FreeCAD import and enclosure interference checks

## Current checkpoint

- Done: branch created, source baseline archived, hashes recorded, source preservation policy committed.
- Not done: no new schematic, PCB, USB-C footprints or Rev5 FreeCAD outputs have been released yet.
- Next: audit the power net and XS1 connectivity, freeze the USB4105 footprint orientation and recommended land pattern, then update schematic and PCB in a separate versioned working copy.
- Environment note: KiCad CLI and FreeCAD are not installed in the current preparation environment. Native ERC/DRC and FreeCAD recompute are not being claimed.
