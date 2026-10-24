#!/usr/bin/env python3
"""Построение АЧХ и ФЧХ линейных SPICE-подмоделей.

Кривые датчика — приближённая аппроксимация рисунка 6 руководства Winsen
MQ-4 v1.6. Это не гарантированные изготовителем постоянные времени и не
калиброванная передаточная функция «концентрация газа — напряжение».
"""
from pathlib import Path
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
DATA_PATH = ROOT / "bode_results.dat"
PLOT_PATH = ROOT / "bode_linearized.png"

if not DATA_PATH.is_file():
    print(
        f"Не найден файл {DATA_PATH}. Сначала выполните "
        "ngspice -b spice/sensor_bode.cir из корня репозитория.",
        file=sys.stderr,
    )
    raise SystemExit(1)

try:
    data = np.loadtxt(DATA_PATH, skiprows=1)
except (OSError, ValueError) as exc:
    print(f"Не удалось прочитать данные AC-анализа {DATA_PATH}: {exc}", file=sys.stderr)
    raise SystemExit(1)

if data.ndim != 2 or data.shape[1] < 9 or data.shape[0] < 10:
    print(
        "Неверный формат данных AC-анализа. Ожидаются частота и 8 векторов: "
        "модуль и фаза для нарастания/восстановления датчика и заряда/разряда таймера.",
        file=sys.stderr,
    )
    raise SystemExit(1)

frequency = data[:, 0]
rise_db, rise_phase = data[:, 1], data[:, 2]
recovery_db, recovery_phase = data[:, 3], data[:, 4]
charge_db, charge_phase = data[:, 5], data[:, 6]
discharge_db, discharge_phase = data[:, 7], data[:, 8]

if np.any(frequency <= 0) or not np.all(np.isfinite(data[:, :9])):
    print("В данных AC-анализа есть неположительные частоты или нечисловые значения.", file=sys.stderr)
    raise SystemExit(1)

fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharex=True)

axes[0, 0].semilogx(frequency, rise_db, label="Поступление газа, τ = 2,2 с")
axes[0, 0].semilogx(frequency, recovery_db, label="Восстановление, τ = 3,0 с")
axes[0, 0].set_title("Динамика отклика MQ-4 (приближение)")
axes[0, 0].set_ylabel("Амплитуда, дБ")
axes[0, 0].legend(loc="best")
axes[0, 0].grid(True, which="both", alpha=0.3)

axes[0, 1].semilogx(frequency, rise_phase, label="Поступление газа")
axes[0, 1].semilogx(frequency, recovery_phase, label="Восстановление")
axes[0, 1].set_title("Фазовая характеристика датчика (приближение)")
axes[0, 1].set_ylabel("Фаза, градусы")
axes[0, 1].legend(loc="best")
axes[0, 1].grid(True, which="both", alpha=0.3)

axes[1, 0].semilogx(frequency, charge_db, label="Заряд: (R4 + R5)C1")
axes[1, 0].semilogx(frequency, discharge_db, label="Разряд: R5C1")
axes[1, 0].set_title("АЧХ RC-цепи таймера в отдельных состояниях")
axes[1, 0].set_xlabel("Частота, Гц")
axes[1, 0].set_ylabel("Амплитуда, дБ")
axes[1, 0].legend(loc="best")
axes[1, 0].grid(True, which="both", alpha=0.3)

axes[1, 1].semilogx(frequency, charge_phase, label="Состояние заряда")
axes[1, 1].semilogx(frequency, discharge_phase, label="Состояние разряда")
axes[1, 1].set_title("ФЧХ RC-цепи таймера в отдельных состояниях")
axes[1, 1].set_xlabel("Частота, Гц")
axes[1, 1].set_ylabel("Фаза, градусы")
axes[1, 1].legend(loc="best")
axes[1, 1].grid(True, which="both", alpha=0.3)

fig.suptitle(
    "АЧХ и ФЧХ линейных подмоделей. Не характеристики сигнализатора целиком",
    fontsize=12,
)
fig.tight_layout()
fig.savefig(PLOT_PATH, dpi=180)
print(f"Графики сохранены: {PLOT_PATH}")
