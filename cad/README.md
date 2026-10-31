# CAD: preliminary placement and enclosure

Date: 25.10.2026. Status: **PRELIMINARY / NOT FOR FABRICATION**.

## Iteration 0.1

- Native KiCad PCB placement draft: 72 x 50 x 1.6 mm, net assignments and custom in-file footprints.
- No copper routing is present. DRC unconnected-net warnings are expected and are not a pass for manufacturing.
- Control board is placed beside a separate 25.4 x 25.4 mm Amperka AMP-B052 module.
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

See [end-to-end electrical trace audit](electrical_trace_audit_2026-10-25.md) for the chain from the Amperka A1.S output through the external comparator, reset transistor, timer, LED and sounder driver.

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
