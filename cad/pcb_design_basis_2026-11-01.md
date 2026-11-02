# Основание проектирования PCB и корпуса

**Дата актуализации:** 01.11.2026  
**Рабочая ветка:** analysis/vendor-behavioral-reconciliation  
**Электрическая база:** gost-e3-approved-2026-11-01, коммит 683e53410de5f1a960c9e060061119f843cc2c51.  
**Статус:** конструктивная архитектура и документальные MPN/footprint-кандидаты подготовлены. Реализация PCB и полная CAD-увязка ещё не выполнены. Физическое изготовление, закупка, сборка и лабораторные измерения не входят в текущий объём.

## 1. Решения пользователя

| Параметр | Решение |
|---|---|
| Основная PCB | 2 медных слоя |
| Монтаж | смешанный SMD + THT |
| Сенсор | Joy-IT SEN-MQ4-V2 |
| Корпус | настольный |
| Питание | USB 5 В |
| Габариты | оптимизировать по компоновке |
| Назначение | проектная CAD-конструкция и курсовая документация без физического изготовления |
| E3 | сохранить неизменной |

## 2. Неизменяемая схема E3

Использовать утверждённые файлы:
- cad/project_modification/gost_e3_final/gazo_analizator_E3_GOST_itog.kicad_sch
- cad/project_modification/gost_e3_final/reports/kicad10/netlist_current.xml
- cad/project_modification/gost_e3_final/APPROVED_BASELINE.md

19 компонентов, 15 сетей, ERC 0 errors и 18 документированных warnings. A1.3 — отдельная сеть /AOUT. XS1 — двухконтактный вход VCC/GND. Нельзя менять E3, номиналы и электрическую топологию.

## 3. Сенсор A1

Пользователь подтвердил Joy-IT SEN-MQ4-V2. Amperka AMP-B052 исключён из текущей конструкции. A1 имеет VCC, DOUT, AOUT и GND; 4-контактный кабель подключается к Molex PicoBlade 53261-0471. Доступный паспорт не содержит однозначной нумерации физических контактов Molex относительно VCC/DOUT/AOUT/GND. Pin mapping и ориентация жгута остаются TBC до нахождения номерного чертежа. DOUT active-low — гипотеза по общему руководству Joy-IT, не гарантированный параметр конкретной ревизии V2. Допустимый ток DOUT не опубликован и документально не подтверждён.

По механическому чертежу SEN-MQ4-V2 плата около 25 × 35 мм, четыре отверстия Ø2.9 mm с шагом18.5 ×28.5 mm, общий габарит 41 ×25 ×21 mm. Модуль крепить отдельно от main PCB, не нагружать кабелем.

## 4. Основная PCB E3

2 слоя, mixed SMD/THT. F.Cu — компоненты и короткие сигнал/силовые связи; B.Cu — максимально непрерывная GND-плоскость. Короткий путь A1.2/DOUT к R1/R2/VT1. Не пускать ток HA1 и LED через аналоговые возвратные пути. Добавить test pads VCC, Earth, AOUT, DOUT, RESET и DA1 OUT. Ширину дорожек рассчитывать по фактическим токам, меди и тепловым ограничениям.

Footprint register: cad/footprint_selection_2026-11-01.md. Пользовательская библиотека: cad/kicad/footprints/GazoE3.pretty.

## 5. E4 USB-C power entry

USB-C не добавляется скрытыми цепями в E3. Отдельная плата E4: GCT USB4105-GF-A, Rd 5.1k на CC1/CC2, TVS, eFuse/PTC, выход защищённых +5V/GND через Molex PicoBlade 53261-0271 на XS1. Защита и лимит тока должны обосновываться по гарантированным паспортным данным и worst-case расчёту. Максимальный полный ток SEN-MQ4-V2 не опубликован. Физические измерения не входят в проект, поэтому F1 и доказательство лимита 300 mA могут остаться TBC/BLOCKED.

## 6. Физические компоненты и риски

