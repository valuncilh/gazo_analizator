#!/usr/bin/env python3
"""Plot aligned behavioral/vendor control-chain and output-load comparisons."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
BEHAVIORAL = ROOT / "model_comparison_behavioral.dat"
VENDOR = ROOT / "model_comparison_vendor.dat"
OUTPUT = ROOT / "model_comparison_overlay.png"
BRANCH_OUTPUT = ROOT / "model_comparison_branch_currents.png"


def load_trace(path: Path) -> np.ndarray:
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f"Required simulation data is missing: {path}")
    data = np.loadtxt(path, skiprows=1)
    if data.ndim != 2 or data.shape[1] < 12:
        raise SystemExit(
            f"Unexpected data shape in {path}: {data.shape}, expected time plus eleven vectors"
        )
    if not np.isfinite(data[:, :12]).all():
        raise SystemExit(f"Non-finite data values in {path}")
    return data


def branch_currents(data: np.ndarray) -> dict[str, np.ndarray]:
    # Data order: t, S, UREF, DOUT, RESET, CT, OUT, BZ_COL, supply current,
    # HL1_A, R9_N, VT2_B. All branch-current values are derived from Ohm's law.
    out = data[:, 6]
    bz_col = data[:, 7]
    hl1_a = data[:, 9]
    r9_n = data[:, 10]
    return {
        "HL1 через R6": (out - hl1_a) / 220.0 * 1000.0,
        "Базовая ветвь VT2 через R9": (out - r9_n) / 560.0 * 1000.0,
        "Нагрузка RBZ": (5.0 - bz_col) / 166.7 * 1000.0,
    }


behavioral = load_trace(BEHAVIORAL)
vendor = load_trace(VENDOR)

fig, axes = plt.subplots(4, 1, figsize=(10.5, 10.2), sharex=True)
fig.suptitle("Сопоставление моделей при общем входном сигнале S", fontsize=13)

axes[0].plot(behavioral[:, 0], behavioral[:, 1], label="Поведенческая модель")
axes[0].plot(vendor[:, 0], vendor[:, 1], "--", label="Vendor-модель")
axes[0].set_ylabel("Напряжение S, В")
axes[0].legend(loc="best")
axes[0].grid(True, alpha=0.3)

axes[1].plot(behavioral[:, 0], behavioral[:, 4], label="RESET, поведенческая модель")
axes[1].plot(vendor[:, 0], vendor[:, 4], "--", label="RESET, vendor-модель")
axes[1].set_ylabel("Напряжение RESET, В")
axes[1].legend(loc="best")
axes[1].grid(True, alpha=0.3)

axes[2].plot(behavioral[:, 0], behavioral[:, 6], label="Поведенческая модель")
axes[2].plot(vendor[:, 0], vendor[:, 6], "--", label="Vendor-модель")
axes[2].set_ylabel("Напряжение OUT, В")
axes[2].legend(loc="best")
axes[2].grid(True, alpha=0.3)

axes[3].plot(behavioral[:, 0], behavioral[:, 8] * 1000, label="Поведенческая модель")
axes[3].plot(vendor[:, 0], vendor[:, 8] * 1000, "--", label="Vendor-модель")
axes[3].set_xlabel("Время, с")
axes[3].set_ylabel("Ток источника, мА")
axes[3].legend(loc="best")
axes[3].grid(True, alpha=0.3)

for axis in axes:
    for transition in (0.8, 1.6, 2.4):
        axis.axvline(transition, linewidth=0.8, linestyle=":")
    axis.set_xlim(0, 4.0)

fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(OUTPUT, dpi=160, bbox_inches="tight")
plt.close(fig)
print(f"Comparison plot saved: {OUTPUT}")

b_currents = branch_currents(behavioral)
v_currents = branch_currents(vendor)
branch_fig, branch_axes = plt.subplots(3, 1, figsize=(10.5, 8.5), sharex=True)
branch_fig.suptitle("Токи отдельных нагрузочных ветвей", fontsize=13)

for axis, name in zip(branch_axes, b_currents):
    axis.plot(behavioral[:, 0], b_currents[name], label="Поведенческая модель")
    axis.plot(vendor[:, 0], v_currents[name], "--", label="Vendor-модель")
    axis.set_title(name, loc="left", fontsize=10)
    axis.set_ylabel("Ток, мА")
    axis.legend(loc="upper right", ncol=2, fontsize=8)
    axis.grid(True, alpha=0.3)

for axis in branch_axes:
    for transition in (0.8, 1.6, 2.4):
        axis.axvline(transition, linewidth=0.8, linestyle=":")
    axis.set_xlim(0, 4.0)
branch_axes[-1].set_xlabel("Время, с")
branch_fig.tight_layout(rect=(0, 0, 1, 0.96))
branch_fig.savefig(BRANCH_OUTPUT, dpi=160, bbox_inches="tight")
plt.close(branch_fig)
print(f"Branch-current plot saved: {BRANCH_OUTPUT}")
