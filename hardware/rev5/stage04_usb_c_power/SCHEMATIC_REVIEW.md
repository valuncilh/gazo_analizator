# Stage04R1 schematic review

## Изменения

1. Удалён XS1 (`Connector_Generic:Conn_01x02`) и локальный старый символ Earth `#PWR06`.
2. Добавлен J1 USB-C с 16 контактами и shell pin SH.
3. Назначен footprint GCT USB4105.
4. Добавлены R8 и R9, 5,1 кОм, 0805.
5. A1 и существующая схема датчика/сигнализатора сохранены.
6. PWR_FLAG сети VCC сохранён.

## Сети и физические выводы

| Вывод | Соединение |
|---|---|
| A4/A9/B4/B9 | VCC |
| A1/A12/B1/B12 | Earth |
| SH | Earth |
| A5 CC1 | R8 pin 2 |
| R8 pin 1 | Earth |
| B5 CC2 | R9 pin 2 |
| R9 pin 1 | Earth |
| A6/A7/B6/B7 | NC |
| A8/B8 | NC |

Для стандартного `Device:R` pin 1 является нижним выводом символа, pin 2 — верхним. На PCB соблюдено соответствие: pad 1 = Earth, pad 2 = CCx.

## Структурный аудит

- 32 уникальных symbol references.
- 199 уникальных UUID.
- J1/R8/R9 присутствуют.
- XS1 отсутствует.
- Шесть NC-маркеров на D+/D−/SBU.
- Баланс S-expression проверен.

## Не выполнено

Native KiCad 10 Eeschema load/ERC, экспорт и сравнение netlist с PCB, symbol-to-footprint consistency check. Структурный аудит не заменяет native ERC.
