# Source and deliverable preservation policy — E3 Rev5

## Mandatory rule

**No source artifact is deleted or overwritten because a new revision is being developed.** This applies to KiCad schematics and boards, PCB STEP exports, enclosure STEP/FCStd/STL, FreeCAD macros, footprints, symbols, 3D models, BOMs, hole tables, drawings, reports, and rendered review images.

## Immutable inputs

- Every received baseline is copied into an immutable source snapshot with SHA-256.
- The snapshot is stored outside the working directory and linked from this branch.
- The original filenames and original byte content are retained. A normalized working copy may be created, but must have a new filename and its own checksum.
- Existing R2/R3/R4/R5 deliverables remain available for historical comparison. They are not silently replaced.

## Revision and replacement process

Each substantial stage gets a new versioned output name, for example:
- `gazo_e3_rev5_pcb_placement.kicad_pcb`
- `gazo_e3_rev5_pcb_routed.kicad_pcb`
- `gazo_e3_rev5_pcb.step`
- `gazo_e3_rev5_enclosure.FCStd`
- `gazo_e3_rev5_enclosure.step`
- `gazo_e3_rev5_enclosure_base.stl`
- `gazo_e3_rev5_enclosure_lid.stl`

A prior revision may be marked **superseded** only after the replacement has:
1. Passed native KiCad ERC/DRC where applicable, with the actual reports retained.
2. Passed independent geometry/connectivity checks.
3. Passed PCB STEP-to-FreeCAD import and board/component envelope checks.
4. Passed enclosure interference, connector aperture, screw/hole alignment, and lid-fit checks.
5. Been opened/recomputed in FreeCAD and exported successfully.
6. Been placed in the revision package with BOM, hole schedule, reports, and SHA-256 manifest.

Until then, the previous file remains the authoritative usable baseline. Even after supersession, it remains in Git history and the immutable baseline archive.

## GitHub workflow

- Every substantial stage is committed to `design/usb-c-pcb-enclosure-r5`.
- Commits are scoped to one coherent stage: baseline intake, schematic, PCB placement, PCB routing/DRC, PCB mechanical export, enclosure, release.
- A commit or stage note must contain **Done / Not done / Checks / Next**.
- Never change `main` or the pre-existing engineering branch as a side effect of Rev5.
- Do not call a design "final", "DRC PASS", "manufacturing-ready", or "checked" unless the corresponding native application check has actually been completed and retained.

## Required file ledger

Maintain `hardware/rev5/reports/ARTIFACT_LEDGER.csv` with:
- artifact path and revision
- SHA-256
- source/revision it was derived from
- status (baseline, working, checked, superseded)
- checks performed
- remaining checks
- OneDrive/GitHub location

## Current immutable baseline

The first immutable intake is stored at:

- OneDrive folder: https://1drv.ms/f/c/24fda6920aa8c92a/IgAnVFgpfc9WQK9nWuSqdRp3AbaSeJAc8tlWTGNKwYewT6k
- ZIP: https://1drv.ms/u/c/24fda6920aa8c92a/IQBHREov1F1bSay7DkcBEFrQAWv0sY4f9sOWANQYgvgHAPk

The individual source PCB, schematic, STEP, README, and checksum manifest are in the same folder. Their hashes are listed in `SHA256SUMS.txt`.

**Rule owner:** Rev5 engineering workflow. This policy remains in force for every subsequent turn and revision.
