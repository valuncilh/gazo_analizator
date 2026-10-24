#!/usr/bin/env python3
"""Plot Bode magnitude and phase for the linearized SPICE submodels.

The sensor curves are rough first-order fits to the visual response shape in
Winsen MQ-4 manual v1.6, Fig. 6. They are not manufacturer-guaranteed time
constants or a calibrated concentration-to-voltage transfer function.
"""
from pathlib import Path
import sys

try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError as exc:
    print(
        "Missing plotting dependency. Install numpy and matplotlib. "
        f"Import error: {exc}",
        file=sys.stderr,
    )
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "bode_results.dat"
PLOT_PATH = ROOT / "bode_linearized.png"

if not DATA_PATH.is_file():
    print(
        f"Missing {DATA_PATH}. Run ngspice -b spice/sensor_bode.cir "
        "from the repository root first.",
        file=sys.stderr,
    )
    raise SystemExit(1)

try:
    data = np.loadtxt(DATA_PATH, skiprows=1)
except (OSError, ValueError) as exc:
    print(f"Could not parse ngspice AC data {DATA_PATH}: {exc}", file=sys.stderr)
    raise SystemExit(1)

if data.ndim != 2 or data.shape[1] < 9 or data.shape[0] < 10:
    print(
        "Unexpected AC data layout. Expected frequency plus 8 vectors: "
        "magnitude and phase for sensor rise/recovery and timer charge/discharge.",
        file=sys.stderr,
    )
    raise SystemExit(1)

frequency = data[:, 0]
rise_db, rise_phase = data[:, 1], data[:, 2]
recovery_db, recovery_phase = data[:, 3], data[:, 4]
charge_db, charge_phase = data[:, 5], data[:, 6]
discharge_db, discharge_phase = data[:, 7], data[:, 8]

if np.any(frequency <= 0) or not np.all(np.isfinite(data[:, :9])):
    print("AC output contains non-positive frequencies or non-finite values.", file=sys.stderr)
    raise SystemExit(1)

fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharex=True)

axes[0, 0].semilogx(frequency, rise_db, label="Gas-on / rise, tau=2.2 s")
axes[0, 0].semilogx(frequency, recovery_db, label="Gas-off / recovery, tau=3.0 s")
axes[0, 0].set_title("MQ-4 response dynamics (approximation)")
axes[0, 0].set_ylabel("Magnitude, dB")
axes[0, 0].legend(loc="best")
axes[0, 0].grid(True, which="both", alpha=0.3)

axes[0, 1].semilogx(frequency, rise_phase, label="Gas-on / rise")
axes[0, 1].semilogx(frequency, recovery_phase, label="Gas-off / recovery")
axes[0, 1].set_title("Sensor phase response (approximation)")
axes[0, 1].set_ylabel("Phase, degrees")
axes[0, 1].legend(loc="best")
axes[0, 1].grid(True, which="both", alpha=0.3)

axes[1, 0].semilogx(frequency, charge_db, label="Charge state, (R4+R5)C1")
axes[1, 0].semilogx(frequency, discharge_db, label="Discharge state, R5C1")
axes[1, 0].set_title("Timer RC-state magnitude")
axes[1, 0].set_xlabel("Frequency, Hz")
axes[1, 0].set_ylabel("Magnitude, dB")
axes[1, 0].legend(loc="best")
axes[1, 0].grid(True, which="both", alpha=0.3)

axes[1, 1].semilogx(frequency, charge_phase, label="Charge state")
axes[1, 1].semilogx(frequency, discharge_phase, label="Discharge state")
axes[1, 1].set_title("Timer RC-state phase")
axes[1, 1].set_xlabel("Frequency, Hz")
axes[1, 1].set_ylabel("Phase, degrees")
axes[1, 1].legend(loc="best")
axes[1, 1].grid(True, which="both", alpha=0.3)

fig.suptitle(
    "Bode plots of linearized submodels — not the nonlinear alarm as a whole",
    fontsize=12,
)
fig.tight_layout()
fig.savefig(PLOT_PATH, dpi=180)
print(f"Saved Bode plots to {PLOT_PATH}")
