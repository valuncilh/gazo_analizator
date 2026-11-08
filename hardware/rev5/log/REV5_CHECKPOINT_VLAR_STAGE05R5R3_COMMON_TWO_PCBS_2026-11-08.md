# Checkpoint VLAR — Stage05R5R3 unified two-PCB enclosure

Дата: 2026-11-08  
Ветка: `design/usb-c-pcb-enclosure-r5`  
Статус: geometry validated / native FreeCAD and physical checks pending.

## Пользовательская компоновка реализована

- Один общий корпус и одна общая съёмная крышка.
- Обе PCB находятся внутри одного корпуса и закреплены на одной высоте.
- A1 основной платы обращён к четырём штырькам сенсорной PCB.
- Между A1 и штырьками смоделирован короткий 4-жильный жгут. С A1 — Molex-family plug, с сенсорной стороны — четыре отдельные жилы до штырьков.
- На крышке только дуговая надпись «Детектор метана» вокруг головки MQ-4.
- USB-C — простое скруглённое отверстие в боковой стенке, без рамки/вставки.

## Механика

- Common base: 50.8×121.0 mm, wall height 20.0 mm.
- Common lid: thickness 2.6 mm, top Z=22.6 mm.
- Board substrate plane for both PCBs: Z=6.4…8.0 mm.
- Main PCB transform: `X=2.7+y_STL; Y=64.0-x_STL; Z=8.0+z_STL`.
- Sensor PCB: source orientation preserved, translation (18.7,77.0,6.4) mm.
- Main board M2 points: (6.7,8.5), (6.7,60.5), (43.7,8.5), (43.7,60.5) mm.
- Sensor board M2 points: (21.7,80), (40.7,80), (21.7,109), (40.7,109) mm.
- Sensor head center: (31.2,95.5), aperture Ø14.0 mm, head projection 1.85 mm.
- Eight M2 board fasteners, six M2.5 cover fasteners.
- Four M3 countersunk base mounting holes.

## A1–sensor harness

A1 is oriented +Y toward the sensor pin row. The connector body is a four-position Molex-family visual model. Four separate wires run from the plug to the four sensor pins. This is a mechanical connection layout only. Exact Molex MPN, crimp contact, wire gauge and electrical pin mapping are still open.

## Validation

- Geometry/assembly/datum/clearance/fastener checks: 47/47 PASS.
- STEP round-trip: 12/12 PASS.
- Base and common lid STL: 2/2 watertight.
- Corrected main PCB mesh: 3319 components, 85214 faces, consistent winding, non-watertight as a single mesh.
- Exact SEN-MQ4-V2 STEP: 189 solids.
- ZIP has 40 entries. ZIP CRC PASS. SHA manifest covers 39 files.
- ZIP SHA-256: `98d53bfab82a1a1f1421b828d70854dfa22bbf9fddd0e1411554110b4325a6b5`.
- Manifest SHA-256: `f944979eafb2b1fdf2a9905484f4416bc7c7792fef546ea71a3997ce3769df78`.
- Python scripts and FreeCAD macro pass Python syntax compilation.

## Not done

- FreeCAD 1.1.x native recompute/FCStd save.
- Physical fit of Molex housing/crimps and exact Type-C SKU/plug.
- Wire gauge, electrical pin mapping and insulation routing confirmation.
- 3D print and fit check.
- Wall/table anchor pull-out test.
- Gas response, heater temperature and environmental tests.

## OneDrive

- Folder: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sad33bab3433346379845c3f11d35c6a5
- ZIP: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sa683bd43cfc544828ea4257c6568dead
- Closed GLB: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s111c1ae988724a218c03ed8903ff27fd
- Open GLB: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sa7d48b50ebf842c49f4b7f0da77b7a7f
- FreeCAD macro: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s86cb8081df7a4d2282061486dba3c143
