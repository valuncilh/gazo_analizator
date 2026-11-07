# Rev5 baseline audit

## Git status

- The repository exposes `analysis/vendor-behavioral-reconciliation` as its only pre-existing branch.
- A branch named `main` was not found via the GitHub branches endpoint. The repository default branch at audit time is `analysis/vendor-behavioral-reconciliation`.
- Rev5 therefore branches from the confirmed commit `4451222a416302e97e1f25da4e60df7309f7445f`. No change is made to the pre-existing engineering branch.
- A separate branch named `design/usb-c-pcb-enclosure-r5` is used for all Rev5 work.

## Candidate PCB sources

### Uploaded `gazo_e3_E3_DRC2_repaired.kicad_pcb`

- SHA-256: `7d23d409f29a3627a06ecf123a1a57aed42e19d11c28d353dcdcfeff2c70a246`
- 23 footprints.
- 207 track segments.
- 21 vias.
- 5 zones.
- Four M2 NPTH holes at (172, 127.5), (224, 127.5), (172, 164.5), (224, 164.5) mm.
- Outline 59 × 45 mm, X = 168.5…227.5 mm, Y = 123.5…168.5 mm.
- XS1 is on the same short edge as A1. It must be removed from the power-input role.

### Uploaded `gazo_e3_implementation(8).kicad_pcb`

- SHA-256: `f9cd9797df03fe79267c0c57c1f98b4729e2b27080316102dd9fbbdb9b510e9d`
- 23 footprints.
- Same 59 × 45 mm outline and same four-hole pattern in a local coordinate frame.
- This file contains no route segments, vias, or copper zones. It is a placement/geometry reference, not the routed PCB master.

### Existing DRC2 report

- The supplied DRC2 repair report documents 20 original violations, including solder-mask bridges/shorts at A1 and XS1, silkscreen conflicts, two unconnected pads, a dangling track warning, and library mismatch/configuration warnings.
- The report explicitly states that native KiCad DRC was not rerun after the static repairs and that zones were not refilled in KiCad. This project will not label the board as DRC PASS until a native DRC run is performed.

## USB-C candidate

The selected connector candidate is GCT USB4105, top-mount, horizontal, 16-pin. Manufacturer drawing: https://gct.co/files/drawings/usb4105.pdf

The drawing identifies the recommended PCB layout tolerance as ±0.05 mm, the shell stake slots, signal pad pitch/lengths, PCB-edge datum, and the VBUS/GND/CC pin assignments. Exact footprint geometry must be used, not a hand-drawn approximation.

## Constraint warning

The M2 mounting locations, board dimensions, A1 placement, and existing routed geometry are treated as fixed until the next design review. Component movement will be limited to what is necessary to fit the USB-C power input and associated support circuitry. Any move must be checked against pad, courtyard, copper, silkscreen, and 3D envelopes.
