#!/usr/bin/env python3
"""Построение графиков переходного процесса из SPICE-данных.

Требуются numpy и matplotlib. Перед построением сначала выполните SPICE-анализ.
"""
from pathlib import Path
import argparse
import sys

try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError as exc:
    print(
        "Не найдены зависимости для построения графиков. "
        "Установите numpy и matplotlib. "
        f"Подробности: {exc}",
        file=sys.stderr,
    )
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description="Построение графиков переходного процесса ngspice.")
parser.add_argument(
    "--input",
    type=Path,
    default=ROOT / "spice_chain_results.dat",
    help="Файл данных ngspice. По умолчанию: spice/spice_chain_results.dat",
)
parser.add_argument(
    "--output",
    type=Path,
    default=ROOT / "spice_chain_plots.png",
    help="Путь выходного PNG. По умолчанию: spice/spice_chain_plots.png",
)
args = parser.parse_args()
DATA_PATH = args.input
PLOT_PATH = args.output

if not DATA_PATH.is_absolute() and not DATA_PATH.is_file():
    DATA_PATH = ROOT / DATA_PATH
if not PLOT_PATH.is_absolute() and not PLOT_PATH.parent.exists():
    PLOT_PATH = ROOT / PLOT_PATH

if not DATA_PATH.is_file():
    print(
        f"Не найден файл {DATA_PATH}. Сначала выполните "
        "ngspice -b spice/alarm_chain_behavioral.cir из корня репозитория.",
        file=sys.stderr,
    )
    raise SystemExit(1)

try:
    data = np.loadtxt(DATA_PATH, skiprows=1)
except (OSError, ValueError) as exc:
    print(f"Не удалось прочитать результаты SPICE {DATA_PATH}: {exc}", file=sys.stderr)
    raise SystemExit(1)

if data.ndim != 2 or data.shape[1] < 8 or data.shape[0] < 2:
    print(
        "Неверный формат SPICE-данных. Ожидаются как минимум 8 столбцов: "
        "время, S, UREF, DOUT, RESET, CT, OUT, BZ_COL.",
        file=sys.stderr,
    )
    raise SystemExit(1)

time_s, sensor_v, reference_v, dout_v, reset_v, timer_cap_v, timer_out_v, buzzer_col_v = (data[:, i] for i in range(8))

fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)

axes[0].plot(time_s, sensor_v, label="Сигнал датчика A1.S")
axes[0].plot(time_s, reference_v, label="Опорное напряжение U_REF")
axes[0].set_ylabel("Напряжение, В")
axes[0].set_title("Сигнал датчика и опорный уровень компаратора")
axes[0].legend(loc="best")
axes[0].grid(True, alpha=0.3)

axes[1].plot(time_s, dout_v, label="Выход компаратора DOUT")
axes[1].plot(time_s, reset_v, label="Вход сброса RESET таймера DA1")
axes[1].set_ylabel("Напряжение, В")
axes[1].set_title("Выход компаратора и вход сброса таймера")
axes[1].legend(loc="best")
axes[1].grid(True, alpha=0.3)

axes[2].plot(time_s, timer_cap_v, label="Напряжение на C1")
axes[2].plot(time_s, timer_out_v, label="Выход таймера DA1")
axes[2].set_ylabel("Напряжение, В")
axes[2].set_xlabel("Время, с")
axes[2].set_title("Времязадающий конденсатор и выход таймера")
axes[2].legend(loc="best")
axes[2].grid(True, alpha=0.3)

fig.suptitle(
    "Переходный процесс расчётной модели. Не результаты измерения реального устройства",
    fontsize=11,
)
fig.tight_layout()
PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(PLOT_PATH, dpi=160)
print(f"Графики сохранены: {PLOT_PATH}")
