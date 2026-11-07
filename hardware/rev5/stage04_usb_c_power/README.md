# Stage04R1 — замена входа питания XS1 на USB-C

Дата: 2026-11-07  
Ветка: `design/usb-c-pcb-enclosure-r5`

## Решение

XS1 был двухконтактным входом питания `VCC/Earth`, а не разъёмом датчика. В новой ревизии XS1 удалён из схемы и PCB, на его боковую сторону перенесён J1 GCT USB4105. Сигнальный разъём сенсорного модуля A1 и остальная измерительная/сигнальная часть сохранены.

Принятые пока допущения: USB-C — только вход 5 В, без USB-данных и USB-PD. Добавлены два независимых Rd 5,1 кОм:
- CC1 → R8 pin 2 → R8 pin 1 → Earth.
- CC2 → R9 pin 2 → R9 pin 1 → Earth.

VBUS назначен на `/VCC`, GND и shell — на `Earth`. D+/D−/SBU оставлены NC. PWR_FLAG сети VCC сохранён.

## Файлы

OneDrive хранит двоичные исходники KiCad и полный пакет:
- [Stage04R1 folder](https://1drv.ms/f/c/24fda6920aa8c92a/IgCzlXAjWEiPT4kG0-s0lLTLAWQL7YgHkJiJ3NXKAVn3ne0)
- [ZIP package](https://1drv.ms/u/c/24fda6920aa8c92a/IQA-4KsYZDatTLpRYhOMJbGQAbvrRtMgZ-V9RcyXWbYdwjI)
- [Schematic](https://1drv.ms/u/c/24fda6920aa8c92a/IQD1JFMnvNVNT7EllJ6YICAzARKD7sLaUGmq_uO_8aazbfI)
- [PCB](https://1drv.ms/u/c/24fda6920aa8c92a/IQA3ivIe3LpURbYP1Qzu24wpAbcSwkDSxq-B8VNwI7WuEcE)
- [Placement preview](https://1drv.ms/i/c/24fda6920aa8c92a/IQCNI0SsAiclRIAn5yBOZH9nAQirG9i97YoX1o11sPj6l8Q)

GitHub содержит инженерные отчёты, ссылки и audit trail. Сами бинарные файлы KiCad в GitHub не загружены.

## SHA-256

- Schematic: `f4ecc00b30d8aa52d9f21f3e29bafa825ae219cdc2f13c8c2dc7e27aa8bacd5d`.
- PCB: `78840a0598cb7c21e2f556c656f200bf174126a7d0d94fdd7e42a084c783e162`.
- ZIP: `83f2bb4bb53f939dece74d18359b44430ba0c59f2a63bdfeca39828d877c3ade`.

## Контроль и ограничения

Структурная проверка S-expression пройдена, дубли reference/UUID не обнаружены. Статическая геометрическая проверка размещения показала минимальный зазор 1,1 мм между новыми courtyard и 0,3 мм между новыми медными площадками и чужими существующими дорожками. Размеры платы и четыре отверстия M2 сохранены.

PCB не готова к изготовлению. Существующая дорожка `/VCC` непосредственно соединяет площадки J1 A4/B9. Остальные VBUS/GND/CC соединения пока не разведены. Native KiCad ERC/DRC, Refill All Zones и 3D Viewer не выполнялись. Необходимо завершить трассировку и проверку в KiCad 10.0.7.

Защита входа не выбрана: актуальная спецификация Joy-IT SEN-MQ4-V2 указывает питание 5 В, но не приводит суммарный ток модуля. Ток пуска и установившийся ток должны быть подтверждены до выбора предохранителя/PTC и TVS.
