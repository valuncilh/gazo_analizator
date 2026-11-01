# Реестр физических исполнений и footprints — 01.11.2026

**Электрическая база:** утверждённая E3, коммит 683e53410de5f1a960c9e060061119f843cc2c51. Утверждённый файл схемы не изменяется.

## 1. A1, XS1 и USB-C E4

| Позиция | Физический компонент | MPN / тип | Footprint KiCad | Статус |
|---|---|---|---|---|
| A1 | Joy-IT SEN-MQ4-V2, кабельный интерфейс | Molex 53261-0471, 4 circuits, 1.25 mm | Connector_Molex:Molex_PicoBlade_53261-0471_1x04-1MP_P1.25mm_Horizontal | Выбран. Pin 1 и жгут подтвердить прозвонкой |
| A1 | Сенсорный модуль | Joy-IT SEN-MQ4-V2 | Внешний модуль, отдельное крепление по четырём отверстиям Ø2.9 mm | Выбран. Механическую посадку проверить на образце |
| XS1 | Вход основной E3 платы от E4 | Molex 53261-0271, 2 circuits, 1.25 mm | Connector_Molex:Molex_PicoBlade_53261-0271_1x02-1MP_P1.25mm_Horizontal | Выбран. Полярность кабеля проверить |
| USB1 / E4 | USB-C receptacle | GCT USB4105-GF-A | Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal | Кандидат. Проверить shell stakes и footprint KiCad 10 |
| R_CC1, R_CC2 / E4 | Rd termination | 5.1 kΩ, 1% | Resistor_SMD:R_0603_1608Metric | Номинал и корпус выбраны, точный MPN не назначен |
| F1 / E4 | Ограничитель тока VBUS | eFuse или PTC | Не назначен | BLOCKED до измерений тока |
| D_TVS / E4 | Защита VBUS | TVS для USB 5 V | Не назначен | BLOCKED до выбора MPN и расчёта |

## 2. Основные компоненты E3

| Позиция | Выбранный кандидат | Footprint KiCad | Состояние и ограничения |
|---|---|---|---|
| DA1 | Texas Instruments NE555P, PDIP-8 | Package_DIP:DIP-8_W7.62mm | Активный PDIP-8 вариант 0…+70 °C. Текущий выбор физического корпуса не меняет символ NE555D и значение NE555N в утверждённой E3. Согласовать температурный диапазон устройства. |
| VT1 | КТ3102Б без суффикса М | Не назначен | Металлостеклянный корпус с гибкими выводами. Старый KT-26/TO-92 footprint запрещён. Нужен образец для измерения отверстий и ориентации pin 1/B, pin 2/C, pin 3/E. |
| HA1 | Ningbo Kepo HCM1206X, drawing OEM2690R | GazoE3:HCM1206X_P7.6mm | Model-specific OEM2690R: 6 V rated, 4…8 V, 40 mA max at 6 V, SPL 88 dB/10 cm. General HCM12X sheet conflicts (4…7 V, 30 mA). Use 40 mA for worst-case current, conservative voltage intersection 4…7 V and temperature intersection −25…+70 °C until supplier confirms delivered variant. Geometry Ø12 × 9.5 mm, pitch 7.6±0.2 mm, leads Ø0.6 mm. Verify positive lead on sample. |
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

## 3. Собственная библиотека GazoE3

Расположение: cad/kicad/footprints/GazoE3.pretty. Проектная таблица библиотек добавлена рядом с утверждённой E3 в cad/project_modification/gost_e3_final/fp-lib-table.

Созданы два footprint-кандидата:
- HCM1206X_P7.6mm — физическая геометрия из чертежа Ningbo Kepo OEM2690R. Pad 1/2 соответствуют HA1.1/HA1.2, полярность не кодируется до проверки образца.
- NKK_AS11AP_SPST_P5.08mm — прямые выводы с межцентровым расстоянием 5.08 mm. Pad 1/2 соответствуют физическим контактам 1/3 switch.

KT3102Б footprint намеренно не создавался. Паспорт подтверждает металлостеклянный корпус и гибкие выводы, но точную ориентацию и центры выводов необходимо получить с физического транзистора или заводского размерного чертежа.

Source-level checker: cad/scripts/verify_gazo_e3_footprints.py. Он проверяет только исходный текст и координаты площадок, но не заменяет проверку в KiCad 10.

## 4. Источники

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

## 5. Release blockers

1. KT3102B manufacturer/sample and actual lead geometry.
2. A1 Molex pin 1, harness conductor order and DOUT output drive.
3. HA1 polarity mark corresponding to physical lead and measured current at 5 V. The specific HCM1206X datasheet gives up to 40 mA at 6 V; do not use the old generic 30 mA assumption.
4. DA1 temperature range against the final environmental requirement.
5. SA1 panel cutout/actuator orientation and mounting strength.
6. Verify current and power dissipation for LEDs and resistors in the full E3 circuit.
7. Verify all standard and custom footprints in KiCad 10.0.7; then DRC and physical sample fit.
8. Select E4 TVS/eFuse/PTC after measuring cold-start, warm-up, steady-state and alarm current.

No manufacturing release is implied by the register or the source footprint files.
