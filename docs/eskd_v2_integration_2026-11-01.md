# ЕСКД v2 — интеграция CAD-пакета

**Дата:** 01.11.2026  
**Рабочая ветка:** `analysis/vendor-behavioral-reconciliation`  
**Целевая интеграция:** существующий Draft PR #4 → `main`.  
**Статус:** CAD-пакет подготовлен отдельно, локальная проверка KiCad обязательна.

## Назначение

Сохранить отдельную экспериментальную версию схемы ЕСКД v2, не затрагивая контрольную схему и не меняя `main`. Пакет `gazo_eskd_v2_implementation.tar.gz` содержит рабочую копию проекта в `cad/project_modification_eskd/`, исходный снимок схемы, локальную библиотеку NE555, шаблон листа A4 portrait и статические проверочные скрипты.

## Состав пакета

- `cad/project_modification_eskd/project_modification_eskd.kicad_pro`
- `cad/project_modification_eskd/project_modification_eskd.kicad_sch`
- `cad/project_modification_eskd/baseline_project_modification_layout.kicad_sch`
- `cad/project_modification_eskd/gazo_a4_portrait_gost_r_2_104_2023.kicad_wks`
- `cad/project_modification_eskd/Gazo_GOST.kicad_sym`
- `cad/project_modification_eskd/sym-lib-table`
- `cad/project_modification_eskd/verify_topology_preservation.py`
- `cad/project_modification_eskd/verify_exported_design.py`
- `cad/project_modification_eskd/validate_eskd_package.py`
- `cad/project_modification_eskd/ESKD_IMPLEMENTATION_REPORT.md`

В архив также включены переданный экспорт `gazo_layout.xml`, ERC-отчёт, исходная таблица эталонных соединений и legacy GOST-библиотеки.

## Проверенное и непроверенное

Пакетный отчёт фиксирует следующие статические результаты: 53 сегмента проводников, 19 меток и один NC сохранены; определения восьми выводов NE555 по номеру, координатам и электрическому типу сохранены; переданный XML-экспорт соответствует эталону по 13 сетям, 19 компонентам и 47 выводам.

Это не является новым ERC или новым экспортом схемы после миграции. Полная миграция УГО, финальная компоновка в пределах A4, запуск ERC и выпуск PDF/SVG ещё не завершены. Не считать проект готовым к производству.

## Локальное подключение пакета

Распаковать приложенный архив во временный каталог, затем перенести `cad/project_modification_eskd/` и `data/project_modification_reference.md` в корень клона репозитория. Не перезаписывать `cad/project_modification/` и контрольные исходники.

Пример для fish:

```fish
mkdir -p /tmp/gazo_eskd_v2_import
tar -xzf ~/Downloads/gazo_eskd_v2_implementation.tar.gz -C /tmp/gazo_eskd_v2_import
cp -a /tmp/gazo_eskd_v2_import/cad/project_modification_eskd ./cad/
cp -a /tmp/gazo_eskd_v2_import/data/project_modification_reference.md ./data/
```

После импорта проверить `git status`, затем открыть `cad/project_modification_eskd/project_modification_eskd.kicad_pro` в KiCad 10. Сначала выполнить пакетные Python-проверки, затем ERC, экспорт netlist, PDF и SVG. Результаты и фактические версии KiCad записать в инженерный журнал.

## Политика Git

Изменения относятся только к `analysis/vendor-behavioral-reconciliation`. Ветка `main` не изменяется. Существующий Draft PR #4 остаётся черновым. Автоматическое слияние запрещено.
