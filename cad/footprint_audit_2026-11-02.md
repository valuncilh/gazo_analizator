# Документальный аудит элементной базы и footprints E3/E4

**Дата:** 02.11.2026  
**Рабочая ветка:** `analysis/vendor-behavioral-reconciliation`  
**Основа E3:** утверждённая схема `gost_e3_approved-2026-11-01` и неизменяемый XML-netlist blob `b24384b2e1b39068b3a11c9e11554cd4dc406b57`.  
**Объём:** документальная и CAD-проверка. Физическое изготовление, закупка, сборка и лабораторные измерения в этот проектный объём не входят.

## 1. Вывод аудита

Для всех 19 позиций утверждённой E3 определены физические кандидаты и/или библиотечные footprints. Для VT1 создан отдельный чертёжный footprint DRAFT по корпусу KT-1-7. Его pad map привязан к symbol pins 1=B, 2=C, 3=E. Размерная трактовка верхнего вида ещё не полностью закрыта, поэтому footprint не является fabrication-ready. Для VD1 выбран стандартный DO-35 footprint, геометрически близкий к паспорту КД510А, с правильной стороной pad 1=K.

Доступность библиотек и 3D-моделей проверена в KiCad 10.0.7. Пользователь подтвердил отображение Molex 53261-0471 и GCT USB4105 в 3D-просмотрщике, а также визуальный просмотр 2D-посадочных мест. Это подтверждает загрузку моделей и библиотечных объектов, но не геометрическую совместимость с реальными компонентами.

**Итоговый статус P2: PARTIAL.** Документальный выбор большинства компонентов выполнен. Полная проверка pad numbering, footprint DRC, соответствие всех 19 корпусов и окончательная механическая увязка остаются открытыми.

## 2. Неизменяемая электрическая база

В аудит включена только утверждённая E3:
- 19 компонентов.
- 15 сетей.
- 47 подключённых выводов.
- A1.3 остаётся отдельной сетью `/AOUT`.
- C3.2 и SA1.2 остаются отдельной сетью `Net-(SA1-B)`.
- В E3 не добавляются U2, P1, RHYS, VT2, R8 или R9.

Аудит footprints не изменяет утверждённую схему и XML-netlist. Все дальнейшие назначения полей Footprint выполняются только в отдельной реализации E3.

## 3. Реестр 19 компонентов E3

