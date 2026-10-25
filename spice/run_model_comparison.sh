#!/bin/sh
# Compare the control chain under one shared synthetic sensor-voltage schedule.
# The direct S source deliberately isolates comparator/timer/output behavior.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

if ! command -v ngspice >/dev/null 2>&1; then
    echo "ngspice is required to run the model comparison." >&2
    exit 127
fi

WORK_DIR="${TMPDIR:-/tmp}/gazo_analizator_vendor_models"
if [ ! -d "$WORK_DIR/ti_tlv704x_pspice" ] || [ ! -d "$WORK_DIR/ti_tlc555_pspice" ]; then
    sh spice/fetch_vendor_models.sh
fi

TLV_LIB=$(find "$WORK_DIR/ti_tlv704x_pspice" -type f -iname "tlv7041.lib" -print -quit)
TLC_LIB=$(find "$WORK_DIR/ti_tlc555_pspice" -type f -iname "TLC555_6.LIB" -print -quit)
if [ -z "$TLV_LIB" ] || [ -z "$TLC_LIB" ]; then
    echo "Could not locate the TI libraries. See spice/vendor_model_probe.log." >&2
    exit 2
fi

printf 'set ngbehavior=ps\n' > "$WORK_DIR/.spiceinit"
BEHAVIORAL_NETLIST="$WORK_DIR/alarm_chain_behavioral_comparison.cir"
VENDOR_NETLIST="$WORK_DIR/alarm_chain_vendor_comparison.cir"

python3 - "$TLV_LIB" "$TLC_LIB" "$BEHAVIORAL_NETLIST" "$VENDOR_NETLIST" <<'PY'
from pathlib import Path
import sys

tlv_lib, tlc_lib, behavioral_path, vendor_path = sys.argv[1:]
common_input = (
    "PWL(0 0.926 0.79 0.926 0.81 2.500 "
    "1.59 2.500 1.61 3.125 2.39 3.125 2.41 0.926 4.0 0.926)"
)

behavioral = Path("spice/alarm_chain_behavioral.cir").read_text()
old_source = "VSENSE S 0 PWL(0 0.30 0.20 0.30 0.80 4.50 1.40 4.50 1.60 0.30 3.00 0.30)"
if old_source not in behavioral:
    raise SystemExit("Could not find the expected behavioral sensor source line")
behavioral = behavioral.replace(old_source, f"VSENSE S 0 {common_input}")
behavioral = behavioral.replace("RP1A VCC UREF 5k", "RP1A VCC UREF 5.2k", 1)
behavioral = behavioral.replace("RP1B UREF 0 5k", "RP1B UREF 0 4.8k", 1)

old_wrdata = (
    "wrdata spice/spice_chain_results.dat "
    "v(S) v(UREF) v(DOUT) v(RESET) v(CT) v(OUT) v(BZ_COL)"
)
new_wrdata = (
    "let supply_current = -i(VCCSRC)\n"
    "wrdata spice/model_comparison_behavioral.dat "
    "v(S) v(UREF) v(DOUT) v(RESET) v(CT) v(OUT) v(BZ_COL) supply_current v(HL1_A) v(R9_N) v(VT2_B)"
)
if old_wrdata not in behavioral:
    raise SystemExit("Could not find the expected behavioral wrdata line")
behavioral = behavioral.replace(old_wrdata, new_wrdata, 1)
behavioral = behavioral.replace(
    "let supply_current = -i(VCCSRC)\nmeas tran i_modelled_circuit_peak MAX supply_current",
    "meas tran i_modelled_circuit_peak MAX supply_current",
    1,
)

