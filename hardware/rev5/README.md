# Газоанализатор E3 — Rev5

**Рабочая ветка:** `design/usb-c-pcb-enclosure-r5`  
**Состояние:** инженерная учебная ревизия. Не выпуск для производства.

## Цель

Переработать двухслойную плату E3 под вход питания USB-C 5 В, сохранить существующую схему газового датчика/сигнализатора и согласовать PCB и SEN-MQ4-V2 в одном общем корпусе с общей съёмной крышкой.

## Текущий этап — Stage05R5R3: единый корпус с обеими платами

В Stage05R5R3 исправлена сама архитектура. Основная плата газоанализатора и SEN-MQ4-V2 установлены **в один общий корпус** под **одной общей съёмной крышкой**. Обе платы горизонтальны и лежат на одной высоте Z=6,4…8,0 мм. Каждая закреплена четырьмя винтами M2. Общая крышка держится на шести M2.5. Сам корпус имеет четыре отверстия M3 для монтажа на стену/панель/стол.

A1 основной PCB направлен к четырём штырьковым выводам сенсорной платы. Между ними смоделирован короткий четырёхжильный жгут: Molex-family корпус со стороны A1 и четыре гибкие жилы к сенсорным штырькам. Электрическая распиновка и точный MPN Molex пока не подтверждены.

- Единое основание: 50,8×121,0 мм, высота стенок 20 мм. Общая крышка 2,6 мм, полная высота 22,6 мм.
- На крышке только дуговая надпись «Детектор метана» вокруг головки MQ-4. CH4 и другой декор отсутствуют.
- USB-C — простое скруглённое отверстие 9,4×3,6 мм, R1,7, без рамки и вставки.
- Геометрия/компоновка/зазоры/крепёж: 47/47 PASS. STEP round-trip 12/12 PASS.
- Основание и крышка STL: 2/2 watertight. Основная PCB mesh остаётся многокомпонентной, поэтому полный вид обеих плат — в GLB и FreeCAD, не в BREP-only STEP.
- Native FreeCAD recompute/FCStd, физическая примерка провода/USB-C и печать ещё не выполнены.

[Stage05R5R3 OneDrive folder](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sad33bab3433346379845c3f11d35c6a5)  
[Full Stage05R5R3 ZIP](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sa683bd43cfc544828ea4257c6568dead)  
[Closed GLB](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s111c1ae988724a218c03ed8903ff27fd)  
[Open GLB](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sa7d48b50ebf842c49f4b7f0da77b7a7f)  
[FreeCAD macro](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s86cb8081df7a4d2282061486dba3c143)  
[Top view — both boards and harness](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s61e2e33777ea41439c01a2088a6cc472)  
[A1–Molex–sensor pins close-up](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s44e100321d1d43cd907c1a019b27b4eb)

SHA-256:
- ZIP: `98d53bfab82a1a1f1421b828d70854dfa22bbf9fddd0e1411554110b4325a6b5`
- Manifest: `f944979eafb2b1fdf2a9905484f4416bc7c7792fef546ea71a3997ce3769df78`
- Corrected main PCB source: `0a6489358d9ff5d8a8fbd0f9e5916dcffeefa2e925c6cb4ce9a08b2220c7703b`
- Sensor STEP source: `d064355fa01dd6ed99a5886260bc3dadf1f246ba39076c1bb64b40fadc283ee7`

Подробности: `этапы/Этап 05R5R3 — единый корпус и обе платы/README.md` и checkpoint `log/REV5_CHECKPOINT_VLAR_STAGE05R5R3_COMMON_TWO_PCBS_2026-11-08.md`.

## Архивный этап — Stage05R5R2: установка уточнённой PCB и Type-C

Исправлена компоновка основного корпуса по новой пользовательской STL платы. Плата теперь действительно установлена внутри корпуса по правильному 90° преобразованию координат. Реальные четыре монтажных отверстия выровнены с опорами M2. Два прямоугольных placeholder тела J1 удалены из mesh, вместо них помещён визуальный BREP USB4105 с металлической скруглённой оболочкой, внутренней полостью, язычком и контактами.

