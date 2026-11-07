# USB4105 reference geometry and pin map

## Authoritative mechanical source

Manufacturer product page: https://gct.co/connector/usb4105
Manufacturer drawing, revision B4 (18 Dec 2023): https://gct.co/files/drawings/usb4105.pdf

USB4105 is an active 16-contact USB Type-C 2.0 receptacle, SMT, top-mounted, horizontal, side-entry. Product page identifies 5 A collective VBUS rating, 6.25 A collective GND rating, 20,000 mating cycles, profile 3.31 mm, locating pegs, and through-hole shell stakes. These are connector ratings, not the board's approved operating current.

## Drawing dimensions relevant to PCB/CAD

- Drawing page 1, recommended PCB layout, component-side view, tolerance ±0.05 mm.
- Contact row uses 16 pads with duplicated A/B pairs for VBUS and GND.
- The four shield shell-stake pads are plated through-hole oval slots.
- Two additional Ø0.65 mm locating holes/pegs are present.
- The footprint's PCB-edge datum is explicitly marked. Align that datum to the actual PCB Edge.Cuts line, not to the footprint origin.
- Drawing body width 8.94 mm and height/profile 3.31 mm. Mating-side height 7.35 mm. Actual shape must be taken from the 3D model / STEP, not simplified to these two dimensions.
- Drawing provides 4×0.60 mm and 4×1.00 mm mechanical slot dimensions, 2×Ø0.65 mm locating features, 16×0.20 mm contact pattern and related dimensions. See the drawing directly for complete tolerances.

## Pin assignment from GCT drawing

| Contact | Signal | PCB function |
|---|---|---|
| A4, A9, B4, B9 | VBUS | Tie together to board +5V input after protection |
| A1, A12, B1, B12 | GND | Tie to board ground return |
| A5 | CC1 | Separate Rd = 5.1 kΩ to ground |
| B5 | CC2 | Separate Rd = 5.1 kΩ to ground |
| A6, B6 | D+ | Unused for power-only revision, no-connect |
| A7, B7 | D− | Unused for power-only revision, no-connect |
| A8 | SBU1 | Unused, no-connect |
| B8 | SBU2 | Unused, no-connect |
| SHELL | Shield | Chassis/ground strategy to be documented. Candidate tie to ground by direct or RC/0Ω link only after reviewing EMC and existing ground reference. |

## Placement datum and orientation proposal

The PCB's A1 sensor connector is at the left short edge. USB-C is to be mounted at the opposite short edge, x = 227.5 mm, with its mating face outward. The KiCad footprint's local `PCB Edge` datum is at local y = +3.10 mm. A proposed footprint rotation of −90° maps that local edge datum to the right board edge. The candidate footprint origin therefore has x = 224.40 mm. The final Y coordinate is not frozen until full courtyard, 3D shell, buzzer, LED, switch, mounting-hole and screw-head checks are complete.

## Reference files stored in this branch

- `USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.kicad_mod` — KiCad footprint source from a versioned mirror of the KiCad library. Validate against the manufacturer's drawing before use.
- `USB_C_Receptacle_GCT_USB4105.step.STEP` — third-party CAD copy of the GCT connector referenced by the source repository. It is a geometry reference, not a manufacturer-issued certified model. Cross-check it against the GCT drawing and physical sample.

## Electrical cautions

- USB-C is a sink-only 5 V power input. There is no USB data functionality.
- CC1 and CC2 each need their own Rd. Do not join CC1 and CC2 together.
- Simple Rd resistors establish the sink advertisement but do not protect VBUS against overvoltage, ESD, or overcurrent. Protection and current limit must be selected for the board load, including sensor heater inrush/warm-up current.
- Before release, measure/confirm maximum current draw at start-up and steady state and check voltage drop through the connector, protection, copper and cable.

## Verification status

Footprint and source STEP have been added to the reference directory. The connector is **not yet placed in the routed board**. Its final position, 3D fit and electrical integration remain pending. No DRC or mechanical pass is claimed.
