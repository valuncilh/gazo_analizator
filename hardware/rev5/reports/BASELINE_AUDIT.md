# Rev5 baseline audit

## Git status

- The repository exposes `analysis/vendor-behavioral-reconciliation` as the only pre-existing branch.
- A branch named `main` was not found via the GitHub branches endpoint. The repository default branch at audit time is `analysis/vendor-behavioral-reconciliation`.
- Rev5 branches from confirmed commit `4451222a416302e97e1f25da4e60df7309f7445f`. No change is made to the pre-existing engineering branch.
- All Rev5 changes are made on `design/usb-c-pcb-enclosure-r5`.

## Candidate PCB sources

### Routed source: `gazo_e3_E3_DRC2_repaired.kicad_pcb`

- SHA-256: `7d23d409f29a3627a06ecf123a1a57aed42e19d11c28d353dcdcfeff2c70a246`
- 23 footprints.
- 207 track segments.
- 21 vias.
- 5 copper zones.
- Four M2 NPTH holes:
  - MH1: (172.0, 127.5) mm.
  - MH2: (224.0, 127.5) mm.
  - MH3: (172.0, 164.5) mm.
  - MH4: (224.0, 164.5) mm.
- Exact Edge.Cuts rectangle: X=168.5…227.5 mm, Y=123.5…168.5 mm. Board size 59 × 45 mm.
- Thickness: 1.6 mm.
- Hole pattern: 52 × 37 mm.
- A1 at (173.0, 140.0), rotation −90°.
- XS1 at (173.0, 151.21), rotation −90°. This is the existing two-pin power input to remove only in the new Rev5 working copy.

The supplied repair report expressly states that native KiCad DRC was not rerun after the static repairs and copper zones were not refilled through KiCad. This board is the best available routed baseline, not a release-ready DRC-PASS board.

### Placement reference: `gazo_e3_implementation(8).kicad_pcb`

- SHA-256: `f9cd9797df03fe79267c0c57c1f98b4729e2b27080316102dd9fbbdb9b510e9d`
- 23 footprints.
- Same 59 × 45 mm outline and four-hole M2 pattern.
- No route segments, vias, or copper zones. This is a separate placement/geometry reference, not the routed PCB master.

### Uploaded schematic: `gazo_e3_implementation(2).kicad_sch`

- SHA-256: `8a5692d8905c121bc0479f06e7b1fb313fd8552371b7fd6947fa3fe9f0fd419c`
- This is an uploaded schematic candidate. Its net mapping must be reconciled with the routed PCB and the new USB-C input before any final board is exported.

### Existing board STEP: `gazo_e3_implementation.step`

- SHA-256: `39dc2804ae8935089836de67985e934e5d6b87f58e14bf12953b3a5c311c7087`
- Preserved byte-for-byte as the old board mechanical reference. Do not overwrite it with a Rev5 export.

## DRC2 repair provenance

The original DRC report `DRC(2).rpt` recorded 20 violations, including solder-mask bridge/shorting errors at A1 and XS1, silkscreen conflicts, two unconnected pads, one dangling track, and library warnings.

The supplied repair report states that:
- the A1 and XS1 local footprint pad geometry was corrected
- A1.4 and R7.1 connections were restored using two added transitions
- dangling track and 90-degree turns were addressed
- no duplicate UUIDs or static different-net copper intersections were detected
- calculated minimum clearance between different nets was 0.2243 mm

However, native KiCad DRC after those static changes was not run, and zones were not refilled. The board is therefore not marked DRC PASS.

## USB-C candidate

Selected candidate: GCT USB4105, top-mount, horizontal, 16-pin. Manufacturer drawing: https://gct.co/files/drawings/usb4105.pdf

The manufacturer drawing/official KiCad footprint must be treated as the mechanical source for pad coordinates, shell stake slots, PCB edge datum, and connector body. Do not substitute approximate hand-drawn geometry.

## Preservation

All input sources and R3 reference packages are preserved in the immutable OneDrive snapshot. SHA-256 values are in the archive manifest. The source-preservation policy is mandatory for later revisions.

## Validation environment

- `kicad-cli`: not installed in the current preparation environment.
- `FreeCAD` / `FreeCADCmd`: not installed.
- CadQuery and OpenCascade Python bindings are available for supplemental STEP/solid checks.
- No native KiCad ERC/DRC or FreeCAD recompute is claimed at this stage.

## Next steps

1. Audit the routed board's `/VCC` and `Earth` nets, the complete XS1 pin/pad/tracks/vias/zone topology, and the schematic symbol/pin-to-net mapping.
2. Confirm GCT USB4105 recommended land pattern, footprint orientation, pin map, shield slots, board-edge alignment, and 3D body envelope.
3. Update the schematic first with USB-C sink-only wiring and the required input protection. Keep the original schematic unchanged.
4. Create a new Rev5 PCB placement file from the routed baseline. Remove XS1 only from the new copy. Preserve unrelated circuitry and exact M2 datums.
5. Route and refill zones, then run native KiCad ERC/DRC in a KiCad environment and retain the reports.
6. Export a new versioned PCB STEP only after the PCB passes the release checks.
7. Build and recompute the Rev5 FreeCAD enclosure around that exact STEP. Preserve the full-size one-piece lid with four corner fasteners and keep walls uncut except intentional openings.
8. Package versioned outputs and their test reports. Do not delete or overwrite any preceding revision.