| Ref | Физический кандидат | Footprint-кандидат | Документальный результат | Статус |
|---|---|---|---|---|
| A1 | Joy-IT SEN-MQ4-V2, внешний модуль | `Connector_Molex:Molex_PicoBlade_53261-0471_1x04-1MP_P1.25mm_Horizontal` | Модуль имеет 4-контактный интерфейс. Для платы E3 выбран 4-circuit PicoBlade, 1.25 mm. Геометрия посадочного места и 3D-модель загружаются. Паспорт не даёт однозначной нумерации физических контактов Molex относительно VCC/DOUT/AOUT/GND. | SELECTED / pin map TBC |
| C1 | Multicomp Pro MCGLR16V476M5X11, 47 µF, 16 V | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | Паспортный корпус Ø5 × 11 mm, pitch 2 mm, ±20 %, -55…+105 °C. Геометрия соответствует footprint-кандидату. Проверить полярность pad 1 и обозначение на схеме в отдельной реализации. | CANDIDATE |
| C2 | Yageo CC0805KRX7R9BB104, 100 nF, 50 V, X7R, 10 % | `Capacitor_SMD:C_0805_2012Metric` | Корпус 0805, рабочий температурный диапазон по документации компонента покрывает проектный. | CANDIDATE |
| C3 | Multicomp Pro MCGLR16V476M5X11, 47 µF, 16 V | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | Тот же MPN и корпус, что C1. Сеть C3.2–SA1.2 должна остаться изолированной от Earth и /VCC. | CANDIDATE |
| DA1 | Texas Instruments NE555P, PDIP-8 | `Package_DIP:DIP-8_W7.62mm` | Температура 0…+70 °C покрывает утверждённые +10…+35 °C. В утверждённой E3 символ `Timer:NE555D` имеет графику SOIC-8, а физический кандидат NE555P — PDIP-8. Номера и функции выводов 555 должны быть сверены в отдельной реализации. | SELECTED / symbol-footprint review |
| HA1 | Ningbo Kepo HCM1206X, drawing OEM2690R | `GazoE3:HCM1206X_P7.6mm` | Чертёж: Ø12 × 9.5 mm, шаг 7.6 ±0.2 mm, выводы Ø0.6 mm. Температура работы -25…+70 °C покрывает проектный диапазон. Для worst-case бюджета сохраняется 40 mA при 6 V. Общая таблица семейства расходится по току и рабочему напряжению. Физический вывод, соответствующий золотой метке «+», документально не определён однозначно. | CANDIDATE / polarity TBC |
| HL1 | Kingbright WP7083SED/J3, красный 5 mm LED | `LED_THT:LED_D5.0mm` | Корпус T-1¾, шаг выводов 2.54 mm, отверстия Ø0.9 mm по рекомендациям изготовителя. Стандартный footprint имеет геометрию 5 mm / 2.54 mm. Катод и pad 1 проверить по рисунку вывода и символу. | CANDIDATE |
| HL2 | Kingbright WP7083ZGD/G, зелёный 5 mm LED | `LED_THT:LED_D5.0mm` | Корпус и шаг соответствуют HL1. Температурный диапазон семейства -40…+85 °C покрывает проектный. | CANDIDATE |
| R1 | Yageo RC0805FR-07160KL, 160 kΩ, 1 %, 0.125 W | `Resistor_SMD:R_0805_2012Metric` | Корпус 0805. Геометрия соответствует стандартному footprint. | CANDIDATE |
| R2 | Yageo RC0805FR-0713KL, 13 kΩ, 1 %, 0.125 W | `Resistor_SMD:R_0805_2012Metric` | Корпус 0805. Геометрия соответствует стандартному footprint. | CANDIDATE |
| R3 | Yageo RC0805FR-072KL, 2 kΩ, 1 %, 0.125 W | `Resistor_SMD:R_0805_2012Metric` | Корпус 0805. Геометрия соответствует стандартному footprint. | CANDIDATE |
| R4 | Yageo RC0805FR-078K2L, 8.2 kΩ, 1 %, 0.125 W | `Resistor_SMD:R_0805_2012Metric` | Корпус 0805. Геометрия соответствует стандартному footprint. | CANDIDATE |
| R5 | Yageo RC0805FR-078K2L, 8.2 kΩ, 1 %, 0.125 W | `Resistor_SMD:R_0805_2012Metric` | Корпус 0805. Геометрия соответствует стандартному footprint. | CANDIDATE |
| R6 | Yageo RC0805FR-07220RL, 220 Ω, 1 %, 0.125 W | `Resistor_SMD:R_0805_2012Metric` | Корпус 0805. Ток HL1 зависит от UOH DA1 и Vf выбранного LED. | CANDIDATE / load calculation |
| R7 | Yageo RC0805FR-07220RL, 220 Ω, 1 %, 0.125 W | `Resistor_SMD:R_0805_2012Metric` | Корпус 0805. Используется в ветвях, которые необходимо проверять по фактической топологии E3, не по старой схеме U2/VT2. | CANDIDATE / load calculation |
| SA1 | NKK AS11AP, SPST ON-NONE-OFF, straight PC terminals | `GazoE3:NKK_AS11AP_SPST_P5.08mm` | Для исполнения AS11 используются физические terminal 1 и 3, terminal 2 отсутствует. Pad 1 соответствует terminal 1, pad 2 — terminal 3. Шаг 5.08 mm. Температурный диапазон -30…+85 °C покрывает проектный. Нужна проверка ориентации актуатора в CAD-корпусе. | CANDIDATE |
| VD1 | КД510А, стеклянный осевой диод | `Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal` | Чертёж КД510А: корпус 3.8×1.9 mm, выводы Ø0.5 mm. Стандартный DO-35 footprint KiCad описан как 4×2 mm, pitch 7.62 mm, drill 0.8 mm. Исходный footprint содержит pad 1=K и pad 2=A, что соответствует утверждённому символу E3. Размеры близкие, KiCad 10 local check pending. | CANDIDATE / pad map reviewed |
| VT1 | КТ3102Б без суффикса М, металлостеклянное исполнение | `GazoE3:KT3102B_KT1-7_DWG_DRAFT` | Чертёжный кандидат: body Ø4.95 mm, max envelope Ø5.8 mm, h=5.3 mm, leads Ø0.45 mm × 13.5 mm. Pad 1=B, pad 2=C, pad 3=E. Координаты верхнего вида: pad1=(+0.8,-0.96177), pad2=(0,+1.25), pad3=(-0.8,-0.96177). Они построены по интерпретации PCD Ø2.5 mm и верхнего pin pitch 1.6 mm. Размер 1.2 mm из рисунка ещё требует независимой проверки. Старый TO-92 footprint неприменим. | DRAFT / coordinate review TBC |
| XS1 | Molex PicoBlade 53261-0271, 2 circuits, 1.25 mm | `Connector_Molex:Molex_PicoBlade_53261-0271_1x02-1MP_P1.25mm_Horizontal` | 2-circuit right-angle SMT header. Библиотека и 3D-модель доступны. Pin 1=/VCC, pin 2=Earth согласно E3. | SELECTED / cable map TBC |