- Основной корпус 50,8×69×27,2 мм.
- Крышка на 4×M2.5, PCB на 4×M2, крепление корпуса к стене/столу — 4×M3.
- Сквозное отверстие USB-C в стенке +X: 9,4×3,6 мм, R1,7. Без рамки, накладки и вставки.
- A1 выведен через соседнюю +Y стенку по фактическому положению на новой PCB.
- На крышке только «Детектор метана» и CH4 в шестиугольнике.
- Сенсорный модуль на точной STEP-сборке SEN-MQ4-V2 сохранён самостоятельным, с отдельной винтовой крышкой и 4×M3 креплением.
- Геометрия: 38/38 PASS. STEP round-trip 12/12 PASS. Корпусные STL 4/4 watertight.
- PCB остаётся многокомпонентной mesh-сборкой 3319 компонентов, 85214 facets. Она включена в GLB и FreeCAD macro, но не в BREP-only STEP.

[Stage05R5R2 OneDrive folder](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s43e86e3cd2554478a3df742657a181a8)  
[Full ZIP](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sc21342f6d56843a29c551f0a3fd855f6)  
[Installed PCB GLB](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sf8263a6cc1934c44b4296f94f10a0ed3)  
[FreeCAD macro](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s0bb718d2d183470cbba71423e23361e1)  
[PCB installed in base preview](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s3a05f6db64ed4ec5bd30d0702b37afbd)  
[USB-C receptacle detail](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s48ec2b341e304224b8d2ba0298b3682b)

SHA-256:
- ZIP: `3657170fd33f151edff0ae570b49526113ba1bcc761c39b1cbe0d00b33bcaa58`
- Manifest: `ea24ab7e0acd80144f0638c52ec09469711ca3dbb945a6964fd94ade0e5e6e23`
- Main installed GLB: `2b93f2d0e007a9438ecc0eebedfc174f1ef8d9e4afdd35979d52f3fc46155dba`
- Corrected PCB source: `0a6489358d9ff5d8a8fbd0f9e5916dcffeefa2e925c6cb4ce9a08b2220c7703b`
- Sensor STEP source: `d064355fa01dd6ed99a5886260bc3dadf1f246ba39076c1bb64b40fadc283ee7`
- Geometry validation: `618d5699504a9601fc490b95fbb27a630cf28b0c23960b56273bc6628c1c253a`
- USB4105 visual BREP: `b62f208d44d870ac329c477d9cc61b82c0ef42234bd45a22b835b01cac2cbbe7`

Подробности: `этапы/Этап 05R5R2 — corrected PCB USB-C/README.md` и checkpoint `log/REV5_CHECKPOINT_VLAR_STAGE05R5R2_PCB_INSTALLED_USB_C_2026-11-08.md`.

## Архивный этап — Stage05R5: Wall/Table Mount до корректной установки PCB и USB-C

Корпус полностью перестроен по двум новым пользовательским механическим исходникам. Основной электронный модуль и сенсорный блок стали отдельными самостоятельными корпусами, каждый с собственным настенным/настольным креплением и съёмной винтовой крышкой.

- Основной корпус 73.5×88×27.2 мм. Крышка на 4×M2.5. Крепление к поверхности 4×M3.
- Сенсорный корпус 42×63×15 мм. Крышка на 4×M2.5. Крепление к поверхности 4×M3.
- Плата SEN-MQ4-V2 крепится по своим четырём отверстиям Ø2.8 мм. Только штатная металлическая головка/защитная решётка выступает над крышкой через отверстие Ø18 мм. Выступ 9.049 мм.
- USB-C — простой проём 10.8×5.2 мм в стенке, без накладки/вставки.
- На основной крышке только «Детектор метана» и CH4 в шестиугольнике.
- BREP/компоновка/датумы 28/28 PASS. STEP round-trip 10/10 PASS. Корпусные STL 4/4 watertight.
- Уточнённая основная PCB сохранена как mesh reference, не watertight (3321 отдельных компонента). Точная сенсорная STEP-сборка содержит 189 solids.
- Native FreeCAD recompute и FCStd ещё не выполнялись. Это инженерный CAD-кандидат, не выпуск для производства.

[Папка Stage05R5 OneDrive](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s2c2692908c724ca5944f2ec5af91ee41)  
[Полный ZIP Stage05R5](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s105514d13c294afeb2b2daaa3b26f035)  
[Макрос и инструкция FreeCAD](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s8cb56fe821794ecd85a1055fd7e02440)

