# Основание проектирования PCB и корпуса

**Дата актуализации:** 01.11.2026  
**Рабочая ветка:** analysis/vendor-behavioral-reconciliation  
**Электрическая база:** gost-e3-approved-2026-11-01, коммит 683e53410de5f1a960c9e060061119f843cc2c51.  
**Статус:** конструктив выбран; физическая спецификация и часть footprint-кандидатов подготовлены. Трассировка и выпуск в производство ещё не выполнены.

## 1. Решения пользователя

| Параметр | Решение |
|---|---|
| Основная PCB | 2 медных слоя |
| Монтаж | смешанный SMD + THT |
| Сенсор | Joy-IT SEN-MQ4-V2 |
| Корпус | настольный |
| Питание | USB 5 В |
| Габариты | оптимизировать по компоновке |
| Назначение | реальное изготовление + курсовая документация |
| E3 | сохранить неизменной |

## 2. Неизменяемая схема E3

Использовать утверждённые файлы:
- cad/project_modification/gost_e3_final/gazo_analizator_E3_GOST_itog.kicad_sch
- cad/project_modification/gost_e3_final/reports/kicad10/netlist_current.xml
- cad/project_modification/gost_e3_final/APPROVED_BASELINE.md

19 компонентов, 15 сетей, ERC 0 errors и 18 документированных warnings. A1.3 — отдельная сеть /AOUT. XS1 — двухконтактный вход VCC/GND. Нельзя менять E3, номиналы и электрическую топологию.

## 3. Сенсор A1

Пользователь подтвердил Joy-IT SEN-MQ4-V2. Amperka AMP-B052 исключён из текущей конструкции. A1 имеет VCC, DOUT, AOUT и GND; 4-контактный кабель подключается к Molex PicoBlade 53261-0471. Pin 1 и порядок жил проверить прозвонкой на физическом модуле. DOUT active-low — рабочая гипотеза по общему руководству Joy-IT, не гарантированный параметр конкретной ревизии V2. Допустимый ток DOUT не опубликован, проверить измерением.

По механическому чертежу SEN-MQ4-V2 плата около 25 × 35 мм, четыре отверстия Ø2.9 mm с шагом18.5 ×28.5 mm, общий габарит 41 ×25 ×21 mm. Модуль крепить отдельно от main PCB, не нагружать кабелем.

## 4. Основная PCB E3

2 слоя, mixed SMD/THT. F.Cu — компоненты и короткие сигнал/силовые связи; B.Cu — максимально непрерывная GND-плоскость. Короткий путь A1.2/DOUT к R1/R2/VT1. Не пускать ток HA1 и LED через аналоговые возвратные пути. Добавить test pads VCC, Earth, AOUT, DOUT, RESET и DA1 OUT. Ширину дорожек рассчитывать по фактическим токам, меди и тепловым ограничениям.

Footprint register: cad/footprint_selection_2026-11-01.md. Пользовательская библиотека: cad/kicad/footprints/GazoE3.pretty.

## 5. E4 USB-C power entry

USB-C не добавляется скрытыми цепями в E3. Отдельная плата E4: GCT USB4105-GF-A, Rd 5.1k на CC1/CC2, TVS, eFuse/PTC, выход защищённых +5V/GND через Molex PicoBlade 53261-0271 на XS1. Защита и лимит тока будут выбраны после измерения cold-start/warm-up/steady/alarm currents. До измерений не назначать eFuse/PTC.

## 6. Физические компоненты и риски

- DA1: TI NE555P PDIP-8, Package_DIP:DIP-8_W7.62mm, коммерческий диапазон 0…+70 °C. Проверить требования по температуре, иначе выбрать расширенный аналог без изменения netlist.
- VT1: КТ3102Б без суффикса М — металлостеклянный корпус с гибкими выводами. Запрещено переносить старый KT-26/TO-92 footprint. Footprint не создан до измерения фактических выводов.
- HA1: выбран документированный вариант Ningbo Kepo HCM1206X, drawing OEM2690R. Rated 6V, operating 4…8V, max rated current 40mA at 6V, SPL 88dB/10cm. Питание 5V допустимо по рабочему диапазону. Полярность по знаку плюс на верхней маркировке, но соответствующий физический вывод проверить на образце.
- SA1: NKK AS11AP, SPST ON-NONE-OFF, straight PC terminals. AS11 соединяет terminals 3-1, terminal2 отсутствует. Custom pad1/2 correspond to physical1/3. Проверить ориентацию actuator и посадку.
- Пассивы, LED и диод: кандидаты и MPN в реестре footprints. Ток LED/R6/R7 проверить по реальному UOH таймера.

## 7. USB-C питание и токовый бюджет

Целевое ограничение 300mA сохраняется, пока измерения не подтвердят его достижимость. SEN-MQ4-V2 current max в паспорте не опубликован. HCM1206X specific sheet states max rated 40mA at6V, not generic 30mA. Измерить ток датчика при старте/прогреве/установившемся режиме и полный ток в тревоге с HA1 и HL1/HL2. Выбрать защиту E4 после этих данных.

## 8. Статус ворот

| Gate | Условие | Статус |
|---|---|---|
| G0 | Пользовательские требования | PASS |
| G1 | Joy-IT module selected | PASS по выбору; pin map физически не проверен |
| G2 | E4 USB-C architecture | PARTIAL; protection/current budget open |
| G3 | MPN and footprint candidates | PARTIAL; KT3102B, DA1 temp range, sample checks open |
| G4 | All library footprints opened/checked in KiCad 10 | NOT STARTED |
| G5 | PCB parity, zero unconnected, DRC clean and manual routing review | NOT STARTED |
| G6 | Full FreeCAD case assembly and collision checks | NOT STARTED |
| G7 | Gerber/Excellon/BOM/CPL/PDF | NOT STARTED |

## 9. Правило выпуска

Не редактировать утверждённую E3. E4 оформить отдельной схемой и PCB. Сначала закрыть точные MPN/pinout/footprints, затем placement and routing. Не выпускать Gerber/CPL/BOM до KiCad 10 validation, DRC, физической посадки, электрического и теплового контроля.


## 10. Уточнение HA1 и физической элементной базы

Для HA1 выбран конкретный документированный изготовитель: Ningbo Kepo Electronics, HCM1206X, drawing OEM2690R. Спецификация задаёт 6 V rated, 4…8 V operating, maximum rated current 40 mA at 6 V, SPL 88 dB/10 cm, Ø12 × 9.5 mm body and 7.6 ±0.2 mm lead pitch. Этот паспорт точнее общего семейного каталога, где для иных вариантов HCM12X встречается предел 30 mA. Для токового worst-case использовать 40 mA до измерения при 5 V. HCM plus mark is printed on the upper face; actual positive lead must be confirmed on the received unit.

DA1 candidate is TI NE555P PDIP-8, 0…+70 °C. If the final environmental requirement is wider, the footprint remains DIP-8 but the MPN must be reconsidered. The approved E3 schematic is unchanged.

SA1 candidate is NKK AS11AP. According to the NKK Series AS data, AS11 is SPST ON-NONE-OFF and connects physical contacts 3–1. Terminal2 is absent. Two PCB pads are mapped to physical terminals 1 and 3.

KT3102Б is the metal-glass type with flexible leads, not KT3102БМ plastic type. No PCB footprint is assigned until the physical leads and top-view orientation are measured.
