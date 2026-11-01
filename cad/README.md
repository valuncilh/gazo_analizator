# CAD: historical preliminary placement and current E3/E4 design

The original iteration below is **HISTORICAL / SUPERSEDED**. Current design requirements are in [pcb_design_basis_2026-11-01.md](pcb_design_basis_2026-11-01.md). No manufacturing release is implied.

## Iteration 0.1

- Native KiCad PCB placement draft: 72 x 50 x 1.6 mm, net assignments and custom in-file footprints.
- No copper routing is present. DRC unconnected-net warnings are expected and are not a pass for manufacturing.
- This historical placement used a separate 25.4 x 25.4 mm Amperka AMP-B052 module. The current design uses Joy-IT SEN-MQ4-V2 and does not reuse this mechanical placement.
- A parametric FreeCAD case concept is provided at 120 x 78 x 42 mm. It includes a removable lid, standoffs, module rails, MQ-4 vent grid, HCM1205X aperture, LED holes and a provisional power connector cutout.
- The selected JL World HCM1205X dimensions come from passport 0105-86 Rev. A2: body OD 12 mm, height about 9.5 mm, lead pitch 7.6 mm. The MQ-4 sensor can profile is still a TBC envelope.

## Critical TBC items

1. KT3102GM manufacturer-specific pinout, package drawing and saturation at the required collector current.
2. The physical P1 trim potentiometer, SA1 DPDT switch and XS1 power connector.
3. Exact resistor, capacitor, LED and diode footprints.
4. KiCad schematic, ERC, netlist parity, PCB routing and DRC closure.
5. Actual A1 mounting method, MQ-4 sensor height, ventilation and heat clearances.
6. Acoustic clearance and lid light-pipe fit.
7. Formal mechanical test levels and any required ingress-protection criteria.

## Sources

- Amperka AMP-B052: https://amperka.ru/product/troyka-mq4-gas-sensor and https://wiki.amperka.ru/продукты:mq4.
- JL World HCM1205X, Specification 0105-86 Rev. A2: https://satec.ru/_img/goods_attach/474/00-00135474/134038_0.pdf.
- KR1006VI1, package 2101.8-1: https://radiolub.ru/uploads/2012pic/kr1006vi1.pdf.
- KiCad PCB file format: https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/.
- KiCad CLI: https://docs.kicad.org/9.0/en/cli/cli.html.
- FreeCAD headless usage: https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Headless_FreeCAD.md.

## Next gate

Create a native KiCad schematic and validate its pin mapping before routing. Replace all TBC footprints with exact selected manufacturer footprints, run ERC/DRC, then issue production files only after the thermal/current/case mechanical blockers have been reviewed.


## Electrical trace audit

The [historical electrical trace audit](electrical_trace_audit_2026-10-25.md) describes the Amperka A1.S path and an alternative comparator design. It is not the current Joy-IT E3 signal path and must not be used to populate the current PCB.

Run `python3 cad/scripts/test_electrical_trace.py` locally to compare declared SPICE nodes against the provisional PCB pad-net map. This is a topology consistency check, not a measurement of copper continuity.

Latest completed physical-layout checks before the trace regression was added:

- KiCad pad-net map: 27 expected footprints and 72 pad assignments matched.
- KiCad DRC: 0 geometry violations, but 53 unconnected items.
- Copper tracks: 0. The PCB is still **UNROUTED**.
- Preliminary FreeCAD FCStd, STEP and STL exports were generated in an earlier model build. Their geometry and fit still require manual review against the selected components.

Do not generate manufacturing files from this draft. The native schematic/ERC/netlist parity, exact component pinouts and footprints, copper routing and physical fit checks remain open.


## Проектная схема Э3 по ЕСКД

Проектная электрическая принципиальная схема CH₄ оформляется отдельным комплектом и не смешивается с транскрипцией Original 2022. Проверяемые критерии оформления, электрической топологии, ERC и выдаваемых артефактов находятся в [критериях приёмки Э3](project_modification_eskd/acceptance_criteria.md).

Перед переносом экспериментальной компоновки в репозиторий необходимо перенести её исходный генератор, эталонную таблицу и локальные результаты KiCad. До этого локальный PASS не является воспроизводимой проверкой из текущего Git-состояния. Все результаты остаются **PRELIMINARY / NOT FOR FABRICATION**.

