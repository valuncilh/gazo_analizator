#!/usr/bin/env python3
"""Run a cautious FreeRouting pass on the generated preliminary KiCad board.

The router output is only a draft. Subsequent KiCad DRC and unconnected checks
remain mandatory, and this script never generates manufacturing deliverables.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PCB = ROOT / "cad/kicad/gazo_analizator_preliminary.kicad_pcb"
OUT = ROOT / "cad/output"
DSN = OUT / "gazo_analizator_preliminary.dsn"
SES = OUT / "gazo_analizator_preliminary.ses"
LOG = OUT / "freerouting_autoroute.log"
REPORT = OUT / "autoroute_report.json"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    router = os.environ.get("FREEROUTING_BIN")
    if not router:
        for candidate in ("freeRouting", "freerouting", "freerouting-cli"):
            found = shutil.which(candidate)
            if found:
                router = found
                break
    if not router or not Path(router).is_file():
        raise SystemExit("FreeRouting CLI binary was not supplied by the CAD workflow.")
    if not PCB.is_file():
        raise SystemExit(f"Generated PCB not found: {PCB}")

    with LOG.open("w", encoding="utf-8") as log:
        log.write(f"Router binary: {router}\n")
        log.write(f"Input board: {PCB}\n")
        log.flush()
        export = subprocess.run(
            ["kicad-cli", "pcb", "export", "specctra", "--output", str(DSN), str(PCB)],
            cwd=ROOT,
            text=True,
            stdout=log,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if export.returncode != 0 or not DSN.is_file() or DSN.stat().st_size == 0:
            raise SystemExit(f"KiCad Specctra DSN export failed. See {LOG}")
        log.write(f"\nRunning autorouter: {router} --autoroute {DSN}\n")
        log.flush()
        try:
            routed = subprocess.run(
                [router, "--autoroute", str(DSN)],
                cwd=OUT,
                text=True,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=1200,
                check=False,
            )
        except subprocess.TimeoutExpired:
            raise SystemExit(f"FreeRouting exceeded 20 minutes. See {LOG}")
        log.write(f"\nFreeRouting exit code: {routed.returncode}\n")
        log.flush()

    candidates = [SES, DSN.with_suffix(".ses")]
    candidates.extend(sorted(OUT.glob("*.ses")))
    session = next((p for p in candidates if p.is_file() and p.stat().st_size > 0), None)
    if routed.returncode != 0:
        raise SystemExit(f"FreeRouting failed with exit code {routed.returncode}. See {LOG}")
    if session is None:
        raise SystemExit(f"FreeRouting created no non-empty SES session. See {LOG}")

    try:
        import pcbnew
    except Exception as exc:
        raise SystemExit(f"Cannot import KiCad pcbnew bindings for SES import: {exc}")

    board = pcbnew.LoadBoard(str(PCB))
    if board is None:
        raise SystemExit(f"KiCad could not load generated board: {PCB}")
    imported = pcbnew.ImportSpecctraSES(board, str(session))
    if not imported:
        raise SystemExit(f"KiCad failed to import FreeRouting session: {session}")
    pcbnew.SaveBoard(str(PCB), board)

    copper_items = list(board.GetTracks())
    if not copper_items:
        raise SystemExit("FreeRouting session imported but produced no PCB tracks or vias.")

    # Replace the generator's now-stale placement-only note while preserving the
    # unconditional NOT FOR FABRICATION warning.
    text = PCB.read_text(encoding="utf-8")
    text = text.replace(
        "NO COPPER ROUTING - CONNECTIVITY WARNINGS EXPECTED",
        "AUTOROUTED DRAFT - REVIEW DRC AND CONNECTIVITY",
    )
    PCB.write_text(text, encoding="utf-8")

    report = {
        "status": "AUTOROUTED PRELIMINARY DRAFT",
        "manufacturing_status": "NOT FOR FABRICATION",
        "router": Path(router).name,
        "specctra_input": str(DSN.relative_to(ROOT)),
        "session_file": str(session.relative_to(ROOT)),
        "imported_copper_items": len(copper_items),
        "limitations": [
            "KiCad DRC and unconnected-item checks are required after import.",
            "An autorouter result does not prove schematic-to-board netlist parity.",
            "Component footprints and transistor pinouts remain TBC.",
            "The board is a preliminary prototype and is not released for fabrication.",
        ],
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"FreeRouting session imported. Copper tracks/vias: {len(copper_items)}.")
    print(f"Report: {REPORT}")
    print("STATUS: AUTOROUTED PRELIMINARY DRAFT. KiCad DRC and connectivity checks still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
