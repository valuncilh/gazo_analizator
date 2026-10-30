# Original 2022 KiCad verification

**Status:** preliminary electrical transcription. This report checks the KiCad document and its exported connectivity; it does not establish physical pinout, behavior, safety, or graphical identity with the printed article.

## Environment and commands

- KiCad CLI: **10.0.7**.
- The schematic was opened in Eeschema and also rendered to SVG for visual inspection.
- ERC command: `kicad-cli sch erc --severity-all -o cad/original_2022/reports/original_2022_erc.rpt cad/original_2022/original_2022.kicad_sch`.
- Netlist command: `kicad-cli sch export netlist --format kicadxml -o cad/original_2022/reports/original_2022.net cad/original_2022/original_2022.kicad_sch`.
- BOM command: `kicad-cli sch export bom -o cad/original_2022/reports/original_2022_bom.csv cad/original_2022/original_2022.kicad_sch`.
- Full connectivity check: `python3 cad/original_2022/verify_netlist.py cad/original_2022/reports/original_2022.net`.
- Repository whitespace check: `git diff --check`.

## Results

- ERC at `2026-10-31T02:50:10`: **0 errors, 0 warnings, 0 violations**. The report listed ignored-check categories: “Global label only appears once in the schematic”, “Four connection points are joined together”, “SPICE model issue”, and “Assigned footprint doesn't match footprint filters”. No ERC messages were emitted.
- BOM: **19 components**.
- Automated full-netlist comparison: **PASS**. All **13 connected nets / 46 connected symbol pins** match the contact sets in [`data/original_scheme_reference.md`](../../../data/original_scheme_reference.md). The single no-connect is **A1.3**. The checker compares complete pin membership sets, not KiCad's generated names for unnamed nets.
- Connected nets in the XML export: `/GND`, `/VCC`, `Net-(A1-Pin_2)`, `Net-(DA1-CONT)`, `Net-(DA1-DISCH)`, `Net-(DA1-OUT)`, `Net-(DA1-THRES)`, `Net-(DA1-~{RST})`, `Net-(HA1-Pin_1)`, `Net-(HA1-Pin_2)`, `Net-(HL1-A)`, `Net-(HL2-K)`, and `Net-(VT1-B)`.
- Exports: [ERC report](original_2022_erc.rpt), [XML netlist](original_2022.net), [BOM](original_2022_bom.csv), and [SVG preview](../exports/original_2022.svg).
- KiCad's SVG export contains trailing spaces; they were stripped from the retained SVG. Raster comparison against the saved PNG preview produced **0 differing pixels**. Final `git diff --check` passes.

## Scope and remaining work

In the KiCad connector symbol only, A1.1=VCC, A1.2=DOUT, A1.3=AOUT/NC, and A1.4=GND. These are **conditional KiCad symbol pin numbers**; no physical pin order for the unidentified MQ-4 module has been established. The `PWR_FLAG` symbols support ERC but are not component pins in the exported netlist.

The SVG shows a connected transcription and is not a graphical facsimile of the article. Spacing, grouping, and title block still need graphic refinement before the drawing can be treated as a finished E3 document. ERC and netlist checks do not establish electrical operation. No footprints, PCB, or physical A1 module are verified in this Original 2022 project.