## 4. Проверка климатических условий

Пользователь утвердил +10…+35 °C и 20–80 % RH без конденсации.

| Узел | Документированный диапазон | Оценка относительно проекта |
|---|---|---|
| DA1 NE555P | 0…+70 °C | Температура покрывает проектный диапазон |
| VT1 КТ3102Б | Для семейства указан диапазон -40…+85 °C | Температура покрывает проектный диапазон, точная редакция паспорта требует учёта при выпуске |
| HA1 HCM1206X OEM2690R | -25…+70 °C | Температура покрывает диапазон. В паспорте электрические/акустические тесты указаны при 15…35 °C и 25–85 % RH, поэтому характеристики на краях проектной влажности и при +10…+15 °C не гарантируются указанным тестовым условием |
| SA1 NKK AS11AP | -30…+85 °C | Температура покрывает диапазон. Влажностное испытание есть в серии AS, но это не подтверждение IP-защиты корпуса |
| R1–R7 Yageo RC0805FR | -55…+155 °C для семейства | Температурный диапазон покрывает проектный |
| C1/C3 Multicomp Pro | -55…+105 °C | Температурный диапазон покрывает проектный |
| C2 Yageo X7R | -55…+125 °C | Температурный диапазон покрывает проектный |
| HL1/HL2 Kingbright | -40…+85 °C | Температурный диапазон покрывает проектный |
| Molex 53261 series | -40…+105 °C | Температурный диапазон покрывает проектный |
| USB-C GCT USB4105 | -40…+85 °C | Температурный диапазон покрывает проектный |
| A1 Joy-IT SEN-MQ4-V2 | Доступный паспорт не задаёт однозначного предельного диапазона эксплуатации | TBC. Наличие графиков зависимости от температуры и влажности не является пределами допустимой эксплуатации |
| VD1 КД510А | −60…+85 °C по datasheet КД510А | Температурный интервал покрывает проектные +10…+35 °C | PASS (temperature only) |

**Вывод:** документально подтверждено покрытие температуры для большей части выбранной элементной базы. Полная климатическая совместимость изделия пока не доказана из-за отсутствия однозначных пределов для Joy-IT SEN-MQ4-V2, уточнения по КД510А и ограничений по условиям гарантирования акустических характеристик HA1. Утверждение климатических условий не превращает эти TBC в PASS.

