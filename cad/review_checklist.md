# CAD review checklist — iteration 0.1

- [x] Add native preliminary KiCad PCB file generator and source.
- [x] Add custom in-file footprints for provisional components and connectors.
- [x] Add a static checker and preliminary BOM/placement reports.
- [x] Add a parameter-driven FreeCAD enclosure script and STEP/STL/FCStd output rules.
- [x] Add explicit PRELIMINARY / NOT FOR FABRICATION warnings.
- [x] Create separate native KiCad schematics for Original 2022 and the preliminary project modification; run ERC and full component/pin/netlist comparisons. Physical Joy-IT pin mapping remains unconfirmed.
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
- [x] Создана самостоятельная KiCad-транскрипция Original 2022; DA1 и окружающие подписи визуально разнесены, netlist сверяется по сетям/компонентам/выводам. ERC 10.0.7: 0 ошибок, 17 предупреждений только по пустым footprint-полям; игнорируемых категорий нет. Это ещё не проектная Э3 и не готовая Э3 по ЕСКД.
- [x] Создана отдельная предварительная KiCad-схема проектной модификации; ERC/netlist и полный список сетей, компонентов, выводов проверены. Электрическое утверждение, физический pinout A1 и калибровка 1000 ppm остаются открытыми.
- [ ] После утверждения проектной схемы выполнить трассировку PCB, затем DRC, проверить незамкнутые сети и визуальную геометрию платы.

## Результат последнего диагностического маршрута

В ранее сохранённом диагностическом результате FreeRouting было получено 205 медных объектов (190 сегментов и 15 vias). После импорта SES оставались одно незамкнутое соединение GND у U2 pad 2 и одно нарушение `via_dangling` сети SOUND_CTL. Этот кандидат не принят. Перед дальнейшей работой необходимо повторить локальную трассировку и полный DRC, а затем вручную проверить геометрию в KiCad.

Все CAD-артефакты остаются **PRELIMINARY / NOT FOR FABRICATION**. Генерация файлов сама по себе не является механической или аппаратной приёмкой.


## Проектная электрическая принципиальная схема Э3 по ЕСКД

Критерии приёмки: [cad/project_modification_eskd/acceptance_criteria.md](project_modification_eskd/acceptance_criteria.md).

- [x] Зафиксировать нормативную базу и проверяемые критерии приёмки Э3.
- [x] Создать первичную таблицу соответствия GOST-кандидатов, номеров и координат выводов: [symbol_mapping.md](project_modification_eskd/symbol_mapping.md). Полная проверка графики и таблиц стандартов ещё открыта.
- [ ] Подготовить автономный листовой шаблон `.kicad_wks` с основной надписью по ГОСТ Р 2.104-2023 и сверить его с методикой МАИ.
- [ ] Перестроить проектную схему по функциональным группам, без коллизий проводов, УГО и текстовых полей.
- [ ] Для каждой итерации получить полный PASS эталонного netlist: 13 сетей, 19 компонентов, 47 выводов, NC A1.3.
- [ ] Получить ERC 0 ошибок и классифицировать все предупреждения без отключения категорий проверки.
- [ ] Проверить полный SVG и PDF в масштабе печати. Проверить также увеличенные фрагменты.
- [ ] Сформировать BOM, отчёты netlist/ERC и зафиксировать версии KiCad, символов и листового шаблона.
- [ ] Не назначать неподтверждённые footprints и не выдавать схему как готовую к изготовлению.

**Локальное состояние на 31.10.2026, сообщённое пользователем:** netlist exact PASS; ERC — 0 ошибок и 19 предупреждений (17 пустых footprint-фильтров, 2 четырёхсторонних соединения). Локальный генератор проектной схемы ещё не опубликован в этой ветке, поэтому результат не считается воспроизводимым из репозитория до переноса и повторной проверки исходников.

## Уточнение формата Э3 по методическим материалам МАИ

- [x] Проверить пособие МАИ «Проектирование РЭС» (2007), раздел 1.3: для курсового проекта графическая часть выполняется на A4 (печатная с. 5).
- [x] Не переносить A1/1–2 листа Э3 из раздела дипломного проектирования (печатная с. 7) на текущую курсовую работу.
- [x] Установить книжную ориентацию A4 по ГОСТ Р 2.104-2023, приложение Б, Б.5. Альбомное A4 не применяется.
- [x] Зафиксировать выводы в [методической основе](project_modification_eskd/mai_methodical_basis.md) и скорректировать [критерии Э3](project_modification_eskd/acceptance_criteria.md).


## Physical part and footprint selection — 01.11.2026

- [x] Select NE555P PDIP-8 as DA1 physical candidate; temperature range 0…+70 °C is an explicit gate.
- [x] Identify KT3102B as metal-glass variant, not KT3102BM/KT-26 plastic. Do not assign a TO-92 footprint.
- [x] Select Ningbo Kepo HCM1206X drawing OEM2690R; update HA1 current allowance to 40 mA at rated 6 V.
- [x] Select NKK AS11AP SPST and map physical terminals 1/3 to the two E3 symbol pins.
- [x] Select Yageo 0805 resistors, Multicomp Pro radial capacitors, Kingbright 5 mm LEDs.
- [x] Create GazoE3 custom source footprints for HCM1206X and NKK AS11AP.
- [x] Add source-level footprint pad-map checker.
- [ ] Load GazoE3.pretty in KiCad 10.0.7 and run footprint checks.
- [ ] Verify the HCM1206X plus mark against its actual positive lead.
- [ ] Verify NKK AS11AP actuator orientation/panel geometry.
- [ ] Measure KT3102B real lead locations and map pin1=B, pin2=C, pin3=E.
- [ ] Confirm DA1 temperature range is acceptable.
- [ ] Measure HA1 current and LED currents with actual DA1 output level.
