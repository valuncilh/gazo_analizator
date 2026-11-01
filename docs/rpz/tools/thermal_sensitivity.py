#!/usr/bin/env python3
"""Generate the parametric thermal characteristic used in the RПЗ.

The curves are sensitivity cases for ΔT = P * R_theta.
Neither the power values nor the thermal-resistance axis represent measured
properties of the present enclosure. They are illustrative inputs that can
be replaced after the physical sensor and case are fixed.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    resistance = np.linspace(0.0, 30.0, 301)
    powers_w = (0.1, 0.25, 0.5, 1.0)

    fig, ax = plt.subplots(figsize=(7.2, 4.6), constrained_layout=True)
    for power in powers_w:
        temperature_rise = power * resistance
        ax.plot(
            resistance,
            temperature_rise,
            label=f"P = {power:g} W",
        )

    ax.set(
        xlim=(0, 30),
        ylim=(0, 30),
        xlabel=r"Эквивалентное тепловое сопротивление $R_{\theta,eff}$, К/Вт",
        ylabel=r"Перегрев $\Delta t$, К",
        title="Параметрическая тепловая характеристика",
    )
    ax.grid(True, which="both", linewidth=0.5)
    ax.legend(title="Тепловой поток")
    fig.text(
        0.01,
        0.005,
        "Иллюстративные сценарии. Не являются результатами измерения корпуса.",
        fontsize=8,
    )

    output = Path(__file__).with_name("thermal_sensitivity.svg")
    fig.savefig(output, format="svg")
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
