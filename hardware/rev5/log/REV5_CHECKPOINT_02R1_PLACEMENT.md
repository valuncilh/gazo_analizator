# Rev5 engineering checkpoint 02R1 — USB-C placement and drill tables

Date: 2026-11-07
Branch: design/usb-c-pcb-enclosure-r5
Base before checkpoint: 36426250fdc21a7b042bfc1620defd7974e7bdaa

## Done

- Generated USB4105 placement proposal at (198.000,127.175), rotation 180°.
- Verified footprint PCB-edge datum transforms exactly to Y=123.500 mm.
- Preserved the 59 × 45 mm outline and all four M2 centers.
- Proposed R8/R9 5.1 kΩ 0805 CC pull-down positions.
- Corrected the Stage 02 courtyard calculation. The earlier generator translated local footprint geometry twice. The first calculation is superseded, but the original archive is retained in OneDrive.
- Recomputed courtyard clearances, candidate pad-to-track proximity, USB courtyard track intersections and resistor courtyard track intersections.
- Produced connector hole table and a merged 35-feature drill schedule.
- Verified all files in the Stage 02R1 SHA-256 manifest.
- Uploaded the full archive and individual outputs to OneDrive.

## Results

- Candidate courtyard collision pairs under 0.25 mm: 0.
- Minimum clearance: 0.860 mm, USB4105 courtyard to R8.
- R8/R9 courtyard clearance: 1.050 mm.
- R9/R6: 0.870 mm.
- R9/R7: 1.071 mm.
- Existing tracks intersecting USB courtyard: 0.
- Existing track clearance flags at USB signal pads: 0.
- Existing F.Cu track clearance flags at CC resistor pads: 0.
- Existing tracks intersecting R8/R9 courtyards: 0.
- Drill schedule: 29 baseline features + 2 NPTH locators + 4 plated shell stakes = 35.
- Four M2 holes remain unchanged at (172,127.5), (224,127.5), (172,164.5), (224,164.5) mm, Ø2.2 mm NPTH.

## Saved artifacts

GitHub:
- hardware/rev5/stage02_placement/README.md
- hardware/rev5/stage02_placement/USB4105_HOLE_TABLE_R5.csv
- This engineering checkpoint.

OneDrive folder:
https://1drv.ms/f/c/24fda6920aa8c92a/IgBUjMa7o1GZRKMwXr-iLH4hASQkkyOK6vWCT9Bu4TfnNjM

Complete Stage 02R1 ZIP:
https://1drv.ms/u/c/24fda6920aa8c92a/IQDAWMaNvP3mRa2qagX9FJv2ASr4eo9tBjtxCLmf4kpHgzo

Superseded first Stage 02 ZIP:
https://1drv.ms/u/c/24fda6920aa8c92a/IQCw7H518QuNQLbxuy2AHctKAdab34OpDaGagY_4e76kk1E

The OneDrive folder includes the script, JSON audit, SVG/PNG review drawing, baseline schedule, proposed combined drill schedule, SHA manifest and individual files.

## Not done

- No routed PCB was modified.
- XS1 remains in baseline.
- No USB-C schematic, VBUS/GND/CC copper routes or protection stage were added.
- No native KiCad ERC/DRC or zone refill was run.
- No PCB STEP or FreeCAD model was created.

## Next

1. Create a versioned PCB working copy and add USB4105 and R8/R9.
2. Reconcile USB-C symbol and footprint pad numbering, including shield pad SH.
3. Verify that the existing VCC rail is 5 V and determine sensor heater startup/steady current before sizing protection.
4. Route VBUS, GND and both CC paths. Remove XS1 only from the new revision after the replacement input path is checked.
5. Run KiCad 10 ERC/DRC and refill zones. Retain native reports.
6. Export a versioned PCB STEP, then build the enclosure in FreeCAD around the exact board and connector.
