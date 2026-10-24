#!/bin/sh
# Run baseline C1=4.7 uF and comparison C1=47 uF.
# Works when invoked from any current directory and is compatible with /bin/sh.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

if ! command -v ngspice >/dev/null 2>&1; then
    echo "ngspice is required. On CachyOS or Arch Linux, install it with: sudo pacman -S ngspice" >&2
    exit 127
fi

BASE_LOG="spice/ngspice.log"
BASE_DATA="spice/spice_chain_results.dat"
VARIANT_LOG="spice/ngspice_47u.log"
VARIANT_DATA="spice/spice_chain_results_47u.dat"
VARIANT_NETLIST="/tmp/gazo_alarm_chain_47u.cir"

echo "[1/3] Running baseline with C1=4.7 uF"
ngspice -b spice/alarm_chain_behavioral.cir > "$BASE_LOG" 2>&1
test -s "$BASE_DATA"
grep -q "t_alarm_period_steady" "$BASE_LOG"
cp "$BASE_DATA" "spice/spice_chain_results_4p7u.dat"

echo "[2/3] Running comparison with C1=47 uF and a longer alarm stimulus"
sed \
    -e 's/^\.param C_TIMER=4\.7u$/.param C_TIMER=47u/' \
    -e 's@^VSENSE S 0 PWL(.*@VSENSE S 0 PWL(0 0.30 0.20 0.30 0.80 4.50 3.80 4.50 4.00 0.30 5.00 0.30)@' \
    -e 's/^tran 0\.1m 3\.0$/tran 0.1m 5.0/' \
    -e 's@spice/spice_chain_results\.dat@spice/spice_chain_results_47u.dat@' \
    spice/alarm_chain_behavioral.cir > "$VARIANT_NETLIST"
ngspice -b "$VARIANT_NETLIST" > "$VARIANT_LOG" 2>&1
test -s "$VARIANT_DATA"
grep -q "t_alarm_period_steady" "$VARIANT_LOG"

echo "[3/3] Checking modelled periods and plotting baseline"
python3 - <<'PY'
from pathlib import Path
import re
import sys

checks = [
    (Path("spice/ngspice.log"), 0.0802, 0.075, 0.085, "baseline C1=4.7uF"),
    (Path("spice/ngspice_47u.log"), 0.802, 0.75, 0.85, "comparison C1=47uF"),
]
ok = True
pattern = re.compile(r"t_alarm_period_steady\s*=\s*([0-9.eE+-]+)")
for path, expected, low, high, label in checks:
    match = pattern.search(path.read_text(errors="replace"))
    if match is None:
        print(f"ERROR: no steady-period measurement in {path}", file=sys.stderr)
        ok = False
        continue
    actual = float(match.group(1))
    print(f"{label}: steady period = {actual:.8f} s (expected near {expected:.4f} s)")
    if not low <= actual <= high:
        print(f"ERROR: period {actual:.8f} s outside [{low}, {high}] s", file=sys.stderr)
        ok = False
if not ok:
    raise SystemExit(1)
PY
python3 -m py_compile spice/plot_results.py
python3 spice/plot_results.py

echo "SPICE comparison passed. Logs and data files are in the spice/ directory."
