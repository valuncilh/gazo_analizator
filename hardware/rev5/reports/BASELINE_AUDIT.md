# Rev5 baseline audit

## Source files and immutable baseline

- Routed candidate PCB: `gazo_e3_E3_DRC2_repaired.kicad_pcb`
  - SHA-256: `7d23d409f29a3627a06ecf123a1a57aed42e19d11c28d353dcdcfeff2c70a246`
  - 23 footprints, 207 track segments, **21 physical vias**, 5 copper zones.
  - Board outline: X=168.5…227.5 mm, Y=123.5…168.5 mm. Size 59×45 mm.
  - Four M2 NPTH Ø2.2 mm at (172,127.5), (224,127.5), (172,164.5), (224,164.5) mm.
  - Pattern 52×37 mm.
  - A1 (173,140), rotation −90°. XS1 (173,151.21), rotation −90°.
- Placement reference PCB: `gazo_e3_implementation(8).kicad_pcb`, 23 footprints, same outline and hole centers, no route segments/zones.
- Uploaded schematic candidate: `gazo_e3_implementation(2).kicad_sch`.
- Previous board STEP: `gazo_e3_implementation.step`.
- All input artifacts stored unchanged in the OneDrive baseline archive.

## Physical via-count audit

A direct count of top-level physical `(via ...)` blocks in the routed PCB file gives **21 vias**. The earlier Stage03 script used a broad prefix token `(via` and incorrectly included four `(vias not_allowed)` design-rule settings. These are not physical vias. The corrected parser requires the exact top-level via-block token.

## Existing DRC report

The DRC2 static repair report explicitly states native KiCad DRC was not rerun after static repair and zones were not refilled in KiCad. It is therefore a routed candidate baseline, not a native DRC-PASS release board.

## Stage03 / Stage03R1 PCB candidate

- File: `gazo_e3_rev5_usb_c_placement.kicad_pcb`.
- SHA-256: `ee73c41b8612b430947aaaffa848d30d5a6a46b0dfcfc78702200968f5eb1537`.
- Size: 255,616 bytes.
- Saved in OneDrive Stage03R1 folder and complete ZIP. Links are in `hardware/rev5/README.md`.
- Static counts: 26 footprints, 946 unique UUIDs, 207 route segments, **21 physical vias**, 5 copper zones.
- No repeated UUIDs or repeated reference designators.
- Existing M2 hole centers and Edge.Cuts geometry preserved.
- USB4105 origin (198.000,127.175), rotation 180°. Footprint PCB-edge datum transformed exactly to Y=123.500 mm.
- R8/R9 5.1 kΩ 0805 at (196.25,134.50) and (199.25,134.50), 90°. Pad1 Earth, pad2 CC2/CC1 respectively.
- New pad to pre-existing track minimum edge gap: 0.3169 mm.
- Minimum candidate courtyard clearance: 0.885 mm.
- Courtyard collision pairs below 0.25 mm: zero.
- Existing track intersections with the USB courtyard: zero.
- Static report files and source generator are included in Stage03R1 package.

## Important limitations

- XS1 remains in the candidate PCB as a temporary legacy power input while the new input circuit is being integrated. It must not be removed before USB-C power route completion.
- The schematic has not yet been updated to match the new J1/R8/R9 pads.
- The VBUS path is assigned to /VCC but there is no new copper route or measured current/protection selection yet.
- KiCad CLI is not installed in the work environment. Native KiCad ERC/DRC and zone refill were not run.
- No new PCB STEP or FreeCAD enclosure has been created at this point.
