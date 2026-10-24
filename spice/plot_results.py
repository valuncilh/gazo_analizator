#!/usr/bin/env python3
"""Plot the transient data produced by alarm_chain_behavioral.cir.

Requires numpy and matplotlib. The simulator output is intentionally kept
outside version control until a successful, reviewed run has been captured.
"""
from pathlib import Path
import argparse
import sys

try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError as exc:
    print(
        "Missing plotting dependency. Install numpy and matplotlib, then retry. "
        f"Import error: {exc}",
        file=sys.stderr,
    )
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description="Plot ngspice transient data.")
parser.add_argument(
    "--input",
    type=Path,
    default=ROOT / "spice_chain_results.dat",
    help="ngspice wrdata file. Default: spice/spice_chain_results.dat",
)
parser.add_argument(
    "--output",
    type=Path,
    default=ROOT / "spice_chain_plots.png",
    help="Output PNG path. Default: spice/spice_chain_plots.png",
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
        f"Missing {DATA_PATH}. Run ngspice -b spice/alarm_chain_behavioral.cir "
        "from the repository root first.",
        file=sys.stderr,
    )
    raise SystemExit(1)

try:
    data = np.loadtxt(DATA_PATH, skiprows=1)
except (OSError, ValueError) as exc:
    print(f"Could not parse ngspice output {DATA_PATH}: {exc}", file=sys.stderr)
    raise SystemExit(1)

if data.ndim != 2 or data.shape[1] < 8 or data.shape[0] < 2:
    print(
        "Unexpected SPICE data layout. Expected at least 8 columns: "
        "time, S, UREF, DOUT, RESET, CT, OUT, BZ_COL.",
        file=sys.stderr,
    )
    raise SystemExit(1)

time_s, sensor_v, reference_v, dout_v, reset_v, timer_cap_v, timer_out_v, buzzer_col_v = (data[:, i] for i in range(8))

fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)

axes[0].plot(time_s, sensor_v, label="A1.S stimulus")
axes[0].plot(time_s, reference_v, label="U_REF")
axes[0].set_ylabel("Voltage, V")
axes[0].set_title("Sensor stimulus and comparator reference")
axes[0].legend(loc="best")
axes[0].grid(True, alpha=0.3)

axes[1].plot(time_s, dout_v, label="DOUT'")
axes[1].plot(time_s, reset_v, label="RESET DA1")
axes[1].set_ylabel("Voltage, V")
axes[1].set_title("Comparator output and timer reset")
axes[1].legend(loc="best")
axes[1].grid(True, alpha=0.3)

axes[2].plot(time_s, timer_cap_v, label="C1 voltage")
axes[2].plot(time_s, timer_out_v, label="DA1 OUT proxy")
axes[2].set_ylabel("Voltage, V")
axes[2].set_xlabel("Time, s")
axes[2].set_title("Timer timing capacitor and output")
axes[2].legend(loc="best")
axes[2].grid(True, alpha=0.3)

fig.tight_layout()
PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(PLOT_PATH, dpi=160)
print(f"Saved plot to {PLOT_PATH}")
