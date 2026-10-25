#!/usr/bin/env python3
"""Регрессионная проверка функциональной топологии предварительного Э3."""
from pathlib import Path
import sys

from generate_preliminary_drawings import electrical_topology_sheet

HERE = Path(__file__).resolve().parent
SOURCE = (HERE / "generate_preliminary_drawings.py").read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"ОШИБКА: {message}", file=sys.stderr)
        raise SystemExit(1)


def main() -> int:
    # DA1 OUT must branch to HL1 and the serial R9+SA1 block. The only drawn
    # path from that block to the sounder must be labeled as the VT2 base path.
    required_paths = (
        'ln(280,76,280,102,0.40)',
        'ln(280,102,280,118,0.40)',
        'ln(306,132,330,132,0.40)',
    )
    for path in required_paths:
        require(path in SOURCE, f"Потерян ожидаемый путь топологии: {path}")

    forbidden_bypass = (
        'ln(280,102,359,102,0.30,"4 2")',
        'ln(359,102,359,118,0.30,"4 2")',
    )
    for path in forbidden_bypass:
        require(path not in SOURCE, f"Найдена линия, обходящая R9/SA1: {path}")

    svg = electrical_topology_sheet()
    require("DA1" in svg and "R9 + SA1" in svg and "VT2 / HA1" in svg,
            "На функциональной топологии отсутствует один из блоков выходной цепи")
    require("VT2 base" in svg, "Не подписан путь управления базой VT2")
    require('stroke-dasharray="4 2"' not in svg,
            "Пунктирная связь может быть прочитана как прямой обход R9/SA1")

    print("Тест функциональной топологии пройден: DA1 → R9/SA1 → база VT2, прямой обход отсутствует.")
    print("Ограничение: это блок-схема, а не полноценная Э3. Netlist parity и аппаратная приёмка остаются открытыми.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
