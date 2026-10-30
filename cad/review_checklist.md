# CAD review checklist — iteration 0.1

- [x] Add native preliminary KiCad PCB file generator and source.
- [x] Add custom in-file footprints for provisional components and connectors.
- [x] Add a static checker and preliminary BOM/placement reports.
- [x] Add a parameter-driven FreeCAD enclosure script and STEP/STL/FCStd output rules.
- [x] Add explicit PRELIMINARY / NOT FOR FABRICATION warnings.
- [ ] Create a native KiCad schematic and verify pin mapping through ERC/netlist.
- [ ] Confirm exact KT3102GM variant, package drawing, and C-B-E ordering.
- [ ] Select physical potentiometer P1, switch SA1, power connector XS1.
- [ ] Replace every TBC footprint with manufacturer dimensions.
- [ ] Verify actual A1 module fit, MQ-4 sensor-can height, gas access and thermal clearance.
- [ ] Verify sounder aperture and LED light-pipe fit.
- [ ] Complete copper routing and resolve DRC issues.
- [ ] Generate Gerber/drill and assembly documentation only after design-review gate.

The current PCB is intentionally unrouted. Its DRC report is diagnostic only. No manufacture release is implied.


## Сверка CAD-состояния

- [x] Создан предварительный KiCad PCB с 27 footprints и 72 назначениями площадок.
- [x] В ранее полученном диагностическом отчёте KiCad геометрических DRC-нарушений не было.
- [ ] Медная трассировка и электрическая замкнутость не подтверждены. Базовый вариант содержал 53 незамкнутых соединения и 0 медных сегментов.
- [x] Создан параметрический FreeCAD-макрос корпуса и ранее получены предварительные FCStd, STEP и STL. Физическая посадка деталей и механические зазоры не приняты.
- [x] Создан [аудит сквозной трассировки](electrical_trace_audit_2026-10-25.md) и локальный скрипт `cad/scripts/test_electrical_trace.py`.
- [ ] Выполнить локальную проверку в KiCad: назначение сетей, DRC, незамкнутые соединения и визуальный осмотр платы.
- [ ] Выполнить локальную проверку FreeCAD-модели и экспортов после уточнения размеров реальных компонентов.
- [ ] Создать нативную схему KiCad, проверить соответствие netlist электрической архитектуре и уточнить все TBC footprints.

## Результат последнего диагностического маршрута

В ранее сохранённом диагностическом результате FreeRouting было получено 205 медных объектов (190 сегментов и 15 vias). После импорта SES оставались одно незамкнутое соединение GND у U2 pad 2 и одно нарушение `via_dangling` сети SOUND_CTL. Этот кандидат не принят. Перед дальнейшей работой необходимо повторить локальную трассировку и полный DRC, а затем вручную проверить геометрию в KiCad.

Все CAD-артефакты остаются **PRELIMINARY / NOT FOR FABRICATION**. Генерация файлов сама по себе не является механической или аппаратной приёмкой.
