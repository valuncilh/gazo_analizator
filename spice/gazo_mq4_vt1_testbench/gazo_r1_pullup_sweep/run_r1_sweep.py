#!/usr/bin/env python3
"""Generate and run an R1 pull-up sensitivity sweep for the GAZO DOUT/KT3102B stage.

This is an exploratory DC model, not a vendor model of SEN-MQ4-V2 or KT3102B.
It keeps R2=13k and R3=2k and tests alternative R1 values without changing
any project files or recommending a hardware modification.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

BETAS = (50, 200, 500)
R1_VALUES = (
    ("160k", "160k"),
    ("100k", "100k"),
    ("82k", "82k"),
    ("68k", "68k"),
    ("56k", "56k"),
    ("47k", "47k"),
    ("33k", "33k"),
    ("22k", "22k"),
    ("10k", "10k"),
    ("6k8", "6.8k"),
    ("4k7", "4.7k"),
    ("3k3", "3.3k"),
)


def make_deck(beta: int) -> str:
    lines = [
        "* GAZO.001 — R1 pull-up sensitivity, DOUT open-collector assumption",
        "* Controlled DC sweep only. Not a physical sensor/NE555 vendor model.",
        f".title GAZO R1 pull-up sweep, estimated KT3102B BF={beta}",
        ".param VCCVAL=5",
        ".param R2VAL=13k",
        ".param R3VAL=2k",
        ".param ROCLOW=10",
        f".model QKT3102B_EST NPN (IS=1e-14 BF={beta} VAF=80 IKF=0.05 CJE=12p CJC=5p TF=0.5n TR=10n RB=100 RC=10 RE=1)",
        "VMAIN VCC 0 DC {VCCVAL}",
        "",
        "* OC RELEASED: external R1 is the only pull-up, feeding the base through R2.",
    ]
    for tag, value in R1_VALUES:
        lines.extend([
            f"RPU_REL_{tag} VCC DREL_{tag} {value}",
            f"R2_REL_{tag} DREL_{tag} BREL_{tag} {{R2VAL}}",
            f"Q_REL_{tag} RESET_REL_{tag} BREL_{tag} 0 QKT3102B_EST",
            f"R3_REL_{tag} VCC RESET_REL_{tag} {{R3VAL}}",
        ])
    lines.extend(["", "* OC ASSERTED LOW: same R1, output sink approximated by 10 ohm."])
    for tag, value in R1_VALUES:
        lines.extend([
            f"RPU_LOW_{tag} VCC DLOW_{tag} {value}",
            f"ROC_LOW_{tag} DLOW_{tag} 0 {{ROCLOW}}",
            f"R2_LOW_{tag} DLOW_{tag} BLOW_{tag} {{R2VAL}}",
            f"Q_LOW_{tag} RESET_LOW_{tag} BLOW_{tag} 0 QKT3102B_EST",
            f"R3_LOW_{tag} VCC RESET_LOW_{tag} {{R3VAL}}",
        ])
    lines.extend(["", ".control", "set noaskquit", "op", ""])
    lines.extend([
        'echo "============================================================"',
        f'echo "R1 SWEEP — estimated BF={beta}, VCC=5V, R2=13k, R3=2k"',
        'echo "OC RELEASED: v(dout), v(base), v(reset), ibase, icollector"',
        'echo "OC LOW: v(dout), v(reset), pull-up sink current"',
        'echo "RESET threshold reference: TI NE555 at 5V, 0.3/0.7/1.0V min/typ/max"',
        'echo "============================================================"',
    ])
    for tag, value in R1_VALUES:
        lines.extend([
            f"let ib_rel_{tag} = (v(drel_{tag})-v(brel_{tag}))/{value if value else '160k'}",
            # Base resistor remains 13k, not R1. Replace expression to avoid confusion.
            f"let ib_rel_{tag} = (v(drel_{tag})-v(brel_{tag}))/13k",
            f"let ic_rel_{tag} = (5-v(reset_rel_{tag}))/2k",
            f"let ipu_low_{tag} = (5-v(dlow_{tag}))/{value}",
            f'echo "R1={value} OC RELEASED"',
            f"print v(drel_{tag}) v(brel_{tag}) v(reset_rel_{tag}) ib_rel_{tag} ic_rel_{tag}",
            f'echo "R1={value} OC LOW"',
            f"print v(dlow_{tag}) v(reset_low_{tag}) ipu_low_{tag}",
        ])
    lines.extend(["", "quit", ".endc", ".end", ""])
    # Drop a redundant first assignment line if present (keeps only the correct /13k).
    cleaned = []
    for line in lines:
        if line.startswith("let ib_rel_") and "/13k" not in line:
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def main() -> int:
    ngspice = shutil.which("ngspice")
    if not ngspice:
        print("ОШИБКА: ngspice не найден. Установи: sudo pacman -S ngspice", file=sys.stderr)
        return 2

    root = Path(__file__).resolve().parent
    results = root / "results"
    results.mkdir(parents=True, exist_ok=True)
    failures = []

    print(f"ngspice: {ngspice}")
    print("R1 sweep: 160k, 100k, 82k, 68k, 56k, 47k, 33k, 22k, 10k, 6.8k, 4.7k, 3.3k")
    print("Сценарии: OC RELEASED и OC LOW. Значения R1 — только исследуемые варианты, не рекомендации.")

    for beta in BETAS:
        deck = results / f"r1_sweep_beta_{beta}.cir"
        log = results / f"r1_sweep_beta_{beta}.log"
        deck.write_text(make_deck(beta), encoding="utf-8")
        completed = subprocess.run(
            [ngspice, "-b", str(deck)],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        log.write_text(completed.stdout, encoding="utf-8")
        if completed.returncode != 0 or "Error" in completed.stdout or "error" in completed.stdout:
            failures.append((beta, completed.returncode))
            print(f"FAIL BF={beta}. См. {log}")
        else:
            print(f"PASS BF={beta} -> {log}")

    summary = results / "README_RESULTS.txt"
    summary.write_text(
        "R1 pull-up sweep completed.\n"
        "Open each r1_sweep_beta_*.log. For OC RELEASED, RESET should be compared "
        "with the TI NE555 RESET voltage-level limits (min 0.3V, typ 0.7V, max 1.0V "
        "at the published test conditions). For OC LOW, ipu_low is the external "
        "pull-up current that the sensor output would need to sink in this simplified model.\n"
        "This is a sensitivity study only. It does not identify the actual Joy-IT DOUT "
        "output topology, polarity, permissible sink current, or the real KT3102B beta.\n"
        "Do not change the circuit based on this sweep alone.\n",
        encoding="utf-8",
    )
    if failures:
        print(f"Завершено с ошибками: {failures}")
        return 1
    print(f"Готово. Логи: {results}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
