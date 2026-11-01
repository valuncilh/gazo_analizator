# Реестр физических исполнений и footprints — 01.11.2026

**Электрическая база:** утверждённая E3, коммит 683e53410de5f1a960c9e060061119f843cc2c51. Утверждённый файл схемы не изменяется.

**Аудит:** [документальная проверка MPN, корпусов и footprints от 02.11.2026](footprint_audit_2026-11-02.md). В нём зафиксированы границы паспортной проверки и TBC без требования физического образца.

## 1. A1, XS1 и USB-C E4

| Позиция | Физический компонент | MPN / тип | Footprint KiCad | Статус |
|---|---|---|---|---|
| A1 | Joy-IT SEN-MQ4-V2, кабельный интерфейс | Molex 53261-0471, 4 circuits, 1.25 mm | Connector_Molex:Molex_PicoBlade_53261-0471_1x04-1MP_P1.25mm_Horizontal | Выбран. Нумерацию Molex относительно VCC/DOUT/AOUT/GND документально подтвердить не удалось. Pin mapping TBC |
| A1 | Сенсорный модуль | Joy-IT SEN-MQ4-V2 | Внешний модуль, отдельное крепление по четырём отверстиям Ø2.9 mm, плата 25×35 mm, pitch отверстий 18.5×28.5 mm | Размеры взяты из заводского drawing. Корпус/высота сенсорной банки частично остаются TBC |
| XS1 | Вход основной E3 платы от E4 | Molex 53261-0271, 2 circuits, 1.25 mm | Connector_Molex:Molex_PicoBlade_53261-0271_1x02-1MP_P1.25mm_Horizontal | Выбран. Pin 1=/VCC и pin 2=Earth по утверждённой E3. Кабельная ориентация TBC до фиксации чертежа жгута |
| USB1 / E4 | USB-C receptacle | GCT USB4105-GF-A, оригинальный shell stake 0.95 mm | Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal | Выбранный кандидат. 2D/3D библиотека отображается в KiCad. Размеры и точную ревизию footprint сверить с drawing перед завершением E4 |
| R_CC1, R_CC2 / E4 | Rd termination | 5.1 kΩ, 1% | Resistor_SMD:R_0603_1608Metric | Номинал и корпус выбраны, точный MPN не назначен |
| F1 / E4 | Ограничитель тока VBUS | eFuse или PTC | Не назначен | BLOCKED: максимальный полный ток A1 не опубликован. Физические измерения не входят в объём проекта, поэтому предел может остаться TBC |
| D_TVS / E4 | Защита VBUS | TVS для USB 5 V | Не назначен | BLOCKED до выбора электрических критериев защиты и конкретного MPN |

## 2. Основные компоненты E3

| Позиция | Выбранный кандидат | Footprint KiCad | Состояние и ограничения |
|---|---|---|---|
| DA1 | Texas Instruments NE555P, PDIP-8 | Package_DIP:DIP-8_W7.62mm | Рабочая температура 0…+70 °C покрывает утверждённые +10…+35 °C. Утверждённый символ NE555D и значение NE555N не меняются. В отдельной реализации проверить одинаковую нумерацию функций symbol→footprint |
| VT1 | КТ3102Б без суффикса М | Собственный footprint по чертежу KT-1-7, ещё не создан | Заводской чертёж семейства подтверждает металлостеклянный корпус с гибкими выводами и позволяет подготовить drawing-derived footprint. Старый KT-26/TO-92 footprint запрещён. Координаты трёх выводов и ориентацию сверить по рисунку до назначения |
| HA1 | Ningbo Kepo HCM1206X, drawing OEM2690R | GazoE3:HCM1206X_P7.6mm | Чертёж OEM2690R: 6 V rated, 4…8 V, до 40 mA при 6 V, -25…+70 °C, корпус Ø12×9.5 mm, pitch 7.6±0.2 mm, leads Ø0.6 mm. Общая спецификация HCM12X расходится по току и напряжению. Для консервативного анализа оставить 40 mA и 4…7 V. Положительный физический вывод не определяется по доступному рисунку однозначно. Сохранить маркировку CHECK + и статус TBC |
| SA1 | NKK AS11AP, SPST ON-NONE-OFF, straight PC | GazoE3:NKK_AS11AP_SPST_P5.08mm | Physical terminals 1 and 3 are fitted; terminal 2 is absent. Pad 1 maps to terminal 1, pad 2 to terminal 3. Contact rating 0.4 VA logic level. |
| R1 | Yageo RC0805FR-07160KL, 160 kΩ, 1%, 0.125 W | Resistor_SMD:R_0805_2012Metric | Candidate MPN |
| R2 | Yageo RC0805FR-0713KL, 13 kΩ, 1%, 0.125 W | Resistor_SMD:R_0805_2012Metric | Candidate MPN |
| R3 | Yageo RC0805FR-072KL, 2 kΩ, 1%, 0.125 W | Resistor_SMD:R_0805_2012Metric | Candidate MPN |
| R4, R5 | Yageo RC0805FR-078K2L, 8.2 kΩ, 1%, 0.125 W | Resistor_SMD:R_0805_2012Metric | Candidate MPN |
| R6, R7 | Yageo RC0805FR-07220RL, 220 Ω, 1%, 0.125 W | Resistor_SMD:R_0805_2012Metric | Candidate MPN. Verify LED current using actual NE555 output level |
| C1, C3 | Multicomp Pro MCGLR16V476M5X11, 47 µF, 16 V | Capacitor_THT:CP_Radial_D5.0mm_P2.00mm | Radial Ø5 x 11 mm, pitch 2 mm, ±20%, lifetime 2000 h at 105 °C, ripple 108 mA |
| C2 | Yageo CC0805KRX7R9BB104, 100 nF, 50 V, X7R, 10% | Capacitor_SMD:C_0805_2012Metric | Candidate MPN |
| VD1 | КД510А, glass axial diode | Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal | Candidate. Confirm cathode mark and map E3 symbol pin 1=K, pin 2=A |
| HL1 | Kingbright WP7083SED/J3, red 5 mm diffused | LED_THT:LED_D5.0mm | 625 nm, 600 mcd minimum / 1200 mcd typical at 20 mA, Vf typ 2.2 V |
| HL2 | Kingbright WP7083ZGD/G, green 5 mm diffused | LED_THT:LED_D5.0mm | 525 nm, 1400 mcd minimum / 2200 mcd typical at 20 mA, Vf typ 3.2 V |