- DA1: TI NE555P PDIP-8, Package_DIP:DIP-8_W7.62mm, рабочий диапазон 0…+70 °C покрывает утверждённые +10…+35 °C. В отдельной реализации сверить pin numbering symbol NE555D и physical NE555P. Утверждённую E3 не менять.
- VT1: КТ3102Б без суффикса М — металлостеклянный KT-1-7 с гибкими выводами. Draft footprint создан по справочнику 1989 года: Ø4.95 mm, max envelope около Ø5.8 mm, высота 5.3 mm, выводы Ø0.45 mm × 13.5 mm. Семейный лист RadioIzba указывает Ø0.5 mm × 14.5 mm. В реализации pad map 1=B, 2=C, 3=E. Координаты upper pair 1.6 mm на Ø2.5 mm circle — DRAFT; дополнительный 1.2 mm callout требует сверки. Старый KT-26/TO-92 footprint запрещён.
- HA1: Ningbo Kepo HCM1206X, drawing OEM2690R. Drawing specifies 40 mA at 6 V, 4…8 V and −25…+70 °C. The general HCM12X family sheet conflicts on current and voltage. For conservative design retain 40 mA and 4…7 V. Physical pin corresponding to the golden + mark is not unambiguously identified in available documentation and remains TBC.
- SA1: NKK AS11AP, SPST ON-NONE-OFF, straight PC terminals. AS11 соединяет terminals 3-1, terminal2 отсутствует. Custom pad1/2 correspond to physical1/3. Проверить ориентацию actuator и посадку.
- VD1: КД510А в стеклянном корпусе КД-2. ГОСТ 18472-88 задаёт для КД-2 корпус Ø1.5…2.2 mm × 3.5…5.4 mm и выводы Ø0.45…0.56 mm. Для CAD выбран KiCad DO-35 horizontal 4×2 mm, pitch 7.62 mm, drill 0.8 mm. Pad 1=K, pad 2=A соответствует frozen E3. KiCad 10 footprint check pending.
- Пассивы и LED: кандидаты и MPN в реестре footprints. Ток LED/R6/R7 проверить по worst-case параметрам NE555P и выбранных светодиодов.

## 7. USB-C питание и токовый бюджет

Целевое ограничение 300 mA сохраняется как проектное требование. Максимальный полный ток SEN-MQ4-V2 в доступном паспорте не указан. Физические измерения не входят в объём проекта. HCM1206X OEM2690R задаёт 40 mA при 6 V. Для E4 требуется worst-case расчёт по документированным верхним пределам. Если максимальный ток A1 остаётся неизвестным, выбор F1 и доказательство лимита 300 mA остаются BLOCKED/TBC.

## 8. Статус ворот

| Gate | Условие | Статус |
|---|---|---|
| G0 | Пользовательские требования | PASS |
| G1 | Joy-IT module selected | PASS по выбору модели; Molex pin mapping TBC по доступной документации |
| G2 | E4 USB-C architecture | PARTIAL; protection/current budget open |
| G3 | MPN and footprint candidates | PARTIAL; KT3102B, DA1 temp range, sample checks open |
| G4 | All library footprints opened/checked in KiCad 10 | NOT STARTED |
| G5 | PCB parity, zero unconnected, DRC clean and manual routing review | NOT STARTED |
| G6 | Full FreeCAD case assembly and collision checks | NOT STARTED |
| G7 | Gerber/Excellon/BOM/CPL/PDF | NOT STARTED |

## 9. Правило выпуска

Не редактировать утверждённую E3. E4 оформить отдельной схемой и PCB. Сначала закрыть точные MPN/pinout/footprints, затем placement and routing. В текущем объёме производственное изготовление не выполняется. Gerber/Drill/BOM/CPL могут формироваться только как проектные CAD-артефакты после KiCad 10 validation, DRC и CAD-проверки механических зазоров. Маркировать PRELIMINARY / NOT FOR FABRICATION. Физическая посадка и аппаратная проверка не заявляются.


## 10. Уточнение HA1 и физической элементной базы

Для HA1 выбран конкретный документированный изготовитель: Ningbo Kepo Electronics, HCM1206X, drawing OEM2690R. Спецификация задаёт 6 V rated, 4…8 V operating, maximum rated current 40 mA at 6 V, SPL 88 dB/10 cm, Ø12 × 9.5 mm body and 7.6 ±0.2 mm lead pitch. Этот паспорт точнее общего семейного каталога, где для иных вариантов HCM12X встречается предел 30 mA. Для консервативного токового расчёта использовать 40 mA при 6 V как паспортный номинальный максимум. Доступный drawing не позволяет однозначно определить, какой физический вывод соответствует золотой метке «+», поэтому полярность остаётся TBC.

DA1 candidate is TI NE555P PDIP-8, 0…+70 °C. If the final environmental requirement is wider, the footprint remains DIP-8 but the MPN must be reconsidered. The approved E3 schematic is unchanged.

SA1 candidate is NKK AS11AP. According to the NKK Series AS data, AS11 is SPST ON-NONE-OFF and connects physical contacts 3–1. Terminal2 is absent. Two PCB pads are mapped to physical terminals 1 and 3.

KT3102Б is the metal-glass type with flexible leads, not KT3102БМ plastic type. PCB footprint ещё не создан. Для текущего CAD-only проекта координаты и ориентацию выводов следует получить транскрипцией заводского чертежа, без требования физического образца.
