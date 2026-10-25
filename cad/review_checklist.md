# CAD review checklist — iteration 0.1

- [x] Add native preliminary KiCad PCB file generator and source.
- [x] Add custom in-file footprints for provisional components and connectors.
- [x] Add a static checker and preliminary BOM/placement reports.
- [x] Add a parameter-driven FreeCAD enclosure script and STEP/STL/FCStd output rules.
- [x] Add explicit PRELIMINARY / NOT FOR FABRICATION warnings.
- [ ] Create a native KiCad schematic and verify pin mapping through ERC/netlist.
- [ ] Confirm exact KT3102GM variant, package drawing, and C-B-E ordering.
- [ ] Select physical potentiometer P1, switch SA1, power connector XS1.
- [ ] Replace every TBC footprint with manufacturer dimensions.
- [ ] Verify actual A1 module fit, MQ-4 sensor-can height, gas access and thermal clearance.
- [ ] Verify sounder aperture and LED light-pipe fit.
- [ ] Complete copper routing and resolve DRC issues.
- [ ] Generate Gerber/drill and assembly documentation only after design-review gate.

The current PCB is intentionally unrouted. Its DRC report is diagnostic only. No manufacture release is implied.
