# Project modification schematic reference

## Purpose and design boundary

This is the independent project version, based on the Original 2022 reference but modified for the course project. The controlled gas is CH₄; target alarm setting is 1000 ppm; nominal supply is 5.0 ±0.1 V DC and the whole-device current limit is 300 mA. The original schematic remains unchanged in `cad/original_2022/` and its threshold is 4400 ppm.

## Engineering changes

| Change | Reason and basis | Status / limitation |
|---|---|---|
| A1 provisionally identified as Joy-IT SEN-MQ4 V1 | Manufacturer documents 5 V, AO/DO, an adjustable threshold range including 1000 ppm and heater current up to 180 mA; family guidance describes active-low DOUT | Exact V1 revision, output stage, pull-up, DOUT polarity for V1 and total module current are not confirmed. A1 pin numbers below are abstract KiCad symbol numbers, not a physical pinout. No footprint is assigned. |
| Threshold target set to 1000 ppm CH₄ | Project requirement, separate from Original 2022's 4400 ppm | The published adjustment range includes the target but does not establish accuracy/calibration at that point. Gas calibration is unverified. |
| C1 changed from 4.7 µF to 47 µF | With R4=R5=8.2 kΩ, the 555 estimate becomes about 1.25 Hz, within the publication's stated 1–2 Hz range | Independent project timing choice, not a correction to Original 2022. Estimate uses `f≈1/[0.693·(R4+2R5)·C1]`; no component tolerances or 555 dynamic limits are included. |
| Remaining discrete values/topology retained provisionally | Reuses the source architecture for a separate working design | Must be checked for 4.9/5.1 V, output loads, full current and selected part limits. This schematic is not an approved PCB input. |

## Conditional KiCad pin inventory

The connector's 1=VCC, 2=DOUT, 3=NC, 4=GND mapping is a logical abstraction only. It must not be used to wire a physical Joy-IT board without a revision-specific manufacturer pinout.

| Reference | Pin numbers |
|---|---|
| A1 | 1, 2, 3, 4 |
| C1 | 1, 2 |
| C2 | 1, 2 |
| C3 | 1, 2 |
| DA1 | 1, 2, 3, 4, 5, 6, 7, 8 |
| HA1 | 1, 2 |
| HL1 | 1, 2 |
| HL2 | 1, 2 |
| R1 | 1, 2 |
| R2 | 1, 2 |
| R3 | 1, 2 |
| R4 | 1, 2 |
| R5 | 1, 2 |
| R6 | 1, 2 |
| R7 | 1, 2 |
| SA1 | 1, 2 |
| VD1 | 1, 2 |
| VT1 | 1, 2, 3 |
| XS1 | 1, 2 |

## Full netlist reference

The following table is the machine-checked expected pin membership, not a claim about the physical A1 pinout. KiCad `PWR_FLAG` symbols are ERC markers and are excluded from its BOM component inventory.

| Сеть | Ожидаемые символы и выводы |
|---|---|
| VCC | A1.1, XS1.1, R1.1, R3.1, R4.1, DA1.8, C3.1, HL2.2 |
| GND | A1.4, XS1.2, VT1.3, DA1.1, C1.2, C2.2, C3.2, HL1.1, SA1.2 |
| DOUT | A1.2, R1.2, R2.1 |
| VT1_B | R2.2, VT1.1 |
| RESET | R3.2, VT1.2, DA1.4 |
| DISCH | DA1.7, R4.2, R5.1 |
| CT | DA1.2, DA1.6, R5.2, C1.1 |
| CTRL | DA1.5, C2.1 |
| OUT | DA1.3, R6.1, VD1.2 |
| HL1_A | R6.2, HL1.2 |
| HA1_P | VD1.1, HA1.1 |
| HA1_N | HA1.2, SA1.1, R7.1 |
| HL2_K | HL2.1, R7.2 |
| NC | A1.3 |

The automated check must compare every net, component reference and pin; any pin must occur exactly once on a net or in the explicit NC set. Passing this check establishes schematic/netlist parity only, not circuit operation or calibration.

## Open verification items

- Confirm the exact SEN-MQ4 V1 revision, physical pinout, DOUT polarity/output stage and full module current from revision-specific manufacturer material. Until then keep A1 abstract and the selection preliminary.
- Calculate the complete current budget at 4.9 and 5.1 V. The heater limit alone is insufficient to confirm the 300 mA requirement.
- Check component ratings, the sounder/LED currents, and the 555 reset and output behavior by datasheets and separate Original/project SPICE scenarios.
- Do not route the board until this electrical design is reviewed and approved. Physical gas calibration and hardware tests are outside the course-project scope.
