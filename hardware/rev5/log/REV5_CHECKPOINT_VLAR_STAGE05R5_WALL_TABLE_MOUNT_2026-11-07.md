# Checkpoint VLAR — Stage05R5 Wall/Table Mount

Дата: 2026-11-07.  
Ветка: `design/usb-c-pcb-enclosure-r5`.  
Статус: CAD статически проверен, native FreeCAD/physical fit pending.

## Принятые пользовательские требования

1. Использовать уточнённую STL-модель основной PCB и точную STEP-сборку SEN-MQ4-V2.
2. Основной корпус и удалённый сенсорный модуль должны независимо крепиться к стене или столу.
3. У каждого модуля своя отдельная съёмная крышка на винтах.
4. Сенсорная плата крепится через четыре её штатных отверстия. Над сенсорной крышкой должна выступать только металлическая головка/защитная решётка MQ-4.
5. USB-C — только прямоугольное отверстие в стенке корпуса, без вставки или декоративной рамки.
6. На лицевой стороне основной крышки разрешены только надпись «Детектор метана» и `CH4` в шестиугольнике.

## Использованные исходники

- Corrected main PCB STL SHA-256: `0a6489358d9ff5d8a8fbd0f9e5916dcffeefa2e925c6cb4ce9a08b2220c7703b`.
- SEN-MQ4-V2 STEP SHA-256: `d064355fa01dd6ed99a5886260bc3dadf1f246ba39076c1bb64b40fadc283ee7`.
- Stage04R3 PCB SHA-256: `ac120c090f22f84342e3be6635b659c08afdf5558355b38c02d2e7035dfdc671`.

## Техническая реализация

- Main enclosure: 73.5×88×27.2 мм, крышка 4×M2.5, четыре отверстия M3 surface mount.
- Sensor enclosure: 42×63×15 мм, крышка 4×M2.5, четыре отверстия M3 surface mount.
- Sensor PCB 25×35×1.6 мм, holes Ø2.8 мм at source coordinates (3,3), (22,3), (3,32), (22,32). Four M2 screws mount it to dedicated bosses.
- Sensor lid hole Ø18 mm. All solids passing above lid plane fit within a 7.99mm radial envelope; opening radius9mm. Head projection 9.049mm.
- USB-C direct aperture 10.8×5.2 mm, no bezel or insert.
- Cover front marking only: “Детектор метана” and hexagon containing CH4.
- Main and sensor module wall/table mount datums use 4×M3 clearances per module.

## Validation

- BREP/layout/clearance/mechanical datum checks: 28/28 PASS.
- STEP round-trip: 10/10 PASS.
- Four enclosure print parts: 4/4 watertight, winding consistent, one connected component each.
- Main PCB user STL: 3321 components, non-watertight mesh assembly. Retained as mesh reference only.
- Exact sensor STEP: 189 solids; no volumetric overlap with sensor base/lid in current model.
- ZIP integrity CRC PASS, 44 entries. ZIP SHA-256: `89cfc341d6b7b292881dfd4da45ec5cfc5d60ebf566824ec01792804d2c963a4`.

## Not done

- Native FreeCAD 1.1.x recompute and FCStd creation. Macro is syntax-checked only.
- Physical screw, wall/table anchor, connector/plug fit and sensor PCB clearance tests.
- Print, gas response, heater thermal, cable harness, ingress and durability tests.
- SA1 remains inside because no exterior opening is permitted on the main lid. HL1/HL2 are hidden under the lid unless lid material is translucent or a separate side-indication solution is later approved.

## OneDrive

Folder: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s2c2692908c724ca5944f2ec5af91ee41  
ZIP: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s105514d13c294afeb2b2daaa3b26f035  
FreeCAD macro: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s8cb56fe821794ecd85a1055fd7e02440
