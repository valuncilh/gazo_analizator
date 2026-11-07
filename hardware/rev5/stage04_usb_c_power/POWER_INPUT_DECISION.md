# USB-C 5 V input — assumptions and open decisions

## Current candidate

- Connector: GCT USB4105 Type-C receptacle.
- Role: sink / power input.
- VBUS: nominal 5 V to /VCC.
- CC1: Rd 5.1 kΩ to Earth.
- CC2: Rd 5.1 kΩ to Earth.
- D+, D−, SBU1, SBU2: NC.
- USB Power Delivery: not implemented.

A Type-C sink presents Rd on both CC contacts. Passive Rd resistors do not decode source current advertisement. Do not assume 1.5 A or 3 A availability without appropriate CC current detection/control.

## Load current

Joy-IT SEN-MQ4-V2 product documentation specifies 5 V and an integrated heater, but does not state the module's total current. The older SEN-MQ4 product page provides a heater-current figure up to 180 mA, but it is not the V2 product revision and must not be used as a verified V2 rating.

## Open decisions

- Maximum whole-device current during heater warm-up and steady state.
- Minimum supported USB source class.
- Need and ratings for fuse/PTC, TVS and reverse-current protection.
- Whether USB-C remains power-only or later needs data/service functionality.

Protection selection is intentionally deferred until the load current and power-source assumptions are confirmed.
