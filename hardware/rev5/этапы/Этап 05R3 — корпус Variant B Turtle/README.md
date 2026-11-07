# Этап 05R3 — корпус FreeCAD Variant B Turtle для PCB R3

Исполнитель: VLAR. Дата: 07.11.2026.
Статус: STEP/STL статически проверены; макрос FreeCAD готов; FCStd ожидают запуска в FreeCAD 1.1.x.

## OneDrive

- Папка Stage05R3: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sb1cfb4de66144227ab8e2f89e1d86737
- Полный ZIP: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s5ec2f86d9fc54eb2a98d5a10e64fc8f0
- Макрос FCStd: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s2ff2efe0e18840a5b9cc15ac610a8c85
- Габаритный чертёж: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s885ee2fba2704caabd3616606890ba2a
- Геометрический аудит: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sc98c2ce897584b8e9fb9bc7bb97af3d7

## Состав модели

Variant B Turtle: интегрированное основание, общая крышка, четыре M2 стойки, две направляющие сенсорного модуля, вентиляция MQ-4, USB-C окно на длинной стенке +X напротив A1.

Датумы: плата 59×45×1.6 мм; корпус 65×127×32.5 мм; M2 centres (48,9), (48,61), (11,9), (11,61) мм; J1 edge datum (52,33) мм; USB face-to-wall gap provisional 3.05 мм.

## Проверки

- 35/35 геометрических BREP/координатных/interference/STEP re-import checks PASS.
- 4/4 STL watertight и по одному компоненту на деталь.
- R2→R3 PCB fingerprint: изменены только R8/R9 rotations 180°, все механические координаты сохранены.
- ZIP CRC PASS, SHA-256 manifest covers 43 files.

## Создание FCStd

Запустить Нативный FreeCAD/Создать_нативные_документы_Stage05R3.FCMacro из FreeCAD 1.1.x. Макрос создаст четыре FCStd: Housing, Closed Assembly, Service Assembly, Exploded Assembly. Native recompute здесь не выполнялся, поскольку FreeCAD отсутствует. Объекты — editable imported BREP, не полноценная sketch-based history.

USB4105 exact suffix 060/095/120 не подтверждён. USB aperture provisional until exact CAD/part + plug fit. PCB reference STEP simplified and does not contain PCB R3 copper/vias. Sensor internal positions estimated.