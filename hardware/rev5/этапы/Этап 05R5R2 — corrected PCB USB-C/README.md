# Stage05R5R2 — corrected PCB installed / USB-C rounded aperture

Дата: 2026-11-08  
Ветка: `design/usb-c-pcb-enclosure-r5`  
Статус: preliminary engineering CAD candidate, not a manufacturing release.

## Исправление по пользовательскому замечанию

Основная плата теперь действительно размещена внутри основного корпуса. Для сборки использована пользовательская уточнённая STL, а не предыдущий отдельный mesh reference без корректной установки. Плата установлена по правильному 90° преобразованию координат, не зеркально. Четыре фактических отверстия PCB совмещены с четырьмя опорными стойками M2.

Два упрощённых прямоугольных placeholder тела J1 удалены из PCB mesh. Взамен построен отдельный семейный визуальный BREP-разъём GCT USB4105 с металлической закруглённой оболочкой, внутренней полостью, центральным язычком и контактными полосами.

## Main enclosure

- Внешний габарит: 50.8×69.0×27.2 mm.
- Отдельная крышка на 4×M2.5.
- PCB поддерживается 4×M2.
- Настенное/настольное крепление корпуса: 4×M3.
- На крышке только «Детектор метана» и CH4 в шестиугольнике.
- USB-C: plain through-wall aperture 9.4×3.6 mm, R1.7, +X wall. Без рамки, накладки или сменной вставки.
- A1: отдельный скруглённый кабельный проход на соседней +Y стенке.

### PCB placement

User-supplied PCB STL SHA-256: `0a6489358d9ff5d8a8fbd0f9e5916dcffeefa2e925c6cb4ce9a08b2220c7703b`.

Transform from STL coordinates to enclosure:
`X_case=2.7+y_STL; Y_case=64.0-x_STL; Z_case=8.0+z_STL`.

Installed board substrate bounds: X=2.7…47.7 mm, Y=5…64 mm, Z=6.4…8.0 mm. Minimum nominal plan clearance to the enclosure cavity: 0.30 mm.

Four exact mounting-hole centres in case coordinates:
(6.7,8.5), (6.7,60.5), (43.7,8.5), (43.7,60.5) mm.

The corrected PCB remains a triangulated mesh assembly of 3319 components / 85214 facets, not one closed BREP solid. It is included in the GLB assembly and imported by the FreeCAD macro as a `Mesh::Feature`. The BREP-only STEP assembly does not contain that mesh. Use GLB/FreeCAD for the complete installed board and STEP for enclosure/connector BREP parts.

## USB-C geometry

Official drawing: [GCT USB4105 mechanical drawing](https://gct.co/files/drawings/usb4105.pdf). It specifies the front mating opening 8.34×2.56 mm and front shell width 8.64 mm. The family-level visual BREP uses this front geometry as its guide, including shell, cavity, tongue and 12 visible contact strips. Its 2.86 mm outer face height is an explicit visual approximation, not a manufacturer dimension confirmed by a separate dimension callout.

Case aperture is 9.4×3.6 mm, R1.7. Nominal margins against the modeled 8.64×2.86 mm visual shell are 0.38 mm and 0.37 mm. The connector face is recessed about 2.6 mm from the outer wall. Exact ordered suffix (-060/-095/-120), exact supplier STEP and physical plug insertion remain unconfirmed. The hole remains provisional until the real connector and cable are fitted.

## Sensor module

Uses the exact user-supplied SEN-MQ4-V2 STEP. SHA-256: `d064355fa01dd6ed99a5886260bc3dadf1f246ba39076c1bb64b40fadc283ee7`. It contains 189 solids. Its PCB uses four exact Ø2.8 mm mounting holes, fastened by four M2 screws. Independent sensor enclosure cover uses 4×M2.5 and has an Ø18 mm plain opening. Only the original metal head/guard projects above the lid by 9.049 mm. Radial clearance is approx. 1.01 mm. Sensor pod is independently wall/table mounted through 4×M3.

## Validation

- BREP/layout/clearance/fastener geometry: 38/38 PASS.
- STEP round-trip: 12/12 PASS.
- Enclosure meshes: 4/4 watertight, consistent winding, one connected component.
- PCB: winding consistent, 3319 components, not watertight as a whole. Kept as an installed mesh reference.
- Package: 54 ZIP entries, 45 manifest file hashes, ZIP CRC PASS.

## FreeCAD

The macro `Создать_нативные_документы_Stage05R5R2.FCMacro` creates five FreeCAD 1.1.x documents including an open service view with the real installed PCB mesh and USB-C BREP. It was syntax-checked, but native FreeCAD recompute and FCStd saving have not yet been performed in the build environment.

## OneDrive

- [Stage05R5R2 folder](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s43e86e3cd2554478a3df742657a181a8)
- [Complete ZIP package](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sc21342f6d56843a29c551f0a3fd855f6)
- [Installed PCB GLB assembly](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sf8263a6cc1934c44b4296f94f10a0ed3)
- [FreeCAD macro](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s0bb718d2d183470cbba71423e23361e1)
- [Installed PCB in base preview](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s3a05f6db64ed4ec5bd30d0702b37afbd)
- [USB-C rounded receptacle detail](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s48ec2b341e304224b8d2ba0298b3682b)

## Checksums

- ZIP SHA-256: `3657170fd33f151edff0ae570b49526113ba1bcc761c39b1cbe0d00b33bcaa58`
- Manifest SHA-256: `ea24ab7e0acd80144f0638c52ec09469711ca3dbb945a6964fd94ade0e5e6e23`
- Main installed GLB: `2b93f2d0e007a9438ecc0eebedfc174f1ef8d9e4afdd35979d52f3fc46155dba`
- Main PCB source: `0a6489358d9ff5d8a8fbd0f9e5916dcffeefa2e925c6cb4ce9a08b2220c7703b`
- Sensor source STEP: `d064355fa01dd6ed99a5886260bc3dadf1f246ba39076c1bb64b40fadc283ee7`
- Geometry report: `618d5699504a9601fc490b95fbb27a630cf28b0c23960b56273bc6628c1c253a`
- USB4105 visual BREP: `b62f208d44d870ac329c477d9cc61b82c0ef42234bd45a22b835b01cac2cbbe7`


[Closed main housing STEP](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sfac205a4b97f41b1a0b2b167c78cadcb)
