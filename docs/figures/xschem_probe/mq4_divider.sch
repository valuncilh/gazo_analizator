v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {MQ-4: эквивалентный делитель для сценария чистого воздуха} 40 -260 0 0 0.45 0.45 {}
N 180 -160 420 -160 {lab=VCC}
N 420 -160 420 -130 {lab=VCC}
N 420 -70 420 -30 {lab=S}
N 420 30 420 60 {lab=0}
N 180 -100 100 -100 {lab=0}
N 100 -100 100 60 {lab=0}
N 100 60 420 60 {lab=0}
C {devices/vsource.sym} 180 -130 0 0 {name=VCC value=5}
C {devices/res.sym} 420 -100 0 0 {name=R_S value=88k}
C {devices/res.sym} 420 0 0 0 {name=R_L value=20k}
C {devices/gnd.sym} 420 100 0 0 {name=GND lab=0}
C {devices/code_shown.sym} 700 -80 0 0 {name=SIM only_toplevel=true value=".control\nop\nprint v(S)\n.endc"}
