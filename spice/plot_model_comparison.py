#!/usr/bin/env python3
"""Plot the aligned behavioral/vendor control-chain comparison."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
BEHAVIORAL = ROOT / "model_comparison_behavioral.dat"
VENDOR = ROOT / "model_comparison_vendor.dat"
OUTPUT = ROOT / "model_comparison_overlay.png"


def load_trace(path: Path) -> np.ndarray:
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f"Required simulation data is missing: {path}")
    data = np.loadtxt(path, skiprows=1)
    if data.ndim != 2 or data.shape[1] < 9:
        raise SystemExit(
            f"Unexpected data shape in {path}: {data.shape}, expected time plus eight vectors"
        )
    if not np.isfinite(data[:, :9]).all():
        raise SystemExit(f"Non-finite data values in {path}")
    return data


behavioral = load_trace(BEHAVIORAL)
vendor = load_trace(VENDOR)

fig, axes = plt.subplots(3, 1, figsize=(10.5, 8.2), sharex=True)
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

axes[2].plot(behavioral[:, 0], behavioral[:, 8] * 1000, label="Поведенческая модель")
axes[2].plot(vendor[:, 0], vendor[:, 8] * 1000, "--", label="Vendor-модель")
axes[2].set_xlabel("Время, с")
axes[2].set_ylabel("Ток источника, мА")
axes[2].legend(loc="best")
axes[2].grid(True, alpha=0.3)

for axis in axes:
    for transition in (0.8, 1.6, 2.4):
        axis.axvline(transition, linewidth=0.8, linestyle=":")
    axis.set_xlim(0, 4.0)

fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(OUTPUT, dpi=160, bbox_inches="tight")
print(f"Comparison plot saved: {OUTPUT}")