behavioral_measure = (
    "meas tran t_reset_fall WHEN v(RESET)=2.5 FALL=1\n"
    "meas tran sensor_clean_air FIND v(S) AT=0.5\n"
    "meas tran sensor_1000ppm FIND v(S) AT=1.2\n"
    "meas tran sensor_5000ppm FIND v(S) AT=2.0\n"
    "meas tran sensor_clean_air_after FIND v(S) AT=3.0\n"
    "meas tran reset_air_initial FIND v(RESET) AT=0.5\n"
    "meas tran reset_at_1000ppm FIND v(RESET) AT=1.2\n"
    "meas tran reset_at_5000ppm FIND v(RESET) AT=2.0\n"
    "meas tran reset_clean_after FIND v(RESET) AT=3.0\n"
    "meas tran i_modelled_current_standby AVG supply_current FROM=0.2 TO=0.7\n"
    "meas tran i_modelled_current_alarm AVG supply_current FROM=1.0 TO=1.5\n"
    "meas tran i_modelled_current_5000ppm AVG supply_current FROM=1.8 TO=2.3"
)
period_line = (
    "meas tran t_alarm_period_steady TRIG v(OUT) VAL=2.5 RISE=2 "
    "TARG v(OUT) VAL=2.5 RISE=3"
)
if period_line not in behavioral:
    raise SystemExit("Could not find the behavioral steady-period measurement")
behavioral = behavioral.replace(period_line, period_line + "\n" + behavioral_measure, 1)
Path(behavioral_path).write_text(behavioral)

vendor = Path("spice/alarm_chain_vendor.cir.in").read_text()
start_marker = "* Приближённый чувствительный элемент MQ-4 по библиотеке Amperka TroykaMQ и"
end_marker = "* UREF около 2,4 В."
start = vendor.find(start_marker)
end = vendor.find(end_marker, start + len(start_marker))
if start < 0 or end < 0:
    raise SystemExit("Could not locate the vendor sensor block markers")
replacement = (
    "* Сравнительный тест: общий источник S изолирует электронную цепочку от датчика.\n"
    f"VSENSE S 0 {common_input}\n\n"
)
vendor = vendor[:start] + replacement + vendor[end:]
vendor = vendor.replace("@TLV7041_LIB@", tlv_lib)
vendor = vendor.replace("@TLC555_LIB@", tlc_lib)

old_wrdata_vendor = (
    "wrdata spice/vendor_model_results.dat "
    "v(S) v(UREF) v(DOUT) v(RESET) v(CT) v(OUT) v(BZ_COL)"
)
new_wrdata_vendor = (
    "let modelled_current = -i(VCCSRC)\n"
    "wrdata spice/model_comparison_vendor.dat "
    "v(S) v(UREF) v(DOUT) v(RESET) v(CT) v(OUT) v(BZ_COL) modelled_current v(HL1_A) v(R9_N) v(VT2_B)"
)
if old_wrdata_vendor not in vendor:
    raise SystemExit("Could not find the expected vendor wrdata line")
vendor = vendor.replace(old_wrdata_vendor, new_wrdata_vendor, 1)
vendor = vendor.replace(
    "let modelled_current = -i(VCCSRC)\nmeas tran i_vendor_model_peak MAX modelled_current",
    "meas tran i_vendor_model_peak MAX modelled_current",
    1,
)
vendor_measure = (
    "meas tran t_reset_fall WHEN v(RESET)=2.5 FALL=1\n"
    "meas tran sensor_clean_air FIND v(S) AT=0.5\n"
    "meas tran sensor_1000ppm FIND v(S) AT=1.2\n"
    "meas tran sensor_5000ppm FIND v(S) AT=2.0\n"
    "meas tran sensor_clean_air_after FIND v(S) AT=3.0\n"
    "meas tran reset_air_initial FIND v(RESET) AT=0.5\n"
    "meas tran reset_at_1000ppm FIND v(RESET) AT=1.2\n"
    "meas tran reset_at_5000ppm FIND v(RESET) AT=2.0\n"
    "meas tran reset_clean_after FIND v(RESET) AT=3.0\n"
    "meas tran i_vendor_current_standby AVG modelled_current FROM=0.2 TO=0.7\n"
    "meas tran i_vendor_current_alarm AVG modelled_current FROM=1.0 TO=1.5\n"
    "meas tran i_vendor_current_5000ppm AVG modelled_current FROM=1.8 TO=2.3"
)
vendor_period = (
    "meas tran t_alarm_period TRIG v(OUT) VAL=2.5 RISE=2 "
    "TARG v(OUT) VAL=2.5 RISE=3"
)
if vendor_period not in vendor:
    raise SystemExit("Could not find the vendor steady-period measurement")
vendor = vendor.replace(vendor_period, vendor_period + "\n" + vendor_measure, 1)
Path(vendor_path).write_text(vendor)
PY

