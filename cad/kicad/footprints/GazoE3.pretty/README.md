# GazoE3 custom footprint library

This library contains two source-level footprints for the unchanged E3 netlist.

| Footprint | Pad mapping | Dimensions | Status |
|---|---|---|---|
| HCM1206X_P7.6mm | pad 1 = HA1.1, pad 2 = HA1.2 | body Ø12 x 9.5 mm, pitch 7.6 +/-0.2 mm, leads Ø0.6 mm | Dimensioned from the Ningbo Kepo OEM2690R drawing. Verify the plus mark and which lead is positive on the purchased lot. |
| NKK_AS11AP_SPST_P5.08mm | pad 1 = physical terminal 1, pad 2 = physical terminal 3 | terminal pitch 5.08 mm; body envelope approx. 9.0 × 8.8 mm; terminal 2 is absent on AS11 | Based on NKK Series AS dimensional drawing. Verify switch orientation and housing fit on sample. |

No 3D models are included. These footprints have not been opened in KiCad 10.0.7 and have not passed footprint DRC, PCB DRC, or a physical fit inspection. They are not approved for fabrication.

KT3102B deliberately has no custom footprint yet. The datasheet identifies a metal-glass package with flexible leads, but the exact lead coordinates/orientation must be measured from a sample or confirmed from a dimensioned production drawing. Do not reuse the old KT-26 / TO-92 footprint.
