#!/usr/bin/env python3
"""Generate the vertical-plate natural-convection nomogram for RPZ chapter 6.

The output is a parameterized engineering chart, not a measurement of the
finished gas detector enclosure. Air properties are fixed near 300 K to match
the assumptions written in docs/rpz/06_thermal_model_and_sensitivity.md.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

G = 9.80665
BETA = 1.0 / 300.0
NU = 15.89e-6
THERMAL_DIFFUSIVITY = 22.5e-6
PR = 0.706
AIR_CONDUCTIVITY = 0.0263
HEIGHTS_MM = (40, 60, 80, 100)


def heat_transfer_coefficient(height_mm: float, temperature_rise_k: np.ndarray) -> np.ndarray:
    """Return Churchill–Chu mean h for an isothermal vertical plate, W/(m²·K)."""
    height_m = height_mm / 1000.0
    rayleigh = (
        G
        * BETA
        * temperature_rise_k
        * height_m**3
        / (NU * THERMAL_DIFFUSIVITY)
    )
    nusselt = (
        0.825
        + 0.387
        * rayleigh ** (1.0 / 6.0)
        / (1.0 + (0.492 / PR) ** (9.0 / 16.0)) ** (8.0 / 27.0)
    ) ** 2
    return nusselt * AIR_CONDUCTIVITY / height_m


def main() -> None:
    delta_t = np.linspace(1.0, 40.0, 157)
    fig, ax = plt.subplots(figsize=(10.5, 6.6), constrained_layout=True)

    for height_mm in HEIGHTS_MM:
        alpha = heat_transfer_coefficient(height_mm, delta_t)
        ax.plot(delta_t, alpha, linewidth=2.2, label=f"L = {height_mm} мм")

    ax.set(
        xlim=(0, 40),
        ylim=(3, 8),
        xlabel="Перегрев поверхности Δt, К",
        ylabel="Коэффициент теплоотдачи αₖ, Вт/(м²·К)",
        title="Номограмма естественной конвекции\\nвертикальной изолированной поверхности",
    )
    ax.grid(True, which="major", linewidth=0.6, alpha=0.55)
    ax.legend(title="Высота поверхности", frameon=True)
    fig.text(
        0.01,
        0.005,
        "Воздух около 300 К: ν=15,89·10⁻⁶ м²/с, a=22,5·10⁻⁶ м²/с, "
        "Pr=0,706, λ=0,0263 Вт/(м·К), β=1/300 К⁻¹. "
        "Параметрическая оценка, не измерение корпуса.",
        fontsize=8,
    )

    output = Path(__file__).resolve().parents[1] / "natural_convection_nomogram.svg"
    fig.savefig(output, format="svg")
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
