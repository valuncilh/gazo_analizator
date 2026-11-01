#!/usr/bin/env python3
"""Generate and run the GAZO DOUT/KT3102B SPICE sensitivity matrix."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
TEMPLATE = ROOT / "matrix_template.cir.in"
BETA_CASES = (50, 200, 500)


def main() -> int:
    ngspice = shutil.which("ngspice")
    if ngspice is None:
        print("ОШИБКА: ngspice не найден в PATH.")
        print("Для CachyOS установи его командой: sudo pacman -S ngspice")
        return 2

    RESULTS.mkdir(exist_ok=True)
    template = TEMPLATE.read_text(encoding="utf-8")
    generated: list[tuple[Path, Path]] = []

    for beta in BETA_CASES:
        deck = ROOT / f"matrix_beta_{beta}.cir"
        log = RESULTS / f"matrix_beta_{beta}.log"
        deck.write_text(template.replace("@BF@", str(beta)), encoding="utf-8")
        generated.append((deck, log))

    analog_deck = ROOT / "mq4_ratio_transfer.cir"
    analog_log = RESULTS / "mq4_ratio_transfer.log"
    generated.append((analog_deck, analog_log))

    failures = 0
    print(f"ngspice: {ngspice}")
    print("Запускаю три варианта усиления KT3102B и отдельную модель Rs/R0 → AOUT.\n")

    for deck, log in generated:
        command = [ngspice, "-b", "-o", str(log), str(deck)]
        print(f"RUN  {deck.name}")
        try:
            proc = subprocess.run(command, cwd=ROOT, check=False)
        except OSError as exc:
            print(f"ОШИБКА запуска {deck.name}: {exc}")
            failures += 1
            continue
        if proc.returncode != 0:
            print(f"FAIL {deck.name}: код {proc.returncode}, смотри {log}")
            failures += 1
            continue
        if not log.exists() or log.stat().st_size == 0:
            print(f"FAIL {deck.name}: лог отсутствует или пустой")
            failures += 1
            continue
        log_text = log.read_text(encoding="utf-8", errors="replace")
        error_markers = ("Error on line", "Fatal error", "No. such vector", "vector not found")
        if any(marker.lower() in log_text.lower() for marker in error_markers):
            print(f"FAIL {deck.name}: в логе найдена ошибка ngspice, смотри {log}")
            failures += 1
            continue
        if deck == analog_deck and "aout_ratio44" not in log_text.lower():
            print(f"FAIL {deck.name}: нет ожидаемого вывода AOUT_RATIO44, смотри {log}")
            failures += 1
            continue
        if deck != analog_deck and "reset_pplow" not in log_text.lower():
            print(f"FAIL {deck.name}: нет ожидаемого вывода RESET_PPLOW, смотри {log}")
            failures += 1
            continue
        print(f"PASS {deck.name} -> {log.relative_to(ROOT)}")

    print("\nГотово.")
    print(f"Логи: {RESULTS}")
    if failures:
        print(f"Сбоев: {failures}. Приложи все логи из results.")
        return 1
    print("Все задания ngspice завершились без кода ошибки.")
    print("Это проверка исполнения netlist, а не подтверждение модели физической платы.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
