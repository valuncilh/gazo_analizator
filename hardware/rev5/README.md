# Газоанализатор E3 — Rev5

**Рабочая ветка:** `design/usb-c-pcb-enclosure-r5`  
**Состояние:** инженерная учебная ревизия. Не выпуск для производства.

## Цель

Переработать двухслойную плату E3 под вход питания USB-C 5 В, сохранить существующую схему газового датчика/сигнализатора и согласовать PCB с новой параметрической моделью корпуса Variant B Turtle.

## Соглашение о сохранении файлов

Ни один исходный файл PCB, схемы, STEP, FCStd, STL, footprint, скрипта или отчёта не удаляется и не перезаписывается при подготовке новой ревизии. Каждое реальное изменение сохраняется в новый файл и отдельный этапный пакет. Статус старого файла меняется на superseded только после проверки нового файла. Смотри `SOURCE_PRESERVATION_POLICY.md`.

## Исходники и контрольная база

Неизменяемые копии исходной разведённой PCB, схемы, PCB STEP, старых пакетов корпуса и сенсорного модуля сохранены в OneDrive.

[Исходный baseline folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgAnVFgpfc9WQK9nWuSqdRp3AbaSeJAc8tlWTGNKwYewT6k)  
[Baseline ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQBHREov1F1bSay7DkcBEFrQAWv0sY4f9sOWANQYgvgHAPk)

## Stage 02R1 — проверка размещения USB4105

[Stage 02R1 folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgBUjMa7o1GZRKMwXr-iLH4hASQkkyOK6vWCT9Bu4TfnNjM)  
[Stage 02R1 ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQDAWMaNvP3mRa2qagX9FJv2ASr4eo9tBjtxCLmf4kpHgzo)

## Stage 03 — новый PCB-файл с USB-C placement candidate

[Stage 03 folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgDAm06P30bhQL4P4ST_QhPPAeOlVd40lZh9Fiod0AYJDjM)  
[Полный Stage 03 ZIP](https://1drv.ms/u/c/24fda6920aa8c92a/IQAlDy0rexlITJ0wN4pNTUEEASRN_l5IGK1uom9vudSFx8E)  
[Открыть PCB-кандидат в OneDrive](https://1drv.ms/u/c/24fda6920aa8c92a/IQC87rWVi-XjQohqghzMzB0QAaIV4ggXGasmHesOrV-PHiQ)  
[PNG размещения](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s93860d4fdfdc4bab9aa4c37353784c5b)  
[SVG размещения](https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s5cd79c8880564216a401fb1c06b1c56e)

В Stage 03 сохранены новый файл `gazo_e3_rev5_usb_c_placement.kicad_pcb`, исходная PCB, footprint/3D references, скрипты генерации, статический аудит, таблицы отверстий, общий drill schedule, PNG/SVG, README и SHA-256 manifest.

### Текущий статус Stage 03

- Создан новый PCB-файл на базе исходной разведённой платы.
- Добавлены J1 (USB4105), R8 и R9.
- USB-C назначен входом 5 В. A4/A9/B4/B9 → `/VCC`, GND и shell → `Earth`.
- CC1 и CC2 разведены раздельно на индивидуальные 5,1 кОм pull-down резисторы.
- D+/D−/SBU остались NC.
- XS1 сохранён как временный старый вход. Удалять его будем только после проверки новой цепи питания.
- Существующие M2 отверстия, исходный контур, дорожки, via и зоны сохранены.
- Статический анализ геометрии/UUID/привязок выполнен.

**Нативный KiCad ERC/DRC не запускался.** До финализации нужно открыть файл в KiCad, обновить зоны и запустить DRC. Это не заявляется как DRC PASS.

## Механические базы

- Плата 59 × 45 × 1,6 мм.
- M2: четыре отверстия Ø2,2 мм NPTH.
- Центры: (172,127.5), (224,127.5), (172,164.5), (224,164.5) мм в координатах routed baseline.
- Межосевые расстояния 52 × 37 мм.
- Корпус строится только после фиксации PCB и экспорта новой STEP-геометрии.

## Следующий этап

1. Сверить USB-C placement и 3D-модель в KiCad с пользователем.
2. Обновить схему новым USB-C символом, CC1/CC2 Rd и корректным номером shield pads.
3. Проверить ток нагрузки/пусковой ток нагревателя MQ-4 и подобрать защиту входа 5 В.
4. Развести новые сети VBUS/GND/CC, сохранить предыдущий файл как baseline.
5. После успешной проверки новой цепи удалить XS1 из новой ревизии, но не из исходника.
6. Запустить нативные ERC/DRC в KiCad 10, сохранить отчёты и только затем экспортировать PCB STEP.
7. Построить FreeCAD корпус и проверить посадку, вырез USB-C, крепление крышки и отверстия.
