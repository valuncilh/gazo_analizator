# Этап 04R2 — перенос USB-C на длинную кромку

Исполнитель: VLAR. Дата: 07.11.2026.
Статус: статически проверенный кандидат, требуется native KiCad verification.

## Артефакты

- [Папка OneDrive](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s68ff8df4759942b4a786c38cd05060a9)
- [Полный ZIP](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sbf58dc5fbfc54506ba71e3176f5ff471)
- [Редактируемая PCB KiCad](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s89af74c7e0e246b8b73eb5461352af85)
- [Общий вид платы PNG](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s5d7f15f2c26e433f8d85bc33d33f60a9)
- [Деталь USB-C PNG](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sbbc18e2560ff460a97cbc67545196c2f)

## Суть изменения

USB-C GCT USB4105 перенесён с короткой стороны возле бывшего XS1 на верхнюю длинную кромку. Разъём ориентирован наружу, отдельно от A1. R8/R9 перенесены рядом с J1. Трассировка VBUS, GND/shell, CC1/CC2 завершена как статически проверенный кандидат.

## Числа

- Плата 59×45×1.6 мм, 2 слоя.
- J1 origin (196.0000, 126.6000), rotation 180°.
- Датум PCB Edge (196.0000,123.5000), совпадает с Edge.Cuts.
- 220 сегментов, 25 физических via.
- 25 footprint references, 908 UUID без дубликатов.
- Четыре M2 отверстия сохранены.

## Проверки и ограничения

Статические структурные, геометрические и топологические проверки PASS. Native ERC/DRC, Refill All Zones и 3D Viewer ещё не выполнялись. Экспорт STEP и FreeCAD-корпус пока не выполнялись. Не зафиксированы ток нагрузки во время прогрева SEN-MQ4-V2 и схема защиты входа.

См. `reports/PCB_STAGE04R2_REVIEW.md` и checkpoint в `hardware/rev5/log/`.
