# Газоанализатор E3 — Rev5

**Рабочая ветка:** `design/usb-c-pcb-enclosure-r5`  
**Состояние:** инженерная учебная ревизия. Не выпуск для производства.

## Цель

Переработать двухслойную плату E3 под вход питания USB-C 5 В, сохранить существующую схему газового датчика/сигнализатора и согласовать PCB с новой параметрической моделью корпуса Variant B Turtle.

## Текущий этап — Stage04R1: замена XS1 на USB-C

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
3. Завершить трассировку всех VBUS/GND/CC цепей в Stage04R2.
4. В KiCad 10.0.7 обновить зоны и выполнить native ERC/DRC, проверить unconnected items и 3D-модель.
5. Согласовать механический вырез USB-C и экспортировать PCB STEP.
6. После фиксации PCB актуализировать параметрическую модель корпуса.
