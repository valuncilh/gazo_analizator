#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
OUT=spice/xschem_probe
SCH=docs/figures/xschem_probe/mq4_divider.sch
mkdir -p "$OUT"
: > "$OUT/xschem.log"

# Ubuntu installs the generic symbols here. Use a dedicated rc so the runner's
# generated ~/.xschem/xschemrc cannot point at a nonexistent user library.
test -d /usr/share/xschem/xschem_library/devices
test -s /usr/share/xschem/xschem_library/devices/res.sym
cat > "$OUT/xschemrc" <<'XSCHEMRC'
set XSCHEM_LIBRARY_PATH {/usr/share/xschem/xschem_library}
XSCHEMRC

xschem --version | tee "$OUT/xschem_version.txt"
xschem -n -s -x -q --rcfile "$OUT/xschemrc" --netlist_path "$OUT" --netlist_filename mq4_divider.spice "$SCH" > "$OUT/xschem.log" 2>&1
test -s "$OUT/mq4_divider.spice"

echo "=== Exported xschem SPICE netlist ==="
cat "$OUT/mq4_divider.spice"
grep -Eiq '^[[:space:]]*R_S[[:space:]]+VCC[[:space:]]+S[[:space:]]+88k([[:space:]]|$)' "$OUT/mq4_divider.spice"
grep -Eiq '^[[:space:]]*R_L[[:space:]]+S[[:space:]]+0[[:space:]]+20k([[:space:]]|$)' "$OUT/mq4_divider.spice"
grep -Eiq '^[[:space:]]*VCC[[:space:]]+VCC[[:space:]]+0[[:space:]]+5([[:space:]]|$)' "$OUT/mq4_divider.spice"

ngspice -b "$OUT/mq4_divider.spice" > "$OUT/mq4_divider.log" 2>&1
python3 - "$OUT/mq4_divider.log" <<'PY'
from pathlib import Path
import re
import sys

log = Path(sys.argv[1]).read_text(errors="replace")
m = re.search(r"v\(s\)\s*=\s*([0-9.eE+-]+)", log, re.IGNORECASE)
if m is None:
    print("ERROR: xschem probe did not report v(S)", file=sys.stderr)
    print(log, file=sys.stderr)
    raise SystemExit(1)
actual = float(m.group(1))
expected = 5.0 * 20.0 / (88.0 + 20.0)
print(f"xschem MQ-4 clean-air divider: v(S)={actual:.6f} V, hand calculation={expected:.6f} V")
if abs(actual - expected) > 0.005:
    print("ERROR: xschem netlist result does not match the manual divider calculation", file=sys.stderr)
    raise SystemExit(1)
PY

# Export a picture for visual comparison with docs/figures/fig02_mq4_equivalent.png.
xvfb-run -a xschem --png -q --rcfile "$OUT/xschemrc" "$SCH" > "$OUT/xschem_png_export.log" 2>&1
PNG=$(find docs/figures/xschem_probe -maxdepth 1 -type f -name 'mq4_divider.png' -print -quit)
if [ -z "$PNG" ]; then
    PNG=$(find . -maxdepth 5 -type f -name 'mq4_divider.png' -print -quit)
fi
if [ -z "$PNG" ] || [ ! -s "$PNG" ]; then
    echo "ERROR: xschem PNG export was not created" >&2
    cat "$OUT/xschem_png_export.log" >&2
    exit 1
fi
cp "$PNG" "$OUT/mq4_divider.png"
echo "xschem fragment export and netlist checks passed."