SHA-256:
- ZIP: 89cfc341d6b7b292881dfd4da45ec5cfc5d60ebf566824ec01792804d2c963a4
- Manifest: d397cb07badafdebdf5e260c60c579030a967d9ccbe27d37642627bf21d7f137
- PCB source: 0a6489358d9ff5d8a8fbd0f9e5916dcffeefa2e925c6cb4ce9a08b2220c7703b
- Sensor STEP: d064355fa01dd6ed99a5886260bc3dadf1f246ba39076c1bb64b40fadc283ee7

Подробности: этапы/Этап 05R5 — корпус Wall Table Mount/README.md и журнал REV5_CHECKPOINT_VLAR_STAGE05R5_WALL_TABLE_MOUNT_2026-11-07.md.

## Архивный этап — Stage05R4: корпус Split-Deck

Полностью переработана архитектура Stage05R3. Вместо удлинённой общей оболочки используется отдельный электронный короб с самостоятельной крышкой и независимая открытая съёмная кассета MQ-4. USB-C и SA1 выполнены сменными вставками, добавлены световоды HL1/HL2, акустические отверстия HA1 и втулка кабельного ввода A1.

- Электронный короб: 65×70×28 мм, крышка 3 мм. Полный габарит около 65×114×31 мм.
- PCB Stage04R3 неизменна. Координаты J1/A1/HL1/HL2/HA1/SA1 и 4×M2 проверены из PCB S-expression: 10/10 PASS.
- Геометрический журнал: 52/52 PASS. STL: 8/8 watertight.
- Макрос FreeCAD 1.1.x подготовлен, но native recompute и FCStd generation пока не выполнены.
- USB4105 exact suffix/plug fit, реальная ориентация SA1 и внутренние размеры SEN-MQ4-V2 остаются открытыми. Не manufacturing release.

[Stage05R4 папка OneDrive](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sb995a379d890428daa116d62d08965fa)  
[Stage05R4 полный ZIP](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sbee3c9b863624278839e68f9866b4323)  
[FreeCAD макрос](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sef8f81d3cd0a4c0d8478190539087a75)  
[Закрытая сборка PNG](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s8070dcc867b94110995297f7be3024f4)  
[PCB datum audit](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s10acf4d4200b498fbe1bf3142caa9ca1)

SHA-256:
- ZIP: `6b370ea5381fcc663303474600a78a95cbf4e51f25ff8fe12a04bff8882f5f78`
- Closed assembly STEP: `cc646e56c6b6bf8f3ae25c751619fc125ca3eed8d26dbfbfcf16347d29986e62`
- Geometry validation: `f32b3b6e99f39078ac61f270d3fbf28c8031a35c388e6c80dbeaf723f272ac15`
- FreeCAD macro: `a2439ab4a6476c296ef6b3c3c877ea71cc8e491688bdcaf916b5f7262ad57b41`

Подробности: `этапы/Этап 05R4 — корпус Split-Deck/README.md` и `log/REV5_CHECKPOINT_VLAR_STAGE05R4_SPLIT_DECK_2026-11-07.md`.

## Архивный этап — Stage05R3: корпус FreeCAD Variant B Turtle для PCB R3

Продолжена механическая конструкция Variant B Turtle Stage05R2, поскольку Stage04R3 изменил только ориентацию R8/R9 на 180°. Все footprint centres, J1/A1, контур PCB и M2 датумы остались прежними.

- Основание, единая крышка, четыре M2 стойки, две направляющие сенсора MQ-4.
- USB-C на длинной стенке +X, противоположной A1.
- Плата 59×45×1.6 мм; внешний envelope корпуса 65×127×32.5 мм.
- 35/35 геометрических BREP/координатных/interference/STEP round-trip проверок PASS.
- 4/4 STL watertight, consistent winding, один компонент каждая.
- Подготовлен макрос FreeCAD 1.1.x для четырёх FCStd: Housing, Closed Assembly, Service Assembly, Exploded Assembly.
- Native FreeCAD recompute/FCStd ещё не выполнялся; FCStd не заявляются как уже созданные.
- Exact GCT USB4105 ordering code/shell-stake suffix не подтверждён. Окно 9.8×4.2 мм и gap 3.05 мм provisional.
- PCB STEP — упрощённый механический reference без copper/vias R3; внутренние позиции SEN-MQ4-V2 частично оценочные.

