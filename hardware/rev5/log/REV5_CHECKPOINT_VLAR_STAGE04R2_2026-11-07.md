# Checkpoint VLAR — Stage04R2: перенос USB-C на отдельную длинную кромку

Дата: 2026-11-07
Исполнитель: VLAR
Ветка: `design/usb-c-pcb-enclosure-r5`
Статус: `static-checked / native-check-required / user-review`

## Входные данные и сохранность

Получен от пользователя архив `Gazo_E3_Rev5_Stage04_USB_C_Power_R1(1).zip`.
Вложенный полный пакет Stage04R1 распакован. CRC ZIP: PASS.
SHA-256 исходной PCB Stage04R1:
`78840a0598cb7c21e2f556c656f200bf174126a7d0d94fdd7e42a084c783e162`.
SHA-256 схемы Stage04R1:
`f4ecc00b30d8aa52d9f21f3e29bafa825ae219cdc2f13c8c2dc7e27aa8bacd5d`.

Обе суммы совпали с зафиксированными исходными значениями. Stage04R1 PCB/схема не перезаписывались. Точные копии исходных файлов включены в пакет Stage04R2 в каталоге `baseline/`.

## Принятое размещение

J1 GCT USB4105 перенесён с короткой кромки бывшего XS1 на верхнюю длинную кромку платы, отдельную от интерфейса A1. Mating face обращён наружу. Datum footprint `PCB Edge` совмещён с Edge.Cuts.

- J1 origin: X=196.0000 мм, Y=126.6000 мм, rotation 180°.
- PCB edge datum: (196.0000, 123.5000) мм.
- J1 courtyard: X=190.6800…201.3200 мм, Y=122.4200…131.3600 мм.
- A1 и четыре крепёжных отверстия M2 оставлены в исходных координатах.
- R8/R9 перенесены к J1. R8 pad2=CC1, R9 pad2=CC2, pad1 обоих резисторов=Earth.
- XS1 отсутствует. Удалён только осиротевший короткий хвост /VCC, оставшийся после XS1.

## Трассировка

Добавлено 14 сегментов: 10 F.Cu и 4 B.Cu.
Добавлено 4 физических via: 2 /VCC и 2 Earth.
Исходные 207 сегментов изменены только удалением одного висящего XS1-хвоста. Итог — 220 сегментов.
Физических via было 21, стало 25. Правила `(vias not_allowed)` в подсчёт не включаются.

- Обе пары VBUS (A4/A9/B4/B9) сведены в /VCC и подключены к существующей силовой сети.
- CC1 и CC2 не объединялись. Каждая линия идёт на собственный Rd 5.1 кОм.
- GND контакты и shell SH имеют net Earth. Контактные группы выведены на plated shell stakes. Перемычки SH и Earth plane требуют Refill All Zones.
- Выводы Earth резисторов R8/R9 соединены с B.Cu Earth zone через отдельные via.
- D+/D−/SBU оставлены NC в соответствии с power-only назначением.

## Статические проверки VLAR

- S-expression balance: PASS.
- 25 footprint references, дубликатов нет, XS1 отсутствует.
- 908 UUID, дубликатов нет.
- 59×45 мм контур платы сохранён.
- Четыре M2 NPTH: (172,127.5), (224,127.5), (172,164.5), (224,164.5) мм сохранены.
- Courtyard J1/R8/R9 против остальных корпусов: PASS.
- Clearance новых дорожек к дорожкам других сетей: PASS.
- Clearance новых дорожек к чужим площадкам: PASS.
- Clearance новых via к чужим дорожкам и площадкам: PASS.
- Clearance новых дорожек к существующим/новым via других сетей: PASS.
- Via-to-via clearance: PASS.
- Топология CC1/CC2, VBUS, GND/shell, резисторных возвратов и связь с существующей /VCC: PASS.
- Datum J1 к Edge.Cuts: PASS.

Точные результаты и координаты находятся в:
- `PCB_STAGE04R2_STATIC_AUDIT.json`
- `PCB_STAGE04R2_CONNECTIVITY_CHECK.json`
- `PCB_STAGE04R2_REVIEW.md`

## Не выполнено

Native KiCad 10.0.7 ERC/DRC, Refill All Zones, штатная проверка unconnected items и 3D Viewer не выполнялись в среде подготовки. Обновлённая B.Cu Earth zone должна быть перезалита. До заливки нельзя заявлять, что новые Earth via и shell stakes уже соединены готовой медью.
Не экспортирован STEP после переноса. FreeCAD-корпус не менялся.
Ток SEN-MQ4-V2 при прогреве/устоявшемся режиме и выбор входной защиты (предохранитель/PTC/TVS) остаются открытыми.

## OneDrive

Папка Stage04R2 создана внутри исходного Stage04R1 каталога. Файлы загружены как обычные элементы личного OneDrive без создания read-only sharing link. Пользователь может редактировать файлы в своей папке.

- Папка: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s68ff8df4759942b4a786c38cd05060a9
- ZIP пакет: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sbf58dc5fbfc54506ba71e3176f5ff471
- PCB: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s89af74c7e0e246b8b73eb5461352af85
- Общий вид: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!s5d7f15f2c26e433f8d85bc33d33f60a9
- Деталь USB-C: https://onedrive.live.com?cid=24FDA6920AA8C92A&id=24FDA6920AA8C92A!sbbc18e2560ff460a97cbc67545196c2f

ZIP SHA-256:
`ae0597b67cf71bf258204ae053f4f45d5d2882622ab9c0bc4f73fddfb764165b`.

PCB SHA-256:
`4aed2951d60049d60ea458a58818b156909e0ff416e0e592e7b0da4ce62fe0b0`.

Пакет содержит 17 элементов, manifest содержит SHA-256 для 16 входящих файлов. Проверка целостности ZIP: PASS.

## Следующий шаг

Открыть Stage04R2 PCB и Stage04R1 schematic в KiCad 10.0.7. Выполнить Refill All Zones, ERC/DRC и 3D Viewer. Прислать отчёт и изображение USB-C в 3D. При выявлении замечаний продолжать с Stage04R3, не перезаписывая Stage04R2.