Первичная таблица соответствия символов и координат выводов: [аудит GOST-символов](project_modification_eskd/symbol_mapping.md). Это карта кандидатов, не финальная приёмка УГО.

Методическая основа формата: [анализ материалов МАИ](project_modification_eskd/mai_methodical_basis.md). Для текущего курсового проекта выбран A4 по пособию МАИ 2007, раздел 1.3, печатная с. 5. A1 в этом пособии относится к графической части дипломного проекта и не применяется к нашей курсовой.

Для листа A4 установлена книжная ориентация и размещение основной надписи вдоль короткой стороны по ГОСТ Р 2.104-2023, приложение Б, Б.5. Альбомное A4 не использовать.


## Current design selection — 01.11.2026

The selected sensor is Joy-IT SEN-MQ4-V2. The approved E3 schematic remains unchanged. A1 uses the Molex PicoBlade 53261-0471 candidate and XS1 uses 53261-0271. The physical A1 Molex pin-1 mapping to VCC/DOUT/AOUT/GND is not explicit in the available module documentation and remains TBC; no physical continuity test is part of this CAD-only project. USB-C is on a separate two-layer E4 power-entry PCB. Current MPN and package restrictions are documented in [footprint_selection_2026-11-01.md](footprint_selection_2026-11-01.md), [the 02.11.2026 footprint audit](footprint_audit_2026-11-02.md), and [power_input_usb/README.md](power_input_usb/README.md).

A preliminary FreeCAD sensor envelope macro is provided at `freecad/build_joyit_sen_mq4_v2_envelope.FCMacro`. It has not yet been executed or checked in FreeCAD. The main enclosure must be designed after the actual E3 and E4 PCB layouts and the sensor module envelope have been verified.


## Frozen E3 PCB routing basis — 01.11.2026

- Exact net-to-pin map: [`e3_netlist_map_2026-11-01.md`](e3_netlist_map_2026-11-01.md)
- Placement and routing priority: [`placement_plan_joyit_e3_2026-11-01.md`](placement_plan_joyit_e3_2026-11-01.md)
- Netlist regression: `python3 cad/scripts/verify_e3_netlist.py`

These files describe the approved E3 logical topology only. They do not claim that the board has been placed, routed, or DRC-checked.


## E3 implementation project scaffold

An isolated implementation copy is prepared in [`kicad/e3_project/`](kicad/e3_project/). It contains:
- `gazo_e3_implementation.kicad_sch` — implementation copy of the approved E3 schematic, with candidate footprint fields assigned to all 19 physical references. The source schematic remains immutable.
- `fp-lib-table` — local GazoE3 footprint library registration.
- `reports/e3_pad_net_map.csv` — 47 pin-to-net assignments.
- `reports/footprint_assignment_status.csv` — 19-reference candidate/restriction register.

Run `python3 cad/scripts/verify_e3_implementation.py` from the repository root for source-level checks of the implementation copy and immutable schematic/netlist blob IDs. This script does not replace KiCad 10 validation.

No `.kicad_pro` or `.kicad_pcb` has been created in this scaffold yet. The next gate is to open the implementation schematic in KiCad 10.0.7, confirm the project-local GazoE3 library resolves, run ERC and export a fresh XML-netlist. Only after topology parity is confirmed should the board file be created.

## Approved E3 placement and routing plan

The current placement zones and routing priorities derived from the immutable approved XML-netlist are documented in [`placement/e3_placement_plan.md`](placement/e3_placement_plan.md). Conceptual zone diagram: [`placement/e3_placement_zones.svg`](placement/e3_placement_zones.svg).

The netlist audit script is [`scripts/verify_e3_netlist.py`](scripts/verify_e3_netlist.py). The 47-row exported [pad-to-net map](project_modification/gost_e3_final/reports/kicad10/e3_pad_net_map.csv) is committed next to the approved KiCad reports. Run the audit locally from the repository root with:

```fish
python3 cad/scripts/verify_e3_netlist.py --write-csv
```

The script checks the approved XML blob, all 19 component values, 15 exact nets and 47 connected pins, and exports a pad-to-net CSV. It is a topology check only, not KiCad DRC.
