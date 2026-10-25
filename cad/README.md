# CAD: preliminary placement and enclosure

Date: 25.10.2026. Status: **PRELIMINARY / NOT FOR FABRICATION**.

## Iteration 0.1

- Native KiCad PCB placement draft: 72 x 50 x 1.6 mm, net assignments and custom in-file footprints.
- No copper routing is present. DRC unconnected-net warnings are expected and are not a pass for manufacturing.
- Control board is placed beside a separate 25.4 x 25.4 mm Amperka AMP-B052 module.
- A parametric FreeCAD case concept is provided at 120 x 78 x 42 mm. It includes a removable lid, standoffs, module rails, MQ-4 vent grid, HCM1205X aperture, LED holes and a provisional power connector cutout.
- The selected JL World HCM1205X dimensions come from passport 0105-86 Rev. A2: body OD 12 mm, height about 9.5 mm, lead pitch 7.6 mm. The MQ-4 sensor can profile is still a TBC envelope.

## Critical TBC items

1. KT3102GM manufacturer-specific pinout, package drawing and saturation at the required collector current.
2. The physical P1 trim potentiometer, SA1 DPDT switch and XS1 power connector.
3. Exact resistor, capacitor, LED and diode footprints.
4. KiCad schematic, ERC, netlist parity, PCB routing and DRC closure.
5. Actual A1 mounting method, MQ-4 sensor height, ventilation and heat clearances.
6. Acoustic clearance and lid light-pipe fit.
7. Formal mechanical test levels and any required ingress-protection criteria.

## Sources

- Amperka AMP-B052: https://amperka.ru/product/troyka-mq4-gas-sensor and https://wiki.amperka.ru/продукты:mq4.
- JL World HCM1205X, Specification 0105-86 Rev. A2: https://satec.ru/_img/goods_attach/474/00-00135474/134038_0.pdf.
- KR1006VI1, package 2101.8-1: https://radiolub.ru/uploads/2012pic/kr1006vi1.pdf.
- KiCad PCB file format: https://dev-docs.kicad.org/en/file-formats/sexpr-pcb/.
- KiCad CLI: https://docs.kicad.org/9.0/en/cli/cli.html.
- FreeCAD headless usage: https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Headless_FreeCAD.md.

## Next gate

Create a native KiCad schematic and validate its pin mapping before routing. Replace all TBC footprints with exact selected manufacturer footprints, run ERC/DRC, then issue production files only after the thermal/current/case mechanical blockers have been reviewed.
