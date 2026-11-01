# E3 implementation project — isolated copy

**Status:** implementation scaffold / PRELIMINARY. This directory is separate from the immutable approved E3 source.

## Files

- `gazo_e3_implementation.kicad_sch` — copy of the approved E3 schematic with candidate physical footprints assigned in instance fields. Electrical topology, values, references, pins and nets are unchanged.
- `fp-lib-table` — project-local GazoE3 library path, resolved relative to this directory.
- `reports/e3_pad_net_map.csv` — 47 pin-to-net assignments derived from the approved XML-netlist.
- `reports/footprint_assignment_status.csv` — reference-level candidate status and restrictions.

## Footprint assignments

All 19 E3 references have a candidate footprint assignment. These are engineering candidates, not fabrication approval.

| Reference | Candidate footprint | Restriction |
|---|---|---|
| A1 | Molex PicoBlade 53261-0471 1x04 | Physical mapping of Molex pin 1 to sensor VCC/DOUT/AOUT/GND remains TBC. |
| C1, C3 | CP_Radial_D5.0mm_P2.00mm | Verify symbol polarity and mounting dimensions from the component drawing. |
| C2 | C_0805_2012Metric | Standard 0805 candidate. |
| DA1 | DIP-8_W7.62mm | TI NE555P PDIP-8 candidate. Approved symbol graphic remains NE555D. Verify pin-function parity in KiCad. |
| HA1 | GazoE3:HCM1206X_P7.6mm | Body dimensions documented. Positive physical lead remains TBC. |
| HL1, HL2 | LED_D5.0mm | Pad 1=cathode according to the symbol. Verify candidate MPN drawings. |
| R1–R7 | R_0805_2012Metric | 0805 candidates. Verify dissipation and current separately. |
| SA1 | GazoE3:NKK_AS11AP_SPST_P5.08mm | Pad 1/2 map to physical terminals 1/3. Actuator orientation remains a CAD enclosure constraint. |
| VD1 | D_DO-35_SOD27_P7.62mm_Horizontal | Pad 1=K, pad 2=A. Close dimensional candidate for KD510A. |
| VT1 | GazoE3:KT3102B_KT1-7_DWG_DRAFT | Drawing-derived draft. Pad 1=B, 2=C, 3=E. Upper-view coordinate interpretation remains TBC. |
| XS1 | Molex PicoBlade 53261-0271 1x02 | Pin 1=/VCC and pin 2=Earth per approved E3. Cable orientation remains TBC. |

## Immutable baseline

- Approved schematic Git blob SHA: `2e17299ba8a9aeeb0ce5e6c06562fe4e0fd84ba0`.
- Approved XML-netlist Git blob SHA: `b24384b2e1b39068b3a11c9e11554cd4dc406b57`.
- Expected topology: 19 components, 15 nets, 47 connected pins.

Do not edit the approved source schematic, XML-netlist or approved baseline to assign or refine implementation footprints. All further changes belong in this isolated implementation copy.

## Validation state

- Candidate footprint properties are present for all 19 references in this copy.
- Topology is inherited from the immutable approved schematic; native KiCad symbol-to-board netlist parity has not yet been run.
- KiCad 10 native validation, footprint checks and PCB DRC are pending. This remote editing session cannot execute the user's local KiCad 10.0.7 GUI/CLI.
- No PCB outline, placement, routing or manufacturing exports are created yet.
- No physical fit, assembly or laboratory validation is claimed.

## Next gate

Open the schematic in KiCad 10.0.7, confirm that the project-local `GazoE3` library resolves, run ERC and export a fresh XML netlist. Compare the exported topology with the immutable approved XML before creating or editing a board. Then create the dedicated `.kicad_pro` and `.kicad_pcb` files in this directory.
