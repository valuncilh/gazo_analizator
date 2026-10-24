#!/bin/sh
# Fetch the official TI model archives if needed, generate a temporary netlist,
# and test them in ngspice without committing vendor model libraries.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

WORK_DIR="\${TMPDIR:-/tmp}/gazo_analizator_vendor_models"
if [ ! -d "$WORK_DIR/ti_tlv704x_pspice" ] || [ ! -d "$WORK_DIR/ti_tlc555_pspice" ]; then
    sh spice/fetch_vendor_models.sh
fi

TLV_LIB=$(find "$WORK_DIR/ti_tlv704x_pspice" -type f -iname "tlv7041.lib" -print -quit)
TLC_LIB=$(find "$WORK_DIR/ti_tlc555_pspice" -type f -iname "TLC555_6.LIB" -print -quit)

if [ -z "$TLV_LIB" ] || [ -z "$TLC_LIB" ]; then
    echo "Could not locate both vendor model libraries. See spice/vendor_model_probe.log." >&2
    exit 2
fi

TMP_NETLIST="$WORK_DIR/alarm_chain_vendor.cir"
sed \
    -e "s|@TLV7041_LIB@|$TLV_LIB|g" \
    -e "s|@TLC555_LIB@|$TLC_LIB|g" \
    spice/alarm_chain_vendor.cir.in > "$TMP_NETLIST"

# PSpice vendor libraries use constructs such as VSWITCH, VT, and if().
# Tell ngspice to translate the included PSpice libraries before parsing them.
printf 'set ngbehavior=ps\n' > "$WORK_DIR/.spiceinit"
HOME="$WORK_DIR" ngspice -b "$TMP_NETLIST" > spice/vendor_model_test.log 2>&1
test -s spice/vendor_model_results.dat
grep -q "t_reset_rise" spice/vendor_model_test.log
grep -q "t_alarm_period" spice/vendor_model_test.log

python3 - <<'PY'
from pathlib import Path
import re
import sys

log = Path("spice/vendor_model_test.log").read_text(errors="replace")
checks = {
    "sensor_clean_air": (0.926, 0.88, 0.98),
    "sensor_1000ppm": (2.500, 2.45, 2.55),
    "sensor_5000ppm": (3.125, 3.05, 3.20),
    "sensor_clean_air_after": (0.926, 0.88, 0.98),
}
for name, (expected, low, high) in checks.items():
    match = re.search(rf"^{name}\s*=\s*([0-9.eE+-]+)", log, re.MULTILINE)
    if match is None:
        print(f"ERROR: {name} measurement missing from ngspice log", file=sys.stderr)
        raise SystemExit(1)
    value = float(match.group(1))
    print(f"{name}: {value:.6f} V")
    if not low <= value <= high:
        print(f"ERROR: {name}={value:.6f} V outside [{low}, {high}] V", file=sys.stderr)
        raise SystemExit(1)

for name, state in [("reset_air_initial", "low"), ("reset_at_1000ppm", "high"), ("reset_clean_after", "low")]:
    match = re.search(rf"^{name}\s*=\s*([0-9.eE+-]+)", log, re.MULTILINE)
    if match is None:
        print(f"ERROR: {name} measurement missing from ngspice log", file=sys.stderr)
        raise SystemExit(1)
    value = float(match.group(1))
    print(f"{name}: {value:.6f} V")
    valid = value < 1.0 if state == "low" else value > 2.5
    if not valid:
        print(f"ERROR: RESET did not reach expected {state} state at {name}", file=sys.stderr)
        raise SystemExit(1)
PY

# Verify the sound-enabled indicator branch draws current through HL2.
python3 - <<'PY'
from pathlib import Path
import re
import sys

log = Path("spice/vendor_model_test.log").read_text(errors="replace")
match = re.search(r"^i_hl2_peak\\s*=\\s*([0-9.eE+-]+)", log, re.MULTILINE)
if match is None:
    print("ERROR: enabled HL2 current measurement is missing", file=sys.stderr)
    raise SystemExit(1)
current = float(match.group(1))
print(f"HL2 peak current with SOUND_ENABLE=1: {current:.6g} A")
if current < 1e-4:
    print("ERROR: HL2 branch is not conducting when enabled", file=sys.stderr)
    raise SystemExit(1)
PY

# Run the same circuit with sound and HL2 disabled. The indicator current must
# fall to leakage-level values, proving that the control switch is in series.
OFF_NETLIST="$WORK_DIR/alarm_chain_vendor_sound_off.cir"
sed \\
    -e 's/^\\.param SOUND_ENABLE=1$/.param SOUND_ENABLE=0/' \\
    -e 's@spice/vendor_model_results.dat@spice/vendor_model_results_sound_off.dat@' \\
    "$TMP_NETLIST" > "$OFF_NETLIST"
HOME="$WORK_DIR" ngspice -b "$OFF_NETLIST" > spice/vendor_model_sound_off.log 2>&1
test -s spice/vendor_model_results_sound_off.dat
grep -q "i_hl2_peak" spice/vendor_model_sound_off.log
python3 - <<'PY'
from pathlib import Path
import re
import sys

log = Path("spice/vendor_model_sound_off.log").read_text(errors="replace")
match = re.search(r"^i_hl2_peak\\s*=\\s*([0-9.eE+-]+)", log, re.MULTILINE)
if match is None:
    print("ERROR: disabled HL2 current measurement is missing", file=sys.stderr)
    raise SystemExit(1)
current = float(match.group(1))
print(f"HL2 peak current with SOUND_ENABLE=0: {current:.6g} A")
if current > 1e-7:
    print("ERROR: HL2 still conducts when disabled", file=sys.stderr)
    raise SystemExit(1)
PY

python3 -m py_compile spice/plot_results.py
python3 spice/plot_results.py --input spice/vendor_model_results.dat --output spice/vendor_chain_plots.png

echo "Vendor-model transient test completed. See SPICE logs and spice/vendor_chain_plots.png."