## 5. Molex: кабельные ответные части

Для двух кабельных соединений нельзя ограничиваться только платными header footprints.

Кандидатные ответные части Molex PicoBlade:
- `51021-0400` — корпус на 4 circuits для соединения сенсорного модуля с A1 на E3.
- `51021-0200` — корпус на 2 circuits для соединения выхода E4 с XS1 на E3.
- `50058-8000` — female crimp terminal, совместимость с конкретным сечением жилы и обжимным инструментом проверить по документации Molex.

Предварительное количество для кабеля с разъёмами на обоих концах:
- A1: 2 корпуса 51021-0400 и 8 контактов 50058-8000.
- E4↔XS1: 2 корпуса 51021-0200 и 4 контакта 50058-8000.

Это BOM candidates для кабельной сборки, а не закупочная спецификация. Длина кабелей, сечение проводников, цветовая маркировка, способ фиксации и точная ориентация pin 1 ещё не заданы. Существование одинакового номера семейства разъёма само по себе не доказывает ориентацию жгута.

## 6. Отдельная элементная база E4

| Позиция | Кандидат | Статус |
|---|---|---|
| USB1 | GCT USB4105-GF-A, footprint `Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal` | SELECTED candidate. Для суффикса GF-A принять исходную длину shell stake 0.95 mm, сверить точный drawing revision с footprint |
| R_CC1, R_CC2 | 5.1 kΩ, 1 %, 0603, каждый CC pin отдельным резистором на GND | Номинал/типоразмер выбраны. Точный MPN и посадочные места требуют закрепления |
| D_TVS | TVS для VBUS 5 V | MPN не выбран. Обосновать рабочее напряжение, ёмкость, surge rating и размещение |
| F1 | eFuse или PTC | MPN не выбран. Токовый бюджет остаётся BLOCKED из-за отсутствия максимального полного тока A1 в паспорте и отсутствия физического измерения в объёме проекта |
| J_OUT | Molex PicoBlade 53261-0271, 2 circuits | SELECTED candidate. Выход pin 1=protected +5 V, pin 2=GND, согласовать с XS1 E3 |

CC1 и CC2 не объединять. USB PD не применяется. Нельзя предполагать, что источник объявляет 1.5 A или 3 A. Обе ориентации USB-C plug должны быть корректны по симметричной разводке VBUS/GND и независимым CC termination.

## 7. Что проверено в KiCad и что ещё нет

**Проверено по предоставленным скриншотам и результатам пользователя:**
- глобальная переменная `KICAD10_3DMODEL_DIR=/usr/share/kicad/3dmodels/`;
- путь проектной библиотеки `Connector_Molex`;
- загрузка и отображение 3D-моделей Molex PicoBlade 53261-0471 и GCT USB4105;
- визуальный 2D-осмотр pad layouts обоих разъёмов.

**Ранее сообщённые source/library checks:**
- экспорт в SVG двух custom footprints GazoE3;
- экспорт стандартных символов и footprints таймера, пассивов и разъёмов;
- source-level checker двух custom footprints.

**Не выполнено или не подтверждено:**
- нативный KiCad footprint checker для всех назначений;
- окончательная сверка pad 1/pin 1 по каждому компоненту;
- полный отдельный проект E3 implementation;
- schema-to-board netlist parity;
- PCB DRC, трассировка и проверка непрерывности полигонов;
- 3D-сборка всей платы с корпусом и кабелями;
- FreeCAD collision/clearance review.

Сообщение KiCad об отсутствующей `design-block-lib-table` не относится к проверке посадочных мест или 3D-моделей и не является блокером данного этапа.

## 8. Ограничения и запрещённые выводы

