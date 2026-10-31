# Original 2022 KiCad verification

**Status:** preliminary electrical transcription with an improved readable layout. The report checks document structure, ERC and exported connectivity; it does not establish physical pinout, electrical operation, safety, or visual identity with the printed article.

## Environment and commands

- KiCad CLI: **10.0.7**.
- Reviewed the exported SVG at full-sheet view and a detail crop around DA1 and its timing parts.
- ERC: `kicad-cli sch erc --severity-all --format json -o <report>.json cad/original_2022/original_2022.kicad_sch`; retained text report: `kicad-cli sch erc --severity-all -o cad/original_2022/reports/original_2022_erc.rpt cad/original_2022/original_2022.kicad_sch`.
- Netlist: `kicad-cli sch export netlist --format kicadxml -o cad/original_2022/reports/original_2022.net cad/original_2022/original_2022.kicad_sch`.
- BOM: `kicad-cli sch export bom -o cad/original_2022/reports/original_2022_bom.csv cad/original_2022/original_2022.kicad_sch`.
- Full inventory/net review: `python3 -B cad/original_2022/verify_netlist.py cad/original_2022/reports/original_2022.net`.
- Format check: `git diff --check`.

## ERC result and rule coverage

The `.kicad_pro` now explicitly enables the four categories previously reported under `ignored_checks`: `single_global_label` (warning), `four_way_junction` (warning), `simulation_model_issue` (error), and `footprint_filter` (warning). The report JSON now has **`ignored_checks: []`** and the project declares **no individual ERC exclusions** (`erc_exclusions: []`). KiCad 10.0.7 ERC returned **0 errors and 17 warnings**. All 17 warnings are `footprint_filter`: this Original transcription intentionally has no assigned footprints or PCB. No single-global-label, four-way-junction, or SPICE-model violations remain. An earlier run exposed one four-way-junction warning caused by a redundant zero-length wire where R4.2 and R5.1 already shared one grid point; the zero-length segment was removed without changing the net, and the warning disappeared.

Thus the enabled ERC categories produced no electrical-rule errors, but the result is not “zero violations”; the 17 footprint warnings remain open because physical footprints are unknown. KiCad documents distinguish ignored rule categories from individual exclusions; source S69 records the official manual and CLI reference.

## Netlist, component and pin audit

- BOM and KiCad component inventory: **19 references**.
- The reference now includes both a net-membership table and an explicit component/pin inventory. The checker compares each exported net as a complete set, all component references, and every numbered pin in each component. Each declared pin must occur exactly once in a connected net or in the NC set.
- Result: **PASS** — 13 connected nets, 46 connected pins, 19 components, 47 total component pins accounted for; the sole no-connect is A1.3. The checker also fails if a component or a declared component pin is removed from the exported inventory.
- Connected nets: `/GND`, `/VCC`, `Net-(A1-Pin_2)`, `Net-(DA1-CONT)`, `Net-(DA1-DISCH)`, `Net-(DA1-OUT)`, `Net-(DA1-THRES)`, `Net-(DA1-~{RST})`, `Net-(HA1-Pin_1)`, `Net-(HA1-Pin_2)`, `Net-(HL1-A)`, `Net-(HL2-K)`, and `Net-(VT1-B)`.

## Visual review and limits

DA1, C2, R4/R5, C1 and C3 fields were repositioned to separate designators/values from pin names and wire paths. The displayed netlist, reference table and Original values remain unchanged. The SVG is a readable connectivity drawing, not a facsimile of the article or a released E3 sheet; final title-block and ESKD formatting remain future work.

A1.1=VCC, A1.2=DOUT, A1.3=AOUT/NC, and A1.4=GND are conditional **KiCad connector-symbol pin numbers only**. They do not establish the physical pin order of the unidentified module. `PWR_FLAG` symbols support ERC and are not physical BOM components. No footprints, board, exact A1 module, physical behavior, or gas calibration are verified.

## Retained outputs

[ERC report](original_2022_erc.rpt), [XML netlist](original_2022.net), [BOM](original_2022_bom.csv), [SVG](../exports/original_2022.svg), and [PNG preview](../exports/original_2022_preview.png).