echo "[1/3] Run behavioral control-chain model with shared S input"
ngspice -b "$BEHAVIORAL_NETLIST" > spice/model_comparison_behavioral.log 2>&1
test -s spice/model_comparison_behavioral.dat

echo "[2/3] Run vendor control-chain model with the same S input"
HOME="$WORK_DIR" ngspice -b "$VENDOR_NETLIST" > spice/model_comparison_vendor.log 2>&1
test -s spice/model_comparison_vendor.dat

echo "[3/3] Check common input, state sequence, timing and current averages"
python3 - <<'PY'
from pathlib import Path
import math
import re
import sys
import numpy as np

logs = {
    "behavioral": Path("spice/model_comparison_behavioral.log").read_text(errors="replace"),
    "vendor": Path("spice/model_comparison_vendor.log").read_text(errors="replace"),
}

def measure(model, name):
    pattern = rf"^{re.escape(name)}\s*=\s*([+-]?[0-9.eE+-]+)"
    match = re.search(pattern, logs[model], re.MULTILINE)
    if not match:
        print(f"ERROR: {model}: missing measurement {name}", file=sys.stderr)
        raise SystemExit(1)
    value = float(match.group(1))
    if not math.isfinite(value):
        print(f"ERROR: {model}: non-finite {name}", file=sys.stderr)
        raise SystemExit(1)
    return value

for model in logs:
    print(f"--- {model} ---")
    for name in (
        "t_reset_rise", "t_reset_fall", "t_alarm_first_rise",
        "sensor_clean_air", "sensor_1000ppm", "sensor_5000ppm",
        "sensor_clean_air_after", "reset_air_initial", "reset_at_1000ppm",
        "reset_at_5000ppm", "reset_clean_after",
    ):
        print(f"{name}: {measure(model, name):.8g}")

sensor_checks = {
    "sensor_clean_air": 0.926,
    "sensor_1000ppm": 2.500,
    "sensor_5000ppm": 3.125,
    "sensor_clean_air_after": 0.926,
}
for model in logs:
    for name, expected in sensor_checks.items():
        actual = measure(model, name)
        if abs(actual - expected) > 0.02:
            raise SystemExit(f"ERROR: {model} {name}={actual:.6f} V, expected {expected:.3f} V")
    states = {
        "reset_air_initial": "low",
        "reset_at_1000ppm": "high",
        "reset_at_5000ppm": "high",
        "reset_clean_after": "low",
    }
    for name, state in states.items():
        actual = measure(model, name)
        valid = actual < 1.0 if state == "low" else actual > 2.5
        if not valid:
            raise SystemExit(f"ERROR: {model} RESET {state} test failed at {name}: {actual:.6f} V")

period_b = measure("behavioral", "t_alarm_period_steady")
period_v = measure("vendor", "t_alarm_period")
relative_delta = abs(period_b - period_v) / ((period_b + period_v) / 2.0)
reset_rise_b = measure("behavioral", "t_reset_rise")
reset_rise_v = measure("vendor", "t_reset_rise")
reset_fall_b = measure("behavioral", "t_reset_fall")
reset_fall_v = measure("vendor", "t_reset_fall")

print(f"steady period behavioral: {period_b:.8f} s")
print(f"steady period vendor:     {period_v:.8f} s")
print(f"relative period difference: {100*relative_delta:.4f} %")
print(f"RESET rise behavioral/vendor: {reset_rise_b:.8f} / {reset_rise_v:.8f} s")
print(f"RESET fall behavioral/vendor: {reset_fall_b:.8f} / {reset_fall_v:.8f} s")

if not (0.79 <= reset_rise_b <= 0.90 and 0.79 <= reset_rise_v <= 0.90):
    raise SystemExit("ERROR: RESET rise is not aligned with the shared 0.8 s stimulus")
if abs(reset_rise_b - reset_rise_v) > 0.05:
    raise SystemExit("ERROR: RESET rise timings differ by more than 50 ms")
if abs(reset_fall_b - reset_fall_v) > 0.05:
    raise SystemExit("ERROR: RESET fall timings differ by more than 50 ms")
if relative_delta > 0.01:
    raise SystemExit("ERROR: steady periods differ by more than 1 percent")

