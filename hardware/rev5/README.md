# Газоанализатор E3 — Rev5

**Рабочая ветка:** `design/usb-c-pcb-enclosure-r5`  
**Состояние:** инженерная учебная ревизия. Не выпуск для производства.

## Цель

Переработать двухслойную плату E3 под вход питания USB-C 5 В, сохранить существующую схему газового датчика/сигнализатора и согласовать PCB с новой параметрической моделью корпуса Variant B Turtle.

## Текущий этап — Stage04R2: перенос USB-C на длинную кромку

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
3. Открыть Stage04R2 в KiCad 10.0.7, выполнить Refill All Zones и native ERC/DRC, проверить unconnected items.
4. Проверить ориентацию J1, shell stakes и вырез корпуса в 3D Viewer.
5. При замечаниях выпускать Stage04R3, не перезаписывая Stage04R2.
6. После пользовательского/native подтверждения экспортировать PCB STEP и актуализировать параметрическую модель корпуса в FreeCAD.
7. Подтвердить пусковой/установившийся ток SEN-MQ4-V2 и выбрать защиту входа.

## Stage05R2 — Variant B Turtle adapted to Stage04R2 USB-C long-edge PCB

Stage04R2 is the active PCB source. Stage05R2 adapts the existing Variant B Turtle R3 case to the long-edge USB-C orientation, retaining the separate A1 sensor side and open MQ-4 gas-exchange geometry.

- [Stage05R2 OneDrive work folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgDPFgSptzpLQJyZHScUdd5oASWy8KHSvaSuY83UYVDvcps)
- [Stage05R2 GitHub artifact pointer](stage05r2_enclosure/README.md)
- Portable archive SHA-256: `d193ba3e0f0099174fef39ea11ab826372ee4247ced9bd35d95b780c029e4f61`.
- 34/34 CadQuery/OpenCascade geometry checks and 4/4 STL topology checks passed.

**Limitations:** USB4105 is represented by a simplified envelope pending exact supplier STEP/physical plug verification. Native KiCad checks and native FreeCAD recompute/FCStd output remain open. The Stage05R2 case is preliminary, not a fabrication release. Maintain the MQ-4 gas-exchange opening.
