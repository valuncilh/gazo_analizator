# Checkpoint VLAR — Stage05R3: корпус FreeCAD Variant B Turtle для PCB R3

Дата: 2026-11-07
Исполнитель: VLAR
Ветка: design/usb-c-pcb-enclosure-r5
Статус: STEP/STL static-checked / FreeCAD macro syntax-checked / native FCStd pending

## Исходная PCB и геометрическая преемственность

Stage05R3 создан с привязкой к Stage04R3 PCB SHA-256: ac120c090f22f84342e3be6635b659c08afdf5558355b38c02d2e7035dfdc671.
Предыдущая пользовательская Stage04R2 PCB: e562faf3edc81fbe3fb9fdaa9b518c197797f69978f5d2f39d1706aeb14656f8.

Сравнение R2→R3 footprint blocks: 25 references в обеих версиях. Изменились только углы R8/R9 на 180°. Центры R8/R9, остальные footprint centres/angles, J1, A1, Edge.Cuts и отверстия M2 не изменились. Корпуса 0805 симметричны, механические envelope не меняются.

Вариант Variant B Turtle Stage05R2 перенесён в Stage05R3 с новым Stage04R3 PCB mechanical reference STEP и повторной проверкой датумов. Предыдущие FC/STEP/STL Stage05R2 не перезаписывались.

## Концепция

- Общее основание с отдельной камерой сенсора MQ-4.
- Единая съёмная крышка.
- Четыре стойки крепления основной PCB M2.
- Две съёмные боковые направляющие/опоры модуля сенсора.
- USB-C на длинной стенке +X, противоположной A1.
- Боковые вентиляционные прорези камеры MQ-4.

Номинальный габарит корпуса: X=65 мм, Y=127 мм overall, Z=32.5 мм. Плата 59×45×1.6 мм.

## Механические датумы

PCB-to-case transform: X_case=52-y_local; Y_case=5.5+x_local; Z_case=6.4+Z_board.

M2 Ø2.2 mm case coordinates: (48,9), (48,61), (11,9), (11,61).

J1: footprint origin board-local (27.5,3.1) mm, rotation 180°; case origin (48.9,33.0) mm; PCB edge datum (52.0,33.0) mm; USB-C на стенке +X противоположно A1. Оценочная плоскость сопряжения X=59.35 мм, внутренняя стенка X=62.4 мм, gap=3.05 мм. Окно 9.8×4.2 мм, bezel 12×6.4 мм. Всё это предварительно.

MQ-4 external envelope 41×25×21 мм. Внутренние can/Molex позиции оценочные. Геометрический зазор до крышки 5.4 мм. Геометрическая боковая вентиляционная площадь 515.2 мм².

## Stage05R3 OneDrive

Папка: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sb1cfb4de66144227ab8e2f89e1d86737
Полный ZIP: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s5ec2f86d9fc54eb2a98d5a10e64fc8f0
Макрос FreeCAD: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s2ff2efe0e18840a5b9cc15ac610a8c85
Габаритный чертёж: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s885ee2fba2704caabd3616606890ba2a
Закрытая сборка: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sd43b36c74147467e84e050964c73e912
Сервисная сборка: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sd3f354fbe2114cd782bad291f20b0752
Геометрический аудит: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sc98c2ce897584b8e9fb9bc7bb97af3d7

SHA-256:
- Stage04R3 PCB: ac120c090f22f84342e3be6635b659c08afdf5558355b38c02d2e7035dfdc671
- ZIP Stage05R3: 05257f5a223b15f5565075254262a195e6ed0c7cebce4b35eb373db22d7968d9
- FreeCAD macro: 8d9ce80a07ce62d856567f25e7e79211179df70f5646b8de7e27d381eab51086
- Geometry validation: d73bc02f22b613c52bebb35b267e84f67302cada8ff068a3d2e1056190c02237
- Mesh validation: 36ec28f8d9ca188c4776f94017c8909271d3edfb1d2cf3c5bcfe5c1b92a898b6

В пакете 44 элемента. SHA manifest покрывает 43 файла. ZIP CRC PASS. OneDrive содержит ZIP и отдельно загруженные макрос/инструкцию, STEP/STL, чертежи, отчёты, скрипты, исходную PCB/схему и пользовательскую R2. Файлы добавлены как обычные personal OneDrive items; новые read-only sharing links не создавались.

## Выполненные проверки

- CadQuery/OpenCascade STEP BREP validity и solid-count: 35/35 PASS.
- Нет интерференции основание/крышка, PCB/основание, PCB/крышка, PCB/опоры, сенсор/основание/крышка/опоры по BREP intersection-volume.
- Сверка M2 датумов и PCB R3 fingerprint: PASS.
- J1 wall/edge alignment: PASS для упрощённого габарита.
- STEP export/re-import: PASS; корпус 4 solids, closed/service/exploded assembly 33 solids.
- Четыре STL meshes: 4/4 watertight, winding-consistent, один компонент каждая.
- Python source и FreeCAD macro syntax compilation: PASS.
- Package ZIP integrity: PASS.

## Ограничения и не выполнено

1. FreeCAD отсутствует в среде подготовки. Native FreeCAD 1.1.4 recompute и FCStd generation не выполнялись. Макрос создаёт Housing.FCStd, Closed_Assembly.FCStd, Service_Assembly.FCStd и Exploded_Assembly.FCStd.
2. FCStd будут содержать editable imported BREP features и MechanicalBasis properties, но не полностью constraint-driven sketch history.
3. Точный GCT USB4105 ordering code/shell-stake suffix не подтверждён. Макрос ищет KiCad 3D модель USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.step. Если не найдёт, оставит SIMPLIFIED_FALLBACK. Даже при найденной модели сверить с BOM.
4. USB aperture 9.8×4.2 мм и gap 3.05 мм provisional. Проверить физический plug insertion.
5. PCB STEP — упрощённая 21-solid механическая модель Stage05R2, она не отражает copper/vias Stage04R3.
6. SEN-MQ4-V2 internal Molex/can geometry оценочная. Газовые, тепловые, печатные, IP, акустические и safety tests не проводились.
7. Native KiCad DRC/ERC Stage04R3 в этом этапе не подтверждался.

## Следующий шаг

Запустить макрос в FreeCAD 1.1.4. Проверить MechanicalBasis.USB4105ModelStatus, recompute/save всех четырёх FCStd и осмотреть closed/service assembly. Передать вывод Console и скриншоты. Не перезаписывать Stage05R2 или Stage05R3 inputs.