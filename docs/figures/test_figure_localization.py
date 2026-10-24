#!/usr/bin/env python3
"""Проверки русских подписей и ключевых соединений в исходниках рисунков/SPICE."""
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

    # Старые англоязычные фразы были именно надписями на графиках.
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
        require(label not in bode + transient, f"Осталась англоязычная подпись графика: {label}")

    required_russian_labels = [
        "Модуль передаточной функции, дБ",
        "Фаза, градусы",
        "Частота, Гц",
    ]
    for label in required_russian_labels:
        require(label in bode, f"Не найдена русская подпись АЧХ/ФЧХ: {label}")
    for label in [
        "Напряжение, В",
        "Время, с",
        "Выход компаратора",
        "сброс таймера",
    ]:
        require(label in transient, f"Не найдена русская подпись переходного графика: {label}")

    # Проверка конкретной визуальной ошибки: на рисунке 4 линия DISCH теперь
    # непрерывно соединяет узел с левым выводом R5.
    require(
        "wire(ax,[(2.0,4.1),(2.2,4.1)],INK)" in figures,
        "На рисунке 4 отсутствует перемычка от узла DISCH к R5",
    )
    require("NPN low-side" not in figures, "В рисунках осталась английская подпись low-side")
    require("DOUT′ low" not in figures and "DOUT′ high" not in figures,
            "В логике рисунка компаратора остались английские уровни low/high")
    require("ползунок P1" in figures, "На рисунке компаратора не обозначен движок потенциометра P1")
    require("C_U2 = 100 нФ" in figures, "На рисунке компаратора отсутствует конденсатор развязки C_U2")

    # Сверка критических узлов с SPICE-источником, а не с иллюстративными линиями.
    for netlist_name, netlist in [
        ("поведенческая модель", behavioral),
        ("модель с компонентами TI", vendor),
    ]:
        require("R4 VCC DISCH 8.2k" in netlist, f"{netlist_name}: нарушено соединение VCC—R4—DISCH")
        require("R5 DISCH CT 8.2k" in netlist, f"{netlist_name}: нарушено соединение DISCH—R5—CT")
        require("C1 CT 0" in netlist, f"{netlist_name}: C1 должен подключаться от CT к земле")
        require("RHYS DOUT UREF 100k" in netlist, f"{netlist_name}: нарушена цепь гистерезиса")
        require("D1 BZ_COL VCC" in netlist, f"{netlist_name}: изменена полярность защитного диода")

    require(
        "XU2 UREF S DOUT VCC 0 TLV7041" in vendor,
        "Порядок выводов TLV7041 в экземпляре XU2 изменён",
    )
    require(
        "XDA1 CT CTRL555 CT RESET OUT DISCH VCC 0 TLC555_6" in vendor,
        "Порядок выводов функционального аналога TLC555 изменён",
    )

    print("Проверки русских надписей и ключевых соединений пройдены.")
    print("Примечание: это статические регрессионные проверки. Они не заменяют визуальный осмотр PNG, ERC/DRC или запуск ngspice.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
