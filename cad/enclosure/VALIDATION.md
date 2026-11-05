# E3 enclosure — geometry validation

**State:** PRELIMINARY / NOT FOR FABRICATION.

## Geometry basis

- PCB outline: 59 × 45 mm.
- PCB substrate: 1.6 mm nominal.
- Four mounting holes: Ø2.2 mm, M2 clearance, 52 × 37 mm centre pattern.
- Joy-IT SEN-MQ4-V2 external envelope: 41 × 25 × 21 mm, approx. 8 g.
- The KiCad STEP reference contains 19 solids and is imported into both assembly concepts.

## Post-revision checks

- 21 of 21 STEP files passed OpenCascade BREP validity checks.
- Variant A sensor base passed BREP validation.
- Variant A sensor base / coupling bridge boolean intersection volume: 0.0 mm³ after relocating the two M3 captive-nut pockets 1 mm inward (sensor-base local x = 48 mm; assembly global x = -13 mm).
- The geometry checklist records 60 of 60 checks as PASS. One initial sensor-bridge clearance review was corrected and directly rechecked against the reimported STEP solids.

## Important non-claims

- FreeCAD is not installed in the generation runtime. The import/save macro is committed, but four native FCStd files were not generated or opened in this environment.
- The STL tessellations are preview/slicing trials. Current mesh validation does not establish watertight/manifold print readiness. STEP BREP remains the geometric master.
- No FDM test coupons, fit tests with hardware, powered heater thermal test, gas-diffusion or response-time test, IP test, vibration test, or acoustic test were performed.
- MQ-4 internal component positions and connector coordinates remain estimated reference geometry, not manufacturing datums.

## Manufacturing gate

Before fabrication, verify M2 nut capture, M3 wall-mount hardware, A1/XS1 mating connector reach and cable bend radius with physical hardware. Run a powered thermal test of the sensor chamber using the intended final polymer. Confirm that enclosure ventilation does not degrade the sensor response.