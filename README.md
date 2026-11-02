<p align="center">
  <img src="docs/assets/gazo-analizator-banner.svg" alt="Gazo Analizator — инженерный проект сигнализатора метана" width="100%">
</p>

<p align="center">
  <strong>Курсовой проект МАИ</strong><br>
  Бытовой сигнализатор утечки метана (CH₄)
</p>

<p align="center">
  <img src="https://img.shields.io/badge/E3-APPROVED-18794E?style=flat-square" alt="E3 approved">
  <img src="https://img.shields.io/badge/ERC-0_ERRORS%20%7C%2018_WARNINGS-18794E?style=flat-square" alt="ERC zero errors and 18 warnings">
  <img src="https://img.shields.io/badge/PCB-PREPARATION-64748B?style=flat-square" alt="PCB preparation">
  <img src="https://img.shields.io/badge/RPZ-IN_PROGRESS-D97706?style=flat-square" alt="RPZ in progress">
  <img src="https://img.shields.io/badge/DOCUMENTATION-RU-3157A5?style=flat-square" alt="Russian documentation">
  <a href="docs/PROJECT_TAGS.md"><img src="https://img.shields.io/badge/STATUS_TAGS-DEFINED-3157A5?style=flat-square" alt="Project status tags"></a>
</p>

---

## О проекте

Курсовой инженерный проект МАИ по разработке бытового сигнализатора утечки метана (CH₄). В репозитории собраны принципиальная схема KiCad, расчёты, SPICE-модели и документация по подготовке печатной платы и корпуса.

**Как читать обозначения:** E3 — утверждённая принципиальная электрическая схема основной платы, но не готовая печатная плата. E4 — отдельная плата ввода питания USB-C, её схема и PCB ещё не разработаны. РПЗ — расчётно-пояснительная записка. Это учебный проект расчётов и конструкторской документации: физическое изготовление, закупка, монтаж и лабораторные испытания в текущий объём не входят.

## Утверждённая электрическая схема E3