1. Не объявлять физическую посадку, обжим, полярность кабеля или механическую прочность подтверждёнными. В текущем проекте нет образцов и испытаний.
2. Не заявлять полный ток изделия ≤300 mA как доказанный. Joy-IT не публикует максимальный полный ток платы сенсора.
3. Не выбирать F1 только по желаемому пределу 300 mA. Расчёт должен опираться на доступные гарантированные параметры источника, разъёма, кабеля и нагрузки.
4. Не переносить старый корпус и старую PCB 72×50 mm на текущую конфигурацию.
5. Не изменять approved E3 и её XML-netlist.
6. Не превращать статус footprint source PASS в KiCad DRC PASS.

## 9. Следующие действия P2

1. Проверить размерную трактовку 1.2 mm callout в верхнем виде KT3102(A–Д) и закрыть coordinates of KT3102B draft. Не использовать TO-92.
2. Сверить DO-35 footprint КД510А в KiCad 10.0.7, сохранить pin1=K, pin2=A.
3. Проверить pad numbering и ориентацию всех стандартных и custom footprints средствами KiCad 10.0.7.
4. Сверить символ/footprint DA1 NE555P PDIP-8 в отдельной реализации E3.
5. Зафиксировать Molex cable housing/crimp terminal candidates и оформить длины/сечения как отдельные параметры проекта.
6. Обновить footprint register и pad-to-net register без изменения утверждённого XML.
7. Только после этого создавать placement board для E3.


## 10. Источники и прослеживаемость