## 3. Кабельные ответные части Molex

Платные header 53261-0471 и 53261-0271 требуют ответных кабельных компонентов. Предварительные BOM candidates:
- 51021-0400 — housing, 4 circuits, для сенсорного кабеля A1.
- 51021-0200 — housing, 2 circuits, для кабеля E4↔XS1.
- 50058-8000 — female crimp terminal, проверить разрешённое сечение проводника и совместимость с выбранным обжимным инструментом.

Для двухстороннего кабеля ориентировочно требуется 2 корпуса и 8 контактов для A1, 2 корпуса и 4 контакта для E4↔XS1. Это расчётный BOM candidate, а не подтверждённая кабельная спецификация. Длина, сечение и pin-1 orientation ещё не установлены.

## 4. Собственная библиотека GazoE3

Расположение: cad/kicad/footprints/GazoE3.pretty. Проектная таблица библиотек добавлена рядом с утверждённой E3 в cad/project_modification/gost_e3_final/fp-lib-table.

Созданы два footprint-кандидата:
- HCM1206X_P7.6mm — физическая геометрия из чертежа Ningbo Kepo OEM2690R. Pad 1/2 соответствуют HA1.1/HA1.2, полярность не кодируется до проверки образца.
- NKK_AS11AP_SPST_P5.08mm — прямые выводы с межцентровым расстоянием 5.08 mm. Pad 1/2 соответствуют физическим контактам 1/3 switch.

KT3102Б footprint намеренно не создавался. Паспорт подтверждает металлостеклянный корпус и гибкие выводы, но точную ориентацию и центры выводов необходимо получить с физического транзистора или заводского размерного чертежа.

Source-level checker: cad/scripts/verify_gazo_e3_footprints.py. Он проверяет только исходный текст и координаты площадок, но не заменяет проверку в KiCad 10.

## 5. Источники

- Joy-IT SEN-MQ4-V2: https://www.joy-it.net/en/products/SEN-MQ4-V2
- Molex PicoBlade: https://www.content.molex.com/dxresources/2bfd/2bfdda32-7a36-4e6f-bd3d-e4c63f5757d9.pdf
- GCT USB4105: https://gct.co/connector/usb4105
- TI NE555P: https://www.ti.com/product/NE555/part-details/NE555P
- Ningbo Kepo HCM1206X OEM2690R: https://kvarci.ru/files/files/HCM1206X%3DDAP1206X%5BOEM2690%5D.pdf
- NKK Series AS: https://www.nkkswitches.com/wp-content/uploads/2016/02/slides.pdf
- Yageo RC0805FR: https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-07160KL
- Multicomp Pro MCGLR16V476M5X11: https://cpc.farnell.com/multicomp-pro/mcglr16v476m5x11/capacitor-47uf-16v-radial-105/dp/CA08260
- Kingbright WP7083SED/J3: https://www.kingbrightusa.com/images/catalog/SPEC/WP7083SED-J3.pdf
- Kingbright WP7083ZGD/G: https://www.kingbrightusa.com/images/catalog/SPEC/WP7083ZGD-G.pdf
- KT3102B technical family drawing: https://radioizba.ru/cat/PIC/415N0377318.pdf

## 6. Release blockers и ограничения

1. Завершить транскрипцию координат KT-1-7 в custom footprint КТ3102Б и проверить pad 1=B, pad 2=C, pad 3=E по заводскому рисунку.
2. Документально установить порядок физических контактов A1 Molex и соответствие pin 1 к VCC/DOUT/AOUT/GND. При отсутствии явного vendor drawing оставить TBC.
3. Для HA1 сохранить polarity TBC. Не менять pad mapping утверждённой E3 по предположению о типовом зуммере.
4. Для DA1 проверить функции 1…8 между symbol NE555D и физическим NE555P PDIP-8 в отдельной реализации.
5. Проверить ориентацию SA1 и геометрию монтажной панели в FreeCAD.
6. Пересчитать токи и мощности LED/резисторов по worst-case параметрам DA1 и выбранных LED.
7. Запустить KiCad 10.0.7 footprint checks для всех 19 назначений и PCB DRC после создания отдельной E3 PCB.
8. Оставить токовый лимит E4 и F1 TBC, пока нет гарантированного максимального тока A1 и согласованной модели источника. Не заменять отсутствующие данные физическими измерениями, поскольку они вне проекта.
9. Выбрать TVS по определённым критериям VBUS/ESD и документированному MPN.

Физическое изготовление, закупка, проверка образцов, обжим и лабораторные измерения не входят в текущий проект. Никакие статусы документа не подразумевают физическую приёмку.
