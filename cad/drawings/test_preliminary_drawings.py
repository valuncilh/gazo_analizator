#!/usr/bin/env python3
"""Регрессионная проверка функциональной топологии предварительного Э3."""
from pathlib import Path
import re
import sys

from generate_preliminary_drawings import PCB, electrical_topology_sheet, pcb_sheet, read_footprints

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
        'ln(306,62,330,62,0.40)',
        'ln(312,62,312,102,0.40)',
        'ln(312,102,280,102,0.40)',
        'ln(280,102,280,118,0.40)',
        'circ(312,62,0.9,0.25,fill="#111")',
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
    require(\'stroke-dasharray="4 2"\' not in svg,
            "Пунктирная связь может быть прочитана как прямой обход R9/SA1")

    # A routed KiCad board is serialized differently by pcbnew.SaveBoard():
    # footprint positions may be on a separate line instead of the header.
    parts = read_footprints()
    require(len(parts) >= 20, f"Ожидалось не менее 20 площадочных footprints, получено {len(parts)}")
    board_svg = pcb_sheet(parts)
    board_text = PCB.read_text(encoding="utf-8")
    segment_count = len(re.findall(r"\\(segment\\b", board_text))
    via_count = len(re.findall(r"\\(via\\b", board_text))
    if segment_count + via_count:
        require("Автотрассировка:" in board_svg,
                "На чертеже платы не отражена фактическая автотрассировка")
        require("Проверить DRC, связность и маршрут вручную." in board_svg,
                "На чертеже платы отсутствует предупреждение о проверке маршрута")
    else:
        require("Плата не трассирована." in board_svg,
                "Для платы без меди чертёж должен явно сообщать, что она не трассирована")

    print(f"Прочитано footprints: {len(parts)}. Медные сегменты: {segment_count}; переходы: {via_count}.")
    print("Тест функциональной топологии и отражения статуса трассировки пройден.")
    print("Тест функциональной топологии пройден: DA1 → R9/SA1 → база VT2, прямой обход отсутствует.")
    print("Ограничение: это блок-схема, а не полноценная Э3. Netlist parity и аппаратная приёмка остаются открытыми.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
