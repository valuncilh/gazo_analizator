# Source-derived facts and modelling assumptions

## Confirmed from the Joy-IT SEN-MQ4-V2 datasheet
- 5 V DC supply.
- AOUT range 0–5 V.
- DOUT logic levels specified as 0 V / 5 V, adjustable threshold.
- Typical measurement range approximately 300–10,000 ppm.
- The sensor board includes a heater and onboard comparator.
- The sensor requires 10–15 min warm-up after power-up and 48–168 h initial burn-in.
- Page 3 gives the sensor divider equation and RL=1500 ohm.

## Not specified by the Joy-IT V2 datasheet
- DOUT polarity at alarm.
- Whether DOUT is push-pull, open-collector/open-drain, or another topology.
- Internal DOUT pull-up value or allowed sink/source current.
- Heater current and total module current.
- A calibrated R0 for this specific board.

## Confirmed from the project schematic/netlist
- A1.2 is DOUT.
- R1=160k from VCC to DOUT.
- R2=13k from DOUT to VT1 base.
- VT1 emitter is GND and collector is NE555 RESET.
- R3=2k from VCC to RESET.

## Model assumptions
- Push-pull source resistance 50 ohm.
- Open-collector ON state represented by 10 ohm to GND.
- Open-collector released state has no internal pull-up; only external R1=160k is used.
- KT3102B represented by a simple Gummel-Poon NPN model with BF=50/200/500. Only BF range is anchored to reference data; remaining model parameters are approximate.
- Analog MQ-4 ratio deck uses R0 from an MQSensorsLib example, not a measured SEN-MQ4-V2 sensor. It is a transfer illustration only.