[Stage05R3 папка OneDrive](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sb1cfb4de66144227ab8e2f89e1d86737)
[Stage05R3 ZIP](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s5ec2f86d9fc54eb2a98d5a10e64fc8f0)
[Макрос FreeCAD](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s2ff2efe0e18840a5b9cc15ac610a8c85)
[Габаритный чертёж](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s885ee2fba2704caabd3616606890ba2a)
[Закрытая сборка PNG](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sd43b36c74147467e84e050964c73e912)
[Сервисная сборка PNG](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sd3f354fbe2114cd782bad291f20b0752)
[Геометрический аудит](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sc98c2ce897584b8e9fb9bc7bb97af3d7)

Контрольные суммы:
- PCB Stage04R3: ac120c090f22f84342e3be6635b659c08afdf5558355b38c02d2e7035dfdc671
- ZIP Stage05R3: 05257f5a223b15f5565075254262a195e6ed0c7cebce4b35eb373db22d7968d9
- FreeCAD macro: 8d9ce80a07ce62d856567f25e7e79211179df70f5646b8de7e27d381eab51086
- Geometry validation: d73bc02f22b613c52bebb35b267e84f67302cada8ff068a3d2e1056190c02237
- Mesh validation: 36ec28f8d9ca188c4776f94017c8909271d3edfb1d2cf3c5bcfe5c1b92a898b6

Подробности: этапы/Этап 05R3 — корпус Variant B Turtle/README.md и checkpoint log/REV5_CHECKPOINT_VLAR_STAGE05R3_FREECAD_ENCLOSURE_2026-11-07.md.

## Архивный этап — Stage04R3: исправление DRC на пользовательской шелкографии

Исправления выполнены поверх последней пользовательской версии R2, включая его изменения шелкографии. Исходная пользовательская PCB сохранена в Stage04R3-пакете отдельно.

- R8/R9 развёрнуты, CC1/CC2 теперь приходят на pad 2, pad 1 — Earth.
- Все 27 глобальных `gr_text` объектов сохранены побайтно; положения Reference R8/R9 также не изменены.
- Восстановлены пять изначально разомкнутых групп: CC1, CC2, Earth returns и /VCC F.Cu↔B.Cu.
- У HL1 короткий диагональный jog заменён прямой ветвью. Расчётный зазор 0.25 мм.
- Четыре J1 hole-clearance нарушения адресованы отдельным custom DRC правилом для рекомендованной геометрии GCT USB4105. Синтаксис правила требует native проверки в KiCad.
- Семь footprint library warnings J1/R8/R9/VD1/A1/VT1/SA1 оставлены как отдельная библиотечная задача.
- 25 references, 904 UUID, 216 сегментов, 25 физических via. Контур 59×45 мм и четыре M2 отверстия сохранены.
- Native DRC/ERC, Refill All Zones и 3D Viewer ещё не выполнены. Это статически проверенный кандидат, не окончательный выпуск.

[Stage04R3 папка OneDrive](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s29cb8d47002940bdb9b34ef26d31bcfb)
[Stage04R3 ZIP](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s825e6f64d9cd4e27944fe51ea12cf6fb)
[PCB R3](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sb8eb4ec1ce1747debbdb0586e248165c)
[Деталь исправленных узлов](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s78b5d2f615d64a91ad184be889bdc505)
[Отчёт ревью](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sa7ab0fef929c401ea2514a9102f36388)

Контрольные суммы:
- PCB R3 SHA-256: `ac120c090f22f84342e3be6635b659c08afdf5558355b38c02d2e7035dfdc671`.
- ZIP R3 SHA-256: `09ba159986364d73c71604b89ce6d4a707c468e6869e0b8062b737d6d4627a8f`.
- Source user-edited R2 SHA-256: `e562faf3edc81fbe3fb9fdaa9b518c197797f69978f5d2f39d1706aeb14656f8`.

