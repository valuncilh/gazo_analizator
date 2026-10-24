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
python3 -m py_compile spice/plot_results.py
python3 spice/plot_results.py --input spice/vendor_model_results.dat --output spice/vendor_chain_plots.png

echo "Vendor-model transient test completed. See spice/vendor_model_test.log and spice/vendor_chain_plots.png."