for model, names in {
    "behavioral": (
        "i_modelled_current_standby",
        "i_modelled_current_alarm",
        "i_modelled_current_5000ppm",
    ),
    "vendor": (
        "i_vendor_current_standby",
        "i_vendor_current_alarm",
        "i_vendor_current_5000ppm",
    ),
}.items():
    for name in names:
        value = measure(model, name)
        if value <= 0:
            raise SystemExit(f"ERROR: {model} {name} is not positive: {value:.6g} A")
        print(f"{model} {name}: {value*1000:.4f} mA")

# Attribute stable-window current differences to the three major output branches.
# Data vector order: t, S, UREF, DOUT, RESET, CT, OUT, BZ_COL, supply current,
# HL1_A, R9_N, VT2_B.
def weighted_mean(data, column, lo, hi):
    t = data[:, 0]
    mask = (t >= lo) & (t <= hi)
    x = t[mask]
    y = data[mask, column]
    if len(x) < 2 or x[-1] <= x[0]:
        raise SystemExit(f"ERROR: insufficient samples for {lo}-{hi} s window")
    return float(np.sum((y[:-1] + y[1:]) * 0.5 * np.diff(x)) / (x[-1] - x[0]))

def conditional_mean(data, value_column, condition_column, lo, hi, threshold):
    t = data[:, 0]
    mask = (t >= lo) & (t <= hi)
    x = t[mask]
    y = data[mask, value_column]
    c = data[mask, condition_column] > threshold
    if len(x) < 2:
        raise SystemExit(f"ERROR: insufficient samples for conditional mean {lo}-{hi} s")
    dt = np.diff(x)
    valid = c[:-1] & c[1:]
    duration = float(np.sum(dt[valid]))
    if duration <= 0:
        raise SystemExit("ERROR: no high-output interval was found for output level calculation")
    return float(np.sum((y[:-1][valid] + y[1:][valid]) * 0.5 * dt[valid]) / duration)

branch_results = {}
for model, filename in {
    "behavioral": "spice/model_comparison_behavioral.dat",
    "vendor": "spice/model_comparison_vendor.dat",
}.items():
    data = np.loadtxt(filename, skiprows=1)
    if data.ndim != 2 or data.shape[1] < 12:
        raise SystemExit(f"ERROR: {filename} has {data.shape[1]} columns, expected at least 12")
    if not np.isfinite(data[:, :12]).all():
        raise SystemExit(f"ERROR: {filename} contains non-finite data")
    out = data[:, 6]
    bz_col = data[:, 7]
    hl1_a = data[:, 9]
    r9_n = data[:, 10]
    currents = {
        "HL1_R6": (out - hl1_a) / 220.0,
        "VT2_base_R9": (out - r9_n) / 560.0,
        "RBZ_load": (5.0 - bz_col) / 166.7,
    }
    branch_results[model] = {}
    high_out = conditional_mean(data, 6, 6, 1.0, 1.5, 2.5)
    print(f"{model} mean OUT while high: {high_out:.6f} V")
    for branch_name, current in currents.items():
        data_with_current = np.column_stack((data, current))
        column = data_with_current.shape[1] - 1
        for label, lo, hi in (("alarm", 1.0, 1.5), ("gas_5000ppm", 1.8, 2.3)):
            value = weighted_mean(data_with_current, column, lo, hi)
            branch_results[model][f"{branch_name}_{label}"] = value
            print(f"{model} {branch_name} mean {label}: {1000*value:.4f} mA")
        if np.max(current) <= 0:
            raise SystemExit(f"ERROR: {model} {branch_name} never conducts")
    branch_results[model]["out_high_mean"] = high_out

out_difference = abs(branch_results["behavioral"]["out_high_mean"] - branch_results["vendor"]["out_high_mean"])
print(f"Loaded high-level OUT difference: {out_difference:.6f} V")
for branch_name in ("HL1_R6", "VT2_base_R9", "RBZ_load"):
    b = branch_results["behavioral"][f"{branch_name}_alarm"]
    v = branch_results["vendor"][f"{branch_name}_alarm"]
    print(f"Alarm branch {branch_name}: behavioral={1000*b:.4f} mA, vendor={1000*v:.4f} mA")

print("Shared-input model comparison passed. Branch currents are derived from simulated node voltages, not hardware measurements.")
PY

python3 spice/plot_model_comparison.py
