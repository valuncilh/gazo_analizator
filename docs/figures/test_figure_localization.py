#!/usr/bin/env python3
"""Регрессионные проверки локализации рисунков и критических SPICE-связей."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"ОШИБКА: {message}", file=sys.stderr)
        raise SystemExit(1)


def main() -> int:
    bode = (ROOT / "spice/plot_bode.py").read_text(encoding="utf-8")
    transient = (ROOT / "spice/plot_results.py").read_text(encoding="utf-8")
    figures = (ROOT / "docs/figures/generate_figures.py").read_text(encoding="utf-8")
    behavioral = (ROOT / "spice/alarm_chain_behavioral.cir").read_text(encoding="utf-8")
    vendor = (ROOT / "spice/alarm_chain_vendor.cir.in").read_text(encoding="utf-8")
    initial_data = (ROOT / "data/initial_data.md").read_text(encoding="utf-8")

    forbidden_plot_labels = [
        '"Magnitude, dB"',
        '"Phase, degrees"',
        '"Frequency, Hz"',
        '"Voltage, V"',
        '"Time, s"',
        '"Gas-on / rise"',
        '"Gas-off / recovery"',
        'label="Charge state"',
        'label="Discharge state"',
        '"Bode plots of linearized submodels',
        '"Sensor stimulus and comparator reference"',
        '"Comparator output and timer reset"',
    ]
    for label in forbidden_plot_labels:
        require(label not in bode + transient,
                f"Осталась англоязычная подпись графика: {label}")

    for label in ("Амплитуда, дБ", "Фаза, градусы", "Частота, Гц"):
        require(label in bode, f"Не найдена русская подпись АЧХ/ФЧХ: {label}")
    for label in ("Напряжение, В", "Время, с", "Сигнал датчика A1.S",
                  "Вход сброса RESET таймера DA1"):
        require(label in transient,
                f"Не найдена русская подпись переходного графика: {label}")

    # Visual regression for the missing DISCH-to-R5 wire from the timer drawing.
    require("wire(ax,[(2.0,4.1),(2.2,4.1)],INK,1.7)" in figures,
            "На рисунке таймера отсутствует перемычка DISCH—R5")

    # The comparator figure is intentionally a fixed-reference SPICE submodel.
    # It must not be mislabeled as the actual adjustable P1 schematic.
    require("RP1A и RP1B — фиксированные резисторы делителя UREF." in figures,
            "Рисунок компаратора не поясняет, что RP1A/RP1B — фиксированный делитель")
    require('resistor_v(ax,1.55,5.85,4.85,"RP1A = 5,2 кОм",ORANGE)' in figures,
            "На рисунке не указан RP1A = 5,2 кОм")
    require('resistor_v(ax,1.55,4.5,3.3,"RP1B = 4,8 кОм",BLUE)' in figures,
            "На рисунке не указан RP1B = 4,8 кОм")
    require("| P1 | 10 кОм" in initial_data,
            "В исходных данных не зафиксирован реальный регулируемый P1")

    # Critical timing, comparator, feedback, output and protection connections.
    for netlist_name, netlist in (
        ("поведенческая модель", behavioral),
        ("vendor-модель", vendor),
    ):
        required_connections = (
            ("R4 VCC DISCH 8.2k", "VCC—R4—DISCH"),
            ("R5 DISCH CT 8.2k", "DISCH—R5—CT"),
            ("C1 CT 0", "C1 должен идти от CT к земле"),
            ("RHYS DOUT UREF 100k", "обратная связь RHYS"),
            ("D1 BZ_COL VCC", "полярность защитного диода VD1"),
            ("R9 OUT R9_N 560", "базовая цепь VT2 через R9"),
        )
        for needle, description in required_connections:
            require(needle in netlist,
                    f"{netlist_name}: проверка соединения «{description}» не пройдена")

    require("XU2 UREF S DOUT VCC 0 TLV7041" in vendor,
            "Порядок выводов TLV7041 должен быть IN+, IN−, OUT, V+, V−")
    require("XDA1 CT CTRL555 CT RESET OUT DISCH VCC 0 TLC555_6" in vendor,
            "Изменён порядок выводов функциональной модели TLC555")
    require("RP1A VCC UREF 5.2k" in vendor and "RP1B UREF 0 4.8k" in vendor,
            "Фиксированный делитель в рисунке не соответствует vendor-netlist")
    require("C_U2 VCC 0 100n" in vendor,
            "В vendor-netlist отсутствует развязка питания U2")

    print("Регрессионные проверки локализации, рисунка таймера и критических SPICE-связей пройдены.")
    print("Ограничение: проверки статические. Они не заменяют визуальную приёмку, ERC/DRC или аппаратную проверку.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
