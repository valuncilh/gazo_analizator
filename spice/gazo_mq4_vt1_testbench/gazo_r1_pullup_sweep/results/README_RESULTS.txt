R1 pull-up sweep completed.
Open each r1_sweep_beta_*.log. For OC RELEASED, RESET should be compared with the TI NE555 RESET voltage-level limits (min 0.3V, typ 0.7V, max 1.0V at the published test conditions). For OC LOW, ipu_low is the external pull-up current that the sensor output would need to sink in this simplified model.
This is a sensitivity study only. It does not identify the actual Joy-IT DOUT output topology, polarity, permissible sink current, or the real KT3102B beta.
Do not change the circuit based on this sweep alone.
