# E3 implementation project — isolated copy

**Status:** implementation scaffold / PRELIMINARY. This directory is separate from the immutable approved E3 source.

## Files

- `gazo_e3_implementation.kicad_sch` — copy of the approved E3 schematic with candidate physical footprints assigned in instance fields. Electrical topology, values, references, pins and nets are unchanged.
- `fp-lib-table` — project-local GazoE3 library path, resolved relative to this directory.
- `reports/e3_pad_net_map.csv` — 47 pin-to-net assignments derived from the approved XML-netlist.
- `reports/footprint_assignment_status.csv` — reference-level candidate status and restrictions.
- `reports/implementation_scaffold_validation.md` — source-content validation results and limitations.

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
| VD1 | D_DO-35_SOD27_P7.62mm_Horizontal | SELECTED candidate for KД-2 package. Pad 1=K, pad 2=A. KiCad 10 footprint validation remains pending. |
| VT1 | GazoE3:KT3102B_KT1-7_DWG_DRAFT | Drawing-derived draft. Pad 1=B, 2=C, 3=E. Upper-view coordinate interpretation remains TBC. |
| XS1 | Molex PicoBlade 53261-0271 1x02 | Pin 1=/VCC and pin 2=Earth per approved E3. Cable orientation remains TBC. |

## Immutable baseline

- Approved schematic Git blob SHA: `2e17299ba8a9aeeb0ce5e6c06562fe4e0fd84ba0`.
- Approved XML-netlist Git blob SHA: `b24384b2e1b39068b3a11c9e11554cd4dc406b57`.
- Expected topology: 19 components, 15 nets, 47 connected pins.

Do not edit the approved source schematic, XML-netlist or approved baseline to assign or refine implementation footprints. All further changes belong in this isolated implementation copy.

## Reproducible source-level check

From the repository root run:

```fish
python3 cad/scripts/verify_e3_implementation.py
```

The checker verifies the immutable source blob IDs, reversible-copy relationship, 19 footprint assignments, 47 pad-to-net rows and protected E3 nets. It does not run KiCad itself.

## Validation state

- Candidate footprint properties are present for all 19 references in this copy.
- Topology is inherited from the immutable approved schematic; native KiCad symbol-to-board netlist parity has not yet been run.
- KiCad 10 native validation, footprint checks and PCB DRC are pending. This remote editing session cannot execute the user's local KiCad 10.0.7 GUI/CLI.
- No PCB outline, placement, routing or manufacturing exports are created yet.
- No physical fit, assembly or laboratory validation is claimed.

## Local KiCad 10.0.7 acceptance gate

The next gate is deliberately local because the remote source-content checker cannot execute the user's KiCad installation.

1. Update the working branch locally. Do not create or restore `main`.
2. Open `gazo_e3_implementation.kicad_sch` in Eeschema. Confirm the schematic opens without missing symbols and inspect the project-local `GazoE3` footprint library path. The footprint table is `fp-lib-table` in this directory.
3. Run ERC and export a fresh XML-netlist using the KiCad 10 CLI.
4. Compare the fresh XML with the immutable approved netlist using the parity checker below.
5. Send the ERC report and parity output for review. Do not create or edit a PCB until topology parity is confirmed.

From the repository root, fish-compatible commands:

```fish
git fetch origin
git switch analysis/vendor-behavioral-reconciliation
git pull --ff-only origin analysis/vendor-behavioral-reconciliation

python3 cad/scripts/verify_e3_implementation.py

mkdir -p cad/kicad/e3_project/reports/local

kicad-cli version

kicad-cli sch erc --severity-all \
  --output cad/kicad/e3_project/reports/local/implementation_erc.rpt \
  cad/kicad/e3_project/gazo_e3_implementation.kicad_sch

kicad-cli sch export netlist --format kicadxml \
  --output cad/kicad/e3_project/reports/local/implementation_fresh.xml \
  cad/kicad/e3_project/gazo_e3_implementation.kicad_sch

python3 cad/scripts/compare_e3_netlists.py \
  --candidate cad/kicad/e3_project/reports/local/implementation_fresh.xml

python3 cad/scripts/compare_e3_netlists.py \
  --candidate cad/kicad/e3_project/reports/local/implementation_fresh.xml \
  --require-footprints
```

The first comparison checks the 19 component references/values, all 15 nets and 47 connected pins, plus the protected `/AOUT` and `Net-(SA1-B)` connections. The second also requires a non-empty Footprint field for all 19 components. If the second check reports missing footprint fields, keep the topology result separate and send the XML for investigation.

**ERC is a report, not an automatic pass/fail command here.** The command intentionally omits `--exit-code-violations`, so warnings can be reviewed without treating every warning as a shell failure. Do not suppress warnings or alter the approved schematic to make the report clean.

KiCad 10 CLI syntax is documented in the [official KiCad 10 reference](https://docs.kicad.org/10.0/en/cli/cli.html). ERC usage is `kicad-cli sch erc`; XML export uses `kicad-cli sch export netlist --format kicadxml`.

Do not create `.kicad_pro` or `.kicad_pcb` files yet. They are the next remote CAD step only after the local gate confirms schematic loading, library resolution, ERC review and XML parity.
