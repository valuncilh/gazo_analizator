# Карта соединений утверждённой электрической схемы E3

<badge color="success">APPROVED E3</badge>

**Назначение:** текстовое представление фактических групп соединений, извлечённых из утверждённого XML-netlist. Документ нужен для поиска сигналов, проверки визуальной топологии и навигации по схеме.

## Первоисточники

| Артефакт | Ссылка |
|---|---|
| Нативная схема KiCad | [gazo_analizator_E3_GOST_itog.kicad_sch](../../cad/project_modification/gost_e3_final/gazo_analizator_E3_GOST_itog.kicad_sch) |
| XML-netlist | [netlist_current.xml](../../cad/project_modification/gost_e3_final/reports/kicad10/netlist_current.xml) |
| Паспорт утверждённой редакции | [APPROVED_BASELINE.md](../../cad/project_modification/gost_e3_final/APPROVED_BASELINE.md) |
| Отчёт ERC | [erc_current.rpt](../../cad/project_modification/gost_e3_final/reports/kicad10/erc_current.rpt) |
| Git tag | [gost-e3-approved-2026-11-01](https://github.com/valuncilh/gazo_analizator/tree/gost-e3-approved-2026-11-01) |

**SHA blob утверждённого KiCad-файла:** \`2e17299ba8a9aeeb0ce5e6c06562fe4e0fd84ba0\`.  
**SHA blob XML-netlist:** \`b24384b2e1b39068b3a11c9e11554cd4dc406b57\`.

## Полный список сетей

В утверждённом XML-netlist содержится 15 сетей: 14 многовыводных групп и отдельный одиночный вывод AOUT.

| № | Имя сети | Выводы, входящие в сеть |
|---:|---|---|
| 1 | \`/AOUT\` | A1.3 |
| 2 | \`/VCC\` | A1.1, C3.1, DA1.8, HL2.2, R1.1, R3.2, R4.2, XS1.1 |
| 3 | \`Earth\` | A1.4, C1.2, C2.2, DA1.1, HL1.1, VT1.3, XS1.2 |
| 4 | \`Net-(A1-Pin_2)\` | A1.2, R1.2, R2.1 |
| 5 | \`Net-(DA1-CONT)\` | C2.1, DA1.5 |
| 6 | \`Net-(DA1-DISCH)\` | DA1.7, R4.1, R5.1 |
| 7 | \`Net-(DA1-OUT)\` | DA1.3, R6.1, VD1.2 |
| 8 | \`Net-(DA1-THRES)\` | C1.1, DA1.2, DA1.6, R5.2 |
| 9 | \`Net-(DA1-~{RST})\` | DA1.4, R3.1, VT1.2 |
| 10 | \`Net-(HA1-Pin_1)\` | HA1.1, VD1.1 |
| 11 | \`Net-(HA1-Pin_2)\` | HA1.2, R7.1, SA1.1 |
| 12 | \`Net-(HL1-A)\` | HL1.2, R6.2 |
| 13 | \`Net-(HL2-K)\` | HL2.1, R7.2 |
| 14 | \`Net-(SA1-B)\` | C3.2, SA1.2 |
| 15 | \`Net-(VT1-B)\` | R2.2, VT1.1 |

## Контрольные замечания

1. **AOUT.** A1.3 остаётся отдельным выходом измерения. В утверждённой редакции он не соединён с GND, DOUT или другими сетями.
2. **Earth.** C3.2 и SA1.2 образуют отдельную сеть \`Net-(SA1-B)\`. Она не является общим проводом.
3. **Сброс DA1.** DA1.4, R3.1 и VT1.2 входят в одну сеть \`Net-(DA1-~{RST})\`.
4. **Времязадающий узел.** DA1.2, DA1.6, C1.1 и R5.2 входят в одну сеть \`Net-(DA1-THRES)\`.
5. **Выход DA1.** DA1.3 соединён с R6.1 и VD1.2. VD1.1 соединён с HA1.1.
6. **Питание.** XS1.1 является входом \`/VCC\`, XS1.2 — \`Earth\`. USB-C E4 остаётся отдельной платой, не частью утверждённой Э3.

## Границы визуализации

[Функционально-связевая SVG-схема](e3_approved_topology.svg) является дополнительным видом по XML-netlist. Она помогает читать состав и связи, но не воспроизводит координаты символов, геометрию проводников и оформление исходного листа KiCad. Для проверки графики и выпуска документа используется нативный файл \`.kicad_sch\`.