![APPROVED](https://img.shields.io/badge/APPROVED-18794E?style=flat-square)

Нативный редактируемый лист KiCad: [схема электрическая принципиальная E3](cad/project_modification/gost_e3_final/gazo_analizator_E3_GOST_itog.kicad_sch).

<p align="center">
  <img src="docs/assets/%D1%81%D1%85%D0%B5%D0%BC%D0%B0.png" alt="Утверждённая принципиальная схема E3" width="100%">
</p>

Электрическая редакция зафиксирована тегом [gost-e3-approved-2026-11-01](https://github.com/valuncilh/gazo_analizator/tree/gost-e3-approved-2026-11-01). Схема, XML-netlist, baseline и сохранённый ERC-отчёт составляют неизменяемую базовую редакцию. Визуальные правки выполняются только в отдельной копии и должны подтверждаться сравнением netlist.

**Контрольные материалы:** [паспорт утверждённой редакции](cad/project_modification/gost_e3_final/APPROVED_BASELINE.md) · [XML-netlist](cad/project_modification/gost_e3_final/reports/kicad10/netlist_current.xml) · [карта соединений](docs/figures/e3_approved_netlist_map.md) · [ERC](cad/project_modification/gost_e3_final/reports/kicad10/erc_current.rpt).

Обзорная функциональная SVG-визуализация не используется как замена листу ЕСКД. Для проверки оформления и печати открывайте нативный файл в KiCad.

## Проверка проекта за 5–10 минут

1. **Общее состояние:** откройте [путеводитель для проверяющего](docs/REVIEW_GUIDE.md). В нём собраны назначение, результаты и незавершённые части.
2. **Требования и доказательства:** сверьте [проектное ТЗ](requirements/technical_assignment_draft.md), [матрицу верификации](requirements/verification_matrix.md) и [карту прогресса](docs/project_progress_map.md). ТЗ является самостоятельно подготовленным учебным документом, а не подписанным заданием преподавателя.
3. **Главный электрический результат:** откройте [утверждённую E3](cad/project_modification/gost_e3_final/gazo_analizator_E3_GOST_itog.kicad_sch), её [паспорт](cad/project_modification/gost_e3_final/APPROVED_BASELINE.md), [XML-netlist](cad/project_modification/gost_e3_final/reports/kicad10/netlist_current.xml) и [ERC-отчёт](cad/project_modification/gost_e3_final/reports/kicad10/erc_current.rpt). В сохранённом ERC — 0 ошибок и 18 предупреждений, причины перечислены в паспорте.
4. **Расчёты и пояснительная записка:** используйте [каталог глав РПЗ](docs/rpz/README.md). Статус каждой главы и ограничения приведены в самом каталоге.

## Быстрый доступ

| Для чего | Документ |
|---|---|
| Начать знакомство и проверить проект | [Маршрут для преподавателя и рецензента](docs/REVIEW_GUIDE.md) |
| Посмотреть состояние работ | [Карта прогресса](docs/project_progress_map.md) · [визуальная карта SVG](docs/project_progress_map.svg) |
| Изучить расчётно-пояснительную записку | [Главы и статусы РПЗ](docs/rpz/README.md) · [контрольная ODT-сборка, OneDrive](https://1drv.ms/w/c/24fda6920aa8c92a/IQBgvF5tTSGsRpjx8u47tfMPAWUgI9pUcU) |
| Открыть стандарт оформления документации | [Documentation Style Guide](docs/DOCUMENTATION_STYLE.md) |
| Разобраться в статусных метках | [Теги и статусы материалов](docs/PROJECT_TAGS.md) |
| Посмотреть графики и иллюстрации | [Каталог изображений](docs/figures/README.md) |
| Проверить состав документации | [Реестр документов](docs/document_register.md) |
| Изучить исходные требования | [Техническое задание](requirements/technical_assignment_draft.md) · [матрица верификации](requirements/verification_matrix.md) |
| Проверить компонентную базу | [Реестр MPN и footprints](cad/footprint_selection_2026-11-01.md) · [документальный аудит E3/E4](cad/footprint_audit_2026-11-02.md) |
| Проверить расчёты текущей конфигурации | [A1 Joy-IT V2](calculations/mq4_module_check_joyit_v2.md) · [массогабариты E3/E4](calculations/mass_gabarit_joyit_e3.md) · [надёжность](calculations/reliability_joyit_e3_preliminary.md) · [токовый бюджет](calculations/power_budget_joyit_e3.md) · [тепловая оценка](calculations/thermal_joyit_e3.md) |
| Открыть реализационную копию E3 | [KiCad implementation scaffold](cad/kicad/e3_project/README.md) · [проверка базы и назначений](cad/scripts/verify_e3_implementation.py) |
| Найти нормативную базу и правила РПЗ | [Методики МАИ](docs/course_acceptance/README.md) · [контрольный лист оформления](requirements/report_formatting.md) |
| Проследить историю решений | [Инженерный журнал](docs/engineering_log_2026-11-02.md) · [индекс архива](docs/ARCHIVE_INDEX.md) |

## Зафиксированная проектная конфигурация

Ниже приведена принятая проектная архитектура, а не перечень уже изготовленных узлов.

| Узел | Текущее решение |
|---|---|
| Сенсорный модуль A1 | Joy-IT SEN-MQ4-V2 |
| Основная схема E3 | Утверждённая редакция, зафиксированная тегом gost-e3-approved-2026-11-01 |
| Таймер DA1 | NE555N по утверждённой схеме. Для первой итерации PCB выбран физический кандидат TI NE555P |
| Транзистор VT1 | КТ3102Б |
| Звуковой излучатель HA1 | Ningbo Kepo HCM1206X, чертёж OEM2690R |
| Питание | Предусмотрена отдельная плата USB-C E4. По проектной архитектуре на E3 подаётся +5 В через XS1. Сама E4 ещё не разработана |
| Условия среды | +10…+35 °C, относительная влажность 20–80 % без конденсации. Это проектное условие, совместимость полной BOM ещё проверяется |

## Состояние разработки

| Направление | Статус | Текущее положение |
|---|---|---|
| Схема E3 | **APPROVED** | Базовая редакция зафиксирована тегом gost-e3-approved-2026-11-01 |
| ERC и XML-netlist E3 | **VERIFIED** | 0 ошибок ERC и 18 предупреждений в сохранённом отчёте |
| MPN и footprints | **PRELIMINARY** | Документально сверены 19 refs E3. Создан KT3102B footprint DRAFT, для KD510A выбран DO-35 с pad1=K. Открыты координатная сверка 1.2 mm для VT1, pin maps A1/HA1 и локальные KiCad 10 checks |
| PCB E3 | **PREPARATION** | Создана изолированная копия схемы с кандидатными footprints для 19 refs и карта 47 pad-to-net. `.kicad_pro` и `.kicad_pcb` ещё не созданы, ERC/DRC и routing не выполнены |
| USB-C E4 | **PREPARATION** | Архитектура определена. Схема, PCB и защита VBUS ещё не завершены |
| Токовый бюджет | **BLOCKED** | Паспорт не задаёт полный максимальный ток A1. Worst-case всей системы пока не доказан |
| Тепловой расчёт | **PRELIMINARY** | Оценены отдельные источники тепла. Полной модели конечной сборки пока нет |
| Механика и корпус | **NOT STARTED** | Интегрированный корпус E3/E4 ещё не создан |
| Надёжность | **PRELIMINARY** | Количественная оценка ожидает точной BOM и условий эксплуатации |
| РПЗ | **IN PROGRESS** | Содержательные главы подготовлены. Требуются техническая и редакционная проверки |

## Температурные графики

![CURRENT CALCULATION](https://img.shields.io/badge/CURRENT_CALCULATION-3157A5?style=flat-square)

В основной витрине оставлены только два температурных материала главы 6 РПЗ: параметрическая зависимость перегрева и номограмма естественной конвекции. Это расчётные модели, а не измерения готового корпуса.

<p align="center">
  <img src="docs/rpz/thermal_sensitivity.svg" alt="Параметрическая зависимость перегрева от эквивалентного теплового сопротивления" width="48%">
  <img src="docs/rpz/natural_convection_nomogram.svg" alt="Номограмма коэффициента естественной конвекции по Churchill–Chu" width="48%">
</p>

Методика и ограничения: [раздел 6 РПЗ](docs/rpz/06_thermal_model_and_sensitivity.md). Исследовательские SPICE-графики, предварительные компоновки и исторические изображения сохранены в исходных каталогах для прослеживаемости, но не выводятся в основную витрину.

## Статусы и границы достоверности

- **APPROVED** — решение утверждено или базовая редакция зафиксирована. Это не означает аппаратные испытания.
- **VERIFIED** — проверено только в явно указанном объёме, например ERC, netlist или отдельная геометрия.
- **PRELIMINARY** — предварительный расчёт, проектный кандидат или компоновка.
- **BLOCKED** — отсутствуют необходимые исходные данные или проверка не может быть подтверждена в пределах текущего CAD-only проекта.
- **HISTORICAL** — материал сохранён для прослеживаемости, но не относится к текущей реализации.

Проект не является производственно выпущенным или сертифицированным газосигнализатором. SPICE-расчёты, ERC и CAD-проверки не заменяют измерения на физическом макете и калибровку сенсорного канала. Физическое изготовление, закупка и лабораторные измерения не входят в текущий подтверждённый объём. Неподтверждённые без образца характеристики сохраняют статус TBC.

## Рабочая ветка и сохранение базовой схемы

Основная рабочая ветка: analysis/vendor-behavioral-reconciliation. Изменения, проверки и контрольные точки фиксируются коммитами и инженерным журналом. Утверждённая схема E3, её отчёты и тег gost-e3-approved-2026-11-01 не изменяются в рамках редакционного оформления документации.

## Структура репозитория

- cad/ — схемы, проекты PCB, посадочные места, компоновка, корпус и отчёты CAD.
- calculations/ — ручные расчёты и проверки с явным разделением актуальных и исторических материалов.
- data/ — исходные данные, характеристики компонентов и реестр источников.
- docs/ — навигация, инженерные журналы, методики, изображения и РПЗ.
- requirements/ — проектные требования и контрольные матрицы.
- spice/ — модели, тестбенчи и воспроизводимые SPICE-сценарии.

Политика работы с историческими материалами описана в [индексе архива](docs/ARCHIVE_INDEX.md).
