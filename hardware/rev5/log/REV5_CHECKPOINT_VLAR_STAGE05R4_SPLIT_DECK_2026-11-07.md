# Checkpoint VLAR — Stage05R4 Split-Deck modular enclosure

Дата: 2026-11-07  
Ветка: `design/usb-c-pcb-enclosure-r5`  
Исходная PCB: Stage04R3, неизменяемая.  
PCB SHA-256: `ac120c090f22f84342e3be6635b659c08afdf5558355b38c02d2e7035dfdc671`.

## Выполнено

1. Полностью заменена общая удлинённая оболочка Stage05R3 на архитектуру Split-Deck.
2. Построен отдельный электронный короб 65×70×28 мм и съёмная крышка 3 мм.
3. Построена самостоятельная открытая кассета MQ-4, крепящаяся к передней стенке двумя винтами M2. В кассете нет крыши/сетки над чувствительным элементом. Опорный бортик номинально 2 мм по периметру оценочного модуля 41×25 мм.
4. USB-C перенесён в сменную панель 20×14×2 мм. Окно 10.8×5.2 мм оставлено предварительным.
5. SA1 выполнен в виде ступенчатой сменной вставки с фланцем 17.2×12.2×0.8 мм и двумя винтами M1.6. Направление прорези пока не подтверждено реальным переключателем.
6. Добавлены два сменных световода HL1/HL2, акустические отверстия HA1 и кабельная втулка A1.
7. Подготовлены STEP детали, закрытая/сервисная/взрыв-сборка, восемь STL, чертежи и отдельные скрипты.

## Проверка посадки по PCB

По Stage04R3 footprint blocks проверены 25 references. Без смещения совпали J1, A1, HL1, HL2, HA1, SA1 и четыре точки MH1–MH4. Отчёт `STAGE05R4_PCB_DATUM_AUDIT.json`.

Case transform:
- `Xcase=52-(yPCB-123.5)`
- `Ycase=5.5+(xPCB-168.5)`
- `Zcase=6.4+Zboard`

## Валидация

- 52/52 checks PASS, 0 FAIL.
- 8/8 STL watertight, winding-consistent, one component.
- Все экспортированные STEP BREP re-import и solid-count checks PASS.
- Объёмные пересечения для основных узлов равны нулю при используемых упрощённых reference-моделях.
- ZIP CRC PASS. В SHA manifest 44 файлов. ZIP SHA-256: `6b370ea5381fcc663303474600a78a95cbf4e51f25ff8fe12a04bff8882f5f78`.

## Ограничения

- Native FreeCAD 1.1.x recompute и сохранение FCStd здесь не выполнялись. Макрос создаёт Housing, Closed Assembly, Service Assembly и Exploded Assembly.
- BREP объекты в FCStd — editable imported shapes, не полноценная история sketch constraints.
- PCB STEP упрощённый и не содержит дорожек/меди/vias.
- SEN-MQ4-V2 internal STEP geometry оценочная.
- Exact GCT USB4105 suffix/plug clearance не подтверждены.
- NKK AS11AP actuator axis/slot pending physical check.
- Не выполнялись печать, физическая сборка, тепловой/газовый тест, ingress или durability.

## OneDrive

Папка: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sb995a379d890428daa116d62d08965fa  
ZIP: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sbee3c9b863624278839e68f9866b4323  
FreeCAD macro: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sef8f81d3cd0a4c0d8478190539087a75
