# Этап 05R4 — корпус Split-Deck

Дата: 07.11.2026.  
Ветка: `design/usb-c-pcb-enclosure-r5`.  
Статус: preliminary mechanical candidate. Не выпуск для производства.

## Архитектура

Stage05R4 полностью заменяет внешнюю архитектуру Variant B Turtle из Stage05R3.

- Отдельный электронный короб 65×70×28 мм с самостоятельной крышкой толщиной 3 мм.
- Независимая съёмная открытая кассета MQ-4. Нет сплошной крыши, сетки или решётки над чувствительным элементом.
- Номинальный опорный буртик кассеты 2 мм по периметру оценочного габарита сенсорной платы.
- Сменная USB-C панель, сменная ступенчатая вставка SA1, два световода HL1/HL2, кабельный ввод A1 с отдельной втулкой.
- Общий габарит по CAD около 65×114×31 мм.

## Источник платы и датумы

Stage04R3 PCB сохранена без изменений. SHA-256: `ac120c090f22f84342e3be6635b659c08afdf5558355b38c02d2e7035dfdc671`.

Плата 59×45×1.6 мм. Четыре M2 датумы корпуса: (48,9), (48,61), (11,9), (11,61) мм. По исходному PCB точно пересчитаны J1 (48.9,33.0), A1 (35.5,10.0), HL1 (39.5,53.0), HL2 (39.5,46.0), HA1 (28.0,51.4), SA1 (13.2,49.0). 6 footprint datums + 4 M2 holes совпали без координатной ошибки: 10/10 PASS.

## Проверки

- 52/52 сводных проверок BREP, пересечений, STEP round-trip, STL topology и PCB datums PASS.
- 8/8 STL watertight, winding-consistent, по одному связному компоненту.
- ZIP integrity CRC PASS, 44 файлов учтены в SHA-256 manifest.
- PCB mechanical STEP — упрощённый reference без медных дорожек и vias.
- Native FreeCAD recompute/FCStd не запускался в среде подготовки. Макрос создаёт четыре FCStd в FreeCAD 1.1.x.

## Открытые ограничения

Точный ordering code GCT USB4105 и shell-stake suffix 060/095/120 не подтверждён. USB проём 10.8×5.2 мм предварительный. Ориентация физического движка NKK AS11AP также предварительная. Внутренние элементы STEP модели SEN-MQ4-V2 оценочные. Печать, физическая сборка, газовый отклик, температура нагревателя и влагозащита не испытывались. Нативные KiCad ERC/DRC/Refill ещё не подтверждены.

## OneDrive

- [Stage05R4 folder](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sb995a379d890428daa116d62d08965fa)
- [Full ZIP package](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sbee3c9b863624278839e68f9866b4323)
- [FreeCAD macro](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sef8f81d3cd0a4c0d8478190539087a75)
- [Closed assembly preview](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s8070dcc867b94110995297f7be3024f4)
- [PCB datum audit](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s10acf4d4200b498fbe1bf3142caa9ca1)

## Checksums

- ZIP Stage05R4: `6b370ea5381fcc663303474600a78a95cbf4e51f25ff8fe12a04bff8882f5f78`
- Closed assembly STEP: `cc646e56c6b6bf8f3ae25c751619fc125ca3eed8d26dbfbfcf16347d29986e62`
- Geometry validation: `f32b3b6e99f39078ac61f270d3fbf28c8031a35c388e6c80dbeaf723f272ac15`
- FreeCAD macro: `a2439ab4a6476c296ef6b3c3c877ea71cc8e491688bdcaf916b5f7262ad57b41`
