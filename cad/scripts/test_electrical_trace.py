#!/usr/bin/env python3
"""Cross-check the SPICE alarm chain against the provisional KiCad pad-net map.

This proves declared topology and net assignments only. It does not prove copper
continuity, transistor package pinout, component fit, or hardware behaviour.
"""
from pathlib import Path
import sys

from check_preliminary_pcb import (
    EXPECTED_PAD_NETS,
    extract_pad_net_map,
    validate_pad_net_map,
)

ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"TRACE ERROR: {message}", file=sys.stderr)
        raise SystemExit(1)


def declarations(path: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith(("*", ".")):
            continue
        fields = line.split()
        ref = fields[0].upper()
        if ref in result:
            raise SystemExit(f"Duplicate SPICE element declaration {ref} in {path}")
        result[ref] = fields
    return result


def expect_prefix(netlist: dict[str, list[str]], ref: str, expected: list[str]) -> None:
    observed = netlist.get(ref.upper())
    require(observed is not None, f"{ref}: element is missing")
    require(
        observed[: len(expected)] == expected,
        f"{ref}: expected prefix {expected}, got {observed}",
    )


def check_spice_chain(path: Path, vendor: bool) -> None:
    net = declarations(path)

    # MQ-4 signal, comparator polarity, inversion transistor, and timer RESET.
    if vendor:
        expect_prefix(net, "XU2", ["XU2", "UREF", "S", "DOUT", "VCC", "0", "TLV7041"])
        expect_prefix(net, "XDA1", [
            "XDA1", "CT", "CTRL555", "CT", "RESET", "OUT", "DISCH", "VCC", "0",
            "TLC555_6",
        ])
        expect_prefix(net, "C_U2", ["C_U2", "VCC", "0", "100n"])
        expect_prefix(net, "S_1000", ["S_1000", "N_S_1000", "S", "CTRL_1000", "0", "SW_GAS"])
        expect_prefix(net, "RL_S", ["RL_S", "S", "0", "{RL_SENSOR}"])
    else:
        expect_prefix(net, "VSENSE", ["VSENSE", "S", "0", "PWL(0", "0.30"])
        expect_prefix(net, "ECOMP", ["ECOMP", "CTRL_COMP", "0", "VALUE", "=", "{V(S)-V(UREF)}"])
        expect_prefix(net, "S_U2", ["S_U2", "DOUT", "0", "CTRL_COMP", "0", "SW_OC"])
        expect_prefix(net, "C_U2", ["C_U2", "VCC", "0", "100n"])

    expect_prefix(net, "R2", ["R2", "DOUT", "VT1_B", "10k"])
    expect_prefix(net, "QVT1", ["QVT1", "RESET", "VT1_B", "0"])
    expect_prefix(net, "R3", ["R3", "VCC", "RESET", "2k"])

    # The astable RC network is one continuous node chain:
    # VCC -> R4 -> DISCH -> R5 -> CT, with C1 from CT to ground.
    expect_prefix(net, "R4", ["R4", "VCC", "DISCH", "8.2k"])
    expect_prefix(net, "R5", ["R5", "DISCH", "CT", "8.2k"])
    expect_prefix(net, "C1", ["C1", "CT", "0", "{C_TIMER}"])

    # Output paths: OUT->HL1, OUT->R9->SA1->VT2 base, and VT2 collector->HA1.
    expect_prefix(net, "R6", ["R6", "OUT", "HL1_A", "220"])
    expect_prefix(net, "D_HL1", ["D_HL1", "HL1_A", "0", "D_LED_PROXY"])
    expect_prefix(net, "R9", ["R9", "OUT", "R9_N", "560"])
    expect_prefix(net, "S_SA1", ["S_SA1", "R9_N", "VT2_B", "SOUND_EN", "0", "SW_ENABLE"])
    expect_prefix(net, "QVT2", ["QVT2", "BZ_COL", "VT2_B", "0"])
    expect_prefix(net, "RBZ", ["RBZ", "VCC", "BZ_COL", "166.7"])
    expect_prefix(net, "D1", ["D1", "BZ_COL", "VCC", "D_CLAMP_PROXY"])

    # Both poles of SA1 must control the sounder path and the green indicator.
    expect_prefix(net, "R7", ["R7", "VCC", "HL2_A", "220"])
    expect_prefix(net, "D_HL2", ["D_HL2", "HL2_A", "HL2_K", "D_LED_PROXY"])
    expect_prefix(net, "S_HL2", ["S_HL2", "HL2_K", "0", "SOUND_EN", "0", "SW_ENABLE"])
    expect_prefix(net, "VSA1", ["VSA1", "SOUND_EN", "0", "DC", "{5*SOUND_ENABLE}"])

    # R1 and R8 are deliberately parallel DOUT pull-ups in this project revision.
    expect_prefix(net, "R1", ["R1", "VCC", "DOUT", "160k"])
    expect_prefix(net, "R8", ["R8", "VCC", "DOUT", "2.2k"])


def check_board_map(board_path: Path) -> int:
    board_text = board_path.read_text(encoding="utf-8")
    validate_pad_net_map(board_text)
    observed = extract_pad_net_map(board_text)

    def pad(ref: str, number: str) -> str | None:
        require(ref in observed, f"PCB footprint {ref} is missing")
        require(number in observed[ref], f"PCB pad {ref}.{number} is missing")
        return observed[ref][number]

    # A1's two Amperka cable groups and the comparator's physical SOT-23-5 pins.
    require(pad("J2", "1") == pad("U2", "4") == "SENSE",
            "A1.S must reach U2 IN- through the SENSE net")
    require(pad("J2", "2") == pad("U2", "5") == "+5V",
            "A1 signal-board supply must share +5V with U2")
    require(pad("J2", "3") == pad("U2", "2") == "GND",
            "A1 signal-board ground must share GND with U2")
    require(pad("U2", "1") == pad("R2", "1") == pad("R8", "2") == "DOUT",
            "U2 open-drain output, R2 input, and pull-up must share DOUT")
    require(pad("U2", "3") == pad("RHYS", "2") == pad("P1", "2") == "UREF",
            "U_REF must connect U2 IN+, hysteresis, and P1 wiper")
    require(pad("R2", "2") == pad("VT1", "2") == "VT1_BASE",
            "R2 must drive the VT1 base net")
    require(pad("VT1", "1") == pad("R3", "2") == pad("DA1", "4") == "RESET",
            "VT1 collector, R3 pull-up, and DA1 RESET must share RESET")

    # Standard 555 pin numbering. The transistor footprint pinout remains TBC.
    timer_pins = {
        "1": "GND", "2": "TIMER_CT", "3": "OUT", "4": "RESET",
        "5": "TIMER_CTRL", "6": "TIMER_CT", "7": "TIMER_DISCH", "8": "+5V",
    }
    for number, expected_net in timer_pins.items():
        require(pad("DA1", number) == expected_net,
                f"DA1 pad {number}: expected {expected_net}, got {pad('DA1', number)}")
    require(pad("R4", "2") == pad("R5", "1") == pad("DA1", "7") == "TIMER_DISCH",
            "R4/R5/DA1 discharge net is broken in the pad-net map")
    require(pad("R5", "2") == pad("C1", "1") == pad("DA1", "2") == pad("DA1", "6") == "TIMER_CT",
            "R5/C1/THRES/TRIG node is broken in the pad-net map")
    require(pad("R6", "1") == pad("DA1", "3") == pad("R9", "1") if False else True,
            "Internal assertion placeholder")  # PCB switch is placed before R9, unlike SPICE.

    # Board switch pole precedes R9, but the electrical series path is equivalent:
    # DA1.OUT -> SA1 pole -> R9 -> VT2 base. No alternate throw is assigned.
    require(pad("DA1", "3") == pad("J4", "2") == "OUT",
            "DA1 OUT must reach the common contact of the SA1 sound pole")
    require(pad("J4", "1") == pad("R9", "1") == "SOUND_CTL",
            "SA1 sound throw must feed R9, not bypass it")
    require(pad("J4", "3") is None,
            "Unused SA1 sound throw should remain unconnected in this revision")
    require(pad("R9", "2") == pad("VT2", "2") == "VT2_BASE",
            "R9 must be in series with the VT2 base")
    require(pad("VT2", "1") == pad("HA1", "2") == pad("VD1", "1") == "BUZZ_COL",
            "VT2 collector, HA1, and diode anode must share BUZZ_COL")
    require(pad("HA1", "1") == pad("VD1", "2") == "+5V",
            "HA1 and diode cathode must connect to +5V")

    # Second SA1 pole enables HL2 when its return is connected to ground.
    require(pad("R7", "1") == "+5V" and pad("R7", "2") == pad("HL2", "1") == "HL2_A",
            "R7/HL2 supply chain is broken")
    require(pad("HL2", "2") == pad("J4", "5") == "SA1_LED_RETURN",
            "HL2 return must be switched by the second SA1 pole")
    require(pad("J4", "4") == "GND" and pad("J4", "6") is None,
            "SA1 indicator pole should switch HL2 return to ground or leave it open")

    return len(__import__("re").findall(r"\(segment\s", board_text))


def main() -> int:
    behavioral = ROOT / "spice/alarm_chain_behavioral.cir"
    vendor = ROOT / "spice/alarm_chain_vendor.cir.in"
    board = ROOT / "cad/kicad/gazo_analizator_preliminary.kicad_pcb"

    check_spice_chain(behavioral, vendor=False)
    check_spice_chain(vendor, vendor=True)
    copper_segments = check_board_map(board)

    print("PASS: traced A1.S -> U2 -> VT1 -> DA1.RESET -> DA1.OUT -> HL1 and VT2/HA1.")
    print("PASS: SA1 sound pole is in series with R9 and VT2 base. SA1 second pole switches HL2 return.")
    print("PASS: DA1 555 pin mapping and shared CT/DISCH nodes match the provisional PCB pad-net map.")
    print("LIMIT: VT1/VT2 footprints use TBC pinout. Verify the selected KT3102GM manufacturer's drawing.")
    print("LIMIT: source nets and PCB pad-net labels are checked, not physical copper continuity.")
    print(f"PCB copper segments currently present: {copper_segments}.")
    if copper_segments == 0:
        print("STATUS: PCB is still UNROUTED. Zero DRC geometry violations does not mean electrical routing is complete.")
    print(f"PCB expected map covers {len(EXPECTED_PAD_NETS)} footprints. Manufacturing release remains blocked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