- Joy-IT SEN-MQ4-V2: [страница изделия](https://joy-it.net/en/products/SEN-MQ4-V2), [datasheet EN, 2026-01-15](https://joy-it.net/files/files/Produkte/SEN-MQ4-V2/SEN-MQ4-V2_Datasheet-EN_2026-01-15.pdf).
- Molex PicoBlade 53261-0471: [официальная страница](https://www.molex.com/en-us/products/part-detail/532610471). 53261-0271: [официальная страница и PDF](https://www.molex.com/en-us/products/part-detail/532610271?display=pdf). Кабельные housings 51021-0400/0200 и female crimp terminal 50058-8000: [каталог Molex PicoBlade](https://www.molex.com/en-us/products/connectors/wire-to-board-connectors/picoblade-connectors).
- Texas Instruments NE555P: [страница точного исполнения](https://www.ti.com/product/NE555/part-details/NE555P), [datasheet](https://www.ti.com/lit/ds/symlink/ne555.pdf).
- GCT USB4105-GF-A: [официальная страница и datasheet](https://gct.co/connector/usb4105), [габаритный чертёж](https://gct.co/files/drawings/usb4105.pdf).
- NKK AS11AP: [страница точного исполнения](https://www.nkkswitches.com/wp-content/themes/impress-blank/search/inc/part.php?part_no=AS11AP), [Series AS datasheet](https://www.nkkswitches.com/pdf/Aslides.pdf).
- Yageo RC0805FR: [datasheet family](https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-07160KL). Yageo C2 CC0805KRX7R9BB104: [страница компонента](https://www.yageo.com/en/Product/Index?key=CC0805KRX7R9BB104).
- Multicomp Pro MCGLR16V476M5X11: [каталог производителя/дистрибьютора с datasheet-параметрами](https://cpc.farnell.com/multicomp-pro/mcglr16v476m5x11/capacitor-47uf-16v-radial-105/dp/CA08260).
- Kingbright WP7083SED/J3 red: [datasheet](https://www.kingbrightusa.com/images/catalog/SPEC/WP7083SED-J3.pdf). WP7083ZGD/G green: [datasheet](https://www.kingbrightusa.com/images/catalog/SPEC/WP7083ZGD-G.pdf).
- Ningbo Kepo HCM1206X OEM2690R: [model-specific drawing/specification](https://kvarci.ru/files/files/HCM1206X%3DDAP1206X%5BOEM2690%5D.pdf). Различия с общей таблицей HCM12X оставлены в разделе 3 и не скрыты.
- КТ3102A/Б/В/Д and M suffix variants: [family technical sheet](https://radioizba.ru/cat/PIC/415N0377318.pdf), [Goldomedov et al., Small-Signal Transistors Handbook, 1989, scanned page 112–113](https://djvu.online/jpg1/j/T/i/jTiCg7zNvKMqH/058.webp). Чертёж различает металлостеклянный вариант без «М» и пластиковый вариант с «М». Более поздняя листовка КТ3102A–Д даёт явную размерную схему и pin labels: [Radioizba PDF](https://radioizba.ru/cat/PIC/415N0377318.pdf).
- КД510А: [datasheet КД509А/КД510А](https://static.chipdip.ru/lib/249/DOC000249243.pdf) указывает стеклянный корпус 3.8×1.9 mm, leads Ø0.5 mm и маркировочные полосы со стороны катода. [Справочник 1983](https://www.elec.ru/files/2025/01/24/Sprv-DTO.pdf) описывает семейство 2Д510А/КД510А в металлостеклянном исполнении. Библиотечная геометрия сверена по исходнику KiCad: [D_DO-35_SOD27_P7.62mm_Horizontal](https://sources.debian.org/src/kicad-footprints/9.0.2-1/Diode_THT.pretty/D_DO-35_SOD27_P7.62mm_Horizontal.kicad_mod).

**P2 не закрывается, пока все 19 символов не имеют документированного footprint status, pad mapping и понятного ограничения. P3 не начинается до фиксации этого реестра.**


## 11. Drawing-derived footprint update — 02.11.2026

### VT1 — КТ3102Б, корпус KT-1-7

В рабочую библиотеку добавлен файл:

`cad/kicad/footprints/GazoE3.pretty/KT3102B_KT1-7_DWG_DRAFT.kicad_mod`

Использована размерная схема металлостеклянного КТ3102(A–Д), в которую входит Б. Кандидатная геометрия корпуса: Ø4.95 mm, максимальная оболочка Ø5.8 mm, высота 5.3 mm, гибкие выводы Ø0.45 mm, длина 13.5 mm. Распиновка в верхнем виде: Emitter, Base, Collector. Символ утверждённой E3 имеет pin 1=B, pin 2=C, pin 3=E. Поэтому draft footprint использует pad 1=B, pad 2=C, pad 3=E.

Текущая координатная интерпретация чертежа задаёт upper pin pitch 1.6 mm и positioning circle Ø2.5 mm: pad 1=(+0.8,-0.96177), pad 2=(0,+1.25), pad 3=(-0.8,-0.96177). На рисунке присутствует дополнительный размер 1.2 mm, который пока не удалось однозначно отнести к координатам центров выводов. По этой причине файл является DRAFT: он годится для дальнейшей CAD-оценки и проверки в KiCad, но не для fabrication release. Следующая задача — сверить размер 1.2 mm с исходным видом/датумом и при необходимости скорректировать координаты.

### VD1 — КД510А, DO-35

Для КД510А найден datasheet с габаритами стеклянного корпуса 3.8×1.9 mm и выводами Ø0.5 mm. Стандартный KiCad footprint `Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal` описывает корпус 4×2 mm, pitch 7.62 mm, отверстия Ø0.8 mm. Это близкий размерный кандидат. Исходный файл KiCad помечает pin 1 как K (cathode), pin 2 — A (anode). Это соответствует E3 symbol: VD1.1=K, VD1.2=A. В E3 pad 1 остаётся в `Net-(HA1-Pin_1)`, pad 2 — в `Net-(DA1-OUT)`.

КД510А обозначается цветными полосами со стороны катодного вывода. Этот факт записан как документальная подсказка ориентации, но не используется для изменения нумерации symbol/footprint. KiCad 10 local validation остаётся pending.

**P2 remains PARTIAL.** VT1 has draft footprint, VD1 has a library candidate. All assigned footprints still require KiCad 10 checks and pad-to-net review. Physical fit is not claimed.
