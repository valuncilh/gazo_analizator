#!/bin/sh
# Fetch official TI SPICE model archives into a temporary directory for inspection.
# Vendor binaries and model text are not committed into the repository.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

WORK_DIR="\${TMPDIR:-/tmp}/gazo_analizator_vendor_models"
LOG_PATH="spice/vendor_model_probe.log"
mkdir -p "$WORK_DIR"
: > "$LOG_PATH"

download_model() {
    model_name="$1"
    model_url="$2"
    archive="$WORK_DIR/$model_name.zip"
    target="$WORK_DIR/$model_name"
    mkdir -p "$target"

    {
        echo "=== $model_name ==="
        echo "URL: $model_url"
        if ! curl --fail --location --silent --show-error --retry 2 "$model_url" -o "$archive"; then
            echo "DOWNLOAD_FAILED"
            return 0
        fi
        if ! unzip -oq "$archive" -d "$target"; then
            echo "EXTRACT_FAILED"
            return 0
        fi
        echo "Extracted files:"
        find "$target" -type f -printf '%P\n' | sort
        echo "Subcircuit/model declarations:"
        grep -R -I -n -E '^[[:space:]]*\.SUBCKT|^[[:space:]]*\.MODEL|^[[:space:]]*SUBCKT' "$target" || true
        echo "=== end $model_name ==="
    } >> "$LOG_PATH" 2>&1
}

download_model "ti_tlv704x_pspice" "https://www.ti.com/lit/zip/SLVMDH0"
download_model "ti_tlc555_pspice" "https://www.ti.com/lit/zip/SLFJ002E"

echo "Vendor model probe written to $LOG_PATH"