Подробности: `этапы/Этап 04R3 — исправление DRC после проверки KiCad/README.md`, `отчёты/PR_DRC_R2_issue_resolution.csv` и checkpoint `log/REV5_CHECKPOINT_VLAR_STAGE04R3_DRC_FIXES_2026-11-07.md`.

## Архивный этап — Stage04R2: перенос USB-C на длинную кромку

USB-C GCT USB4105 перенесён на верхнюю длинную кромку платы, отдельно от A1, с направлением mating face наружу. R8/R9 размещены рядом с J1. CC1/CC2, VBUS, GND и shell разведены как статически проверенный кандидат. XS1 отсутствует.

- J1 origin: (196.0000, 126.6000) мм, rotation 180°.
- Датум PCB Edge: (196.0000, 123.5000) мм, совпадает с Edge.Cuts.
- Контур 59×45 мм и четыре M2 NPTH сохранены.
- Итог: 220 сегментов и 25 физических via. Дубликатов UUID/Reference нет.
- Статические проверки геометрии, clearance и связности PASS.
- Native KiCad 10.0.7 ERC/DRC, Refill All Zones и 3D Viewer ещё не выполнены. PCB пока не объявляется окончательно принятой.

[Stage04R2 папка OneDrive](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s68ff8df4759942b4a786c38cd05060a9)
[Stage04R2 ZIP](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sbf58dc5fbfc54506ba71e3176f5ff471)
[Редактируемая PCB KiCad](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s89af74c7e0e246b8b73eb5461352af85)
[Общий вид платы PNG](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s5d7f15f2c26e433f8d85bc33d33f60a9)
[Деталь USB-C PNG](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sbbc18e2560ff460a97cbc67545196c2f)

Контрольные суммы:
- PCB Stage04R2 SHA-256: `4aed2951d60049d60ea458a58818b156909e0ff416e0e592e7b0da4ce62fe0b0`.
- ZIP Stage04R2 SHA-256: `ae0597b67cf71bf258204ae053f4f45d5d2882622ab9c0bc4f73fddfb764165b`.
- Схема Stage04R2 оставлена без изменений относительно Stage04R1. SHA-256: `f4ecc00b30d8aa52d9f21f3e29bafa825ae219cdc2f13c8c2dc7e27aa8bacd5d`.

Подробности: `этапы/Этап 04R2 — перенос USB-C на длинную кромку/README.md` и checkpoint `log/REV5_CHECKPOINT_VLAR_STAGE04R2_2026-11-07.md`.

## Архивный этап — Stage04R1: замена XS1 на USB-C

Аудит показал, что XS1 являлся только двухконтактным входом питания `VCC/Earth`, а не интерфейсом сенсора. В Stage04R1 XS1 удалён из новой схемы и PCB. На ту же боковую сторону платы перенесён USB-C J1 GCT USB4105. Разъём датчика A1 и существующая измерительная/сигнальная часть сохранены.

- J1: USB-C, предполагаемый режим питания 5 В, без USB-данных и USB-PD.
- R8/R9: отдельные Rd 5,1 кОм от CC1/CC2 к Earth.
- VBUS назначен в `/VCC`, GND и shell — в `Earth`.
- D+/D−/SBU оставлены NC.
- Четыре M2 отверстия и контур 59 × 45 мм сохранены.
- Схема и плата существуют как отдельные Stage04R1-файлы. Исходный baseline не изменён.
- Стадия пока не завершена: кроме существующего совпадения J1 A4/B9 с участком `/VCC`, силовые/CC/GND соединения ещё требуют трассировки. Требуются native KiCad ERC/DRC и refill зон.

