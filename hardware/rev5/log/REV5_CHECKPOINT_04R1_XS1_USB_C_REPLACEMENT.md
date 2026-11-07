# Rev5 engineering checkpoint 04R1 — XS1 replaced by USB-C

Date: 2026-11-07  
Branch: `design/usb-c-pcb-enclosure-r5`

## Decision implemented

XS1 was the dedicated two-contact VCC/Earth power inlet, not the sensor interface. It is removed in the new schematic and PCB candidate. J1 GCT USB4105 Type-C is placed on the former XS1 board side. Sensor interface A1 is retained. Added separate CC1 and CC2 Rd resistors, 5.1 kΩ each. D+/D−/SBU remain NC. Assumption: 5 V power-only sink, no PD.

## OneDrive artifacts

- Folder: https://1drv.ms/f/c/24fda6920aa8c92a/IgCzlXAjWEiPT4kG0-s0lLTLAWQL7YgHkJiJ3NXKAVn3ne0
- ZIP: https://1drv.ms/u/c/24fda6920aa8c92a/IQA-4KsYZDatTLpRYhOMJbGQAbvrRtMgZ-V9RcyXWbYdwjI
- Schematic: https://1drv.ms/u/c/24fda6920aa8c92a/IQD1JFMnvNVNT7EllJ6YICAzARKD7sLaUGmq_uO_8aazbfI
- PCB: https://1drv.ms/u/c/24fda6920aa8c92a/IQA3ivIe3LpURbYP1Qzu24wpAbcSwkDSxq-B8VNwI7WuEcE
- Preview: https://1drv.ms/i/c/24fda6920aa8c92a/IQCNI0SsAiclRIAn5yBOZH9nAQirG9i97YoX1o11sPj6l8Q

## SHA-256

- Schematic: `f4ecc00b30d8aa52d9f21f3e29bafa825ae219cdc2f13c8c2dc7e27aa8bacd5d`.
- PCB: `78840a0598cb7c21e2f556c656f200bf174126a7d0d94fdd7e42a084c783e162`.
- ZIP: `83f2bb4bb53f939dece74d18359b44430ba0c59f2a63bdfeca39828d877c3ade`.

## Static checks

- S-expression balance passed.
- 32 schematic symbol refs / 199 unique UUIDs.
- 25 PCB footprints / 891 unique UUIDs.
- No duplicate references or UUIDs.
- 4 M2 holes and board outline preserved.
- Static courtyard and pad-to-track clearances checked.
- SHA copy of project files matches generated candidates.
- ZIP contains 22 files and passes archive integrity test.

## Not done

Native KiCad ERC/DRC, Refill All Zones, 3D Viewer, STEP/enclosure fit and final routing are not done. Existing VBUS track connects J1 A4/B9 only. Other VBUS/GND/CC paths remain for routing. Protection ratings not frozen pending current-budget verification. This is not a manufacturing release.