[Stage04R1 folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgCzlXAjWEiPT4kG0-s0lLTLAWQL7YgHkJiJ3NXKAVn3ne0)  
[Полный Stage04R1 ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQA-4KsYZDatTLpRYhOMJbGQAbvrRtMgZ-V9RcyXWbYdwjI)  
[Схема KiCad](https://1drv.ms/u/c/24fda6920aa8c92a/IQD1JFMnvNVNT7EllJ6YICAzARKD7sLaUGmq_uO_8aazbfI)  
[PCB KiCad](https://1drv.ms/u/c/24fda6920aa8c92a/IQA3ivIe3LpURbYP1Qzu24wpAbcSwkDSxq-B8VNwI7WuEcE)  
[Эскиз размещения PNG](https://1drv.ms/i/c/24fda6920aa8c92a/IQCNI0SsAiclRIAn5yBOZH9nAQirG9i97YoX1o11sPj6l8Q)

Контрольные суммы:
- Schematic SHA-256: `f4ecc00b30d8aa52d9f21f3e29bafa825ae219cdc2f13c8c2dc7e27aa8bacd5d`.
- PCB SHA-256: `78840a0598cb7c21e2f556c656f200bf174126a7d0d94fdd7e42a084c783e162`.
- ZIP SHA-256: `83f2bb4bb53f939dece74d18359b44430ba0c59f2a63bdfeca39828d877c3ade`.

Подробности: `stage04_usb_c_power/README.md`, `stage04_usb_c_power/SCHEMATIC_REVIEW.md`, `stage04_usb_c_power/PCB_PLACEMENT_REVIEW.md` и checkpoint `log/REV5_CHECKPOINT_04R1_XS1_USB_C_REPLACEMENT.md`.

### Сохранение файлов

Ни один исходный файл PCB, схемы, STEP, FCStd, STL, footprint, скрипта или отчёта не удаляется и не перезаписывается при подготовке новой ревизии. Каждое реальное изменение сохраняется в новый файл и отдельный этапный пакет. Смотри `SOURCE_PRESERVATION_POLICY.md`.

## Исходники и контрольная база

Неизменяемые копии исходной разведённой PCB, схемы, PCB STEP, старых пакетов корпуса и сенсорного модуля сохранены в OneDrive.

[Исходный baseline folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgAnVFgpfc9WQK9nWuSqdRp3AbaSeJAc8tlWTGNKwYewT6k)  
[Baseline ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQBHREov1F1bSay7DkcBEFrQAWv0sY4f9sOWANQYgvgHAPk)

## Stage 02R1 — проверка размещения USB4105

[Stage 02R1 folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgBUjMa7o1GZRKMwXr-iLH4hASQkkyOK6vWCT9Bu4TfnNjM)  
[Stage 02R1 ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQDAWMaNvP3mRa2qagX9FJv2ASr4eo9tBjtxCLmf4kpHgzo)

## Stage 03R1 — промежуточный USB-C placement candidate

[Stage 03R1 folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgD9TMKIfuSgQa_O5KN5br94ATrWzH_ylvcmSph4diZcSJg)  
[Полный исправленный ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQC7gkvDHw_XQpgaaWC95G_bAXE4XZnOtcgD5lZMVie5jjY)  
[PCB Stage03R1](https://1drv.ms/u/c/24fda6920aa8c92a/IQCzsC2WfO1qQJQvzRn-aAclAT1bQYZMinb9vIwQqvtia24)

Stage03R1 сохранён как промежуточная ревизия, исходные байты не изменялись. Он содержит USB-C placement и прежний XS1 как временное решение. В Stage04R1 это временное решение заменено: XS1 удалён из новой схемы/платы.

## Механические базы

- Плата 59 × 45 × 1,6 мм.
- M2: четыре отверстия Ø2,2 мм NPTH.
- Центры: (172,127.5), (224,127.5), (172,164.5), (224,164.5) мм в координатах routed baseline.
- Межосевые расстояния 52 × 37 мм.
- Корпус строится только после фиксации PCB и экспорта новой STEP-геометрии.

## Следующие действия

1. Подтвердить, что USB-C используется только как вход питания 5 В.
2. Измерить пусковой и установившийся ток устройства с Joy-IT SEN-MQ4-V2, затем выбрать входную защиту.
3. Открыть Stage04R3 в KiCad 10.0.7, проверить синтаксис `.kicad_dru`, выполнить Refill All Zones и native ERC/DRC.
4. Проверить unconnected items и ориентацию J1, shell stakes, R8/R9 в 3D Viewer.
5. При замечаниях выпускать Stage04R4, не перезаписывая Stage04R3.
6. После пользовательского/native подтверждения экспортировать PCB STEP и актуализировать параметрическую модель корпуса в FreeCAD.
7. Подтвердить пусковой/установившийся ток SEN-MQ4-V2 и выбрать защиту входа.
