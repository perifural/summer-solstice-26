import serial
from dataclasses import dataclass


PORT = "COM7"
BAUDRATE = 19200


FUNCTION_MAP = {
    0x3B: "V",
    0x3D: "uA",
    0x3F: "mA",
    0x39: "A",
    0x33: "Ω",
    0x35: "continuity",
    0x31: "diode",
    0x32: "Hz",
    0x36: "capacitance",
    0x34: "temperature",
}


# key: function name, range_code after removing high bit
# value: decimal places, unit text
RANGE_MAP = {
    "V": {
        0x34: (2, "mV"),     # 220.00mV
        0x30: (4, "V"),      # 2.2000V
        0x31: (3, "V"),      # 22.000V
        0x32: (2, "V"),      # 220.00V
        0x33: (1, "V"),      # 1000.0V
    },
    "Ω": {
        0x30: (2, "Ω"),      # 220.00Ω
        0x31: (4, "kΩ"),     # 2.2000kΩ
        0x32: (3, "kΩ"),     # 22.000kΩ
        0x33: (2, "kΩ"),     # 220.00kΩ
        0x34: (4, "MΩ"),     # 2.2000MΩ
        0x35: (3, "MΩ"),     # 22.000MΩ
        0x36: (1, "MΩ"),     # 220.0MΩ
    },
    "capacitance": {
        0x30: (3, "nF"),     # 22.000nF
        0x31: (2, "nF"),     # 220.00nF
        0x32: (4, "uF"),     # 2.2000uF
        0x33: (3, "uF"),     # 22.000uF
        0x34: (2, "uF"),     # 220.00uF
        0x35: (4, "mF"),     # 2.2000mF
        0x36: (0, "mF"),     # 22mF
        0x37: (0, "mF"),     # 220mF
    },
    "Hz": {
        0x30: (2, "Hz"),     # 22.00Hz
        0x31: (1, "Hz"),     # 220.0Hz
        0x33: (2, "kHz"),    # 220.00kHz
        0x34: (4, "MHz"),    # 2.2000MHz
        0x35: (3, "MHz"),    # 22.000MHz
        0x36: (2, "MHz"),    # 50.00MHz
        0x37: (0, ">50MHz"),
    },
}


@dataclass
class MeterReading:
    raw_hex: str
    function: str
    value: str
    unit: str
    mode: str
    auto: bool
    hold: bool
    low_battery: bool
    ol: bool
    rel: bool
    min_: bool
    max_: bool


def low7(byte: int) -> int:
    """
    Protocol often uses bytes like B0-B9 instead of 30-39.
    Removing the high bit converts:
    B0 -> 30
    B3 -> 33
    BA -> 3A
    8A -> 0A
    """
    return byte & 0x7F


def nibble(byte: int) -> int:
    """
    Status bytes are encoded with high bit sometimes set.
    BA means 0x0A logically.
    B3 means 0x03 logically.
    """
    return byte & 0x0F


def parse_digits(frame: bytes) -> str:
    # Byte 2-6 are data digits: data4, data3, data2, data1, data0
    digits = []
    for b in frame[1:6]:
        d = low7(b) - 0x30
        if 0 <= d <= 9:
            digits.append(str(d))
        else:
            digits.append("?")
    return "".join(digits)


def insert_decimal(digits: str, decimals: int) -> str:
    if "?" in digits:
        return digits

    if decimals <= 0:
        return str(int(digits))

    integer_part = digits[:-decimals]
    decimal_part = digits[-decimals:]

    if not integer_part:
        integer_part = "0"

    return f"{int(integer_part)}.{decimal_part}"


def parse_frame(frame: bytes) -> MeterReading:
    if len(frame) != 14:
        raise ValueError(f"Invalid frame length: {len(frame)}")

    if frame[12] != 0x0D or frame[13] != 0x8A:
        raise ValueError(f"Invalid frame ending: {frame[12]:02X} {frame[13]:02X}")

    raw_hex = frame.hex(" ").upper()

    range_code = low7(frame[0])
    func_code = low7(frame[6])
    function = FUNCTION_MAP.get(func_code, f"unknown_0x{frame[6]:02X}")

    status_8 = nibble(frame[7])
    status_9 = nibble(frame[8])
    status_10 = nibble(frame[9])
    status_11 = nibble(frame[10])
    status_12 = nibble(frame[11])

    ol = bool(status_8 & 0x1)
    low_battery = bool(status_8 & 0x2)
    negative = bool(status_8 & 0x4)

    rel = bool(status_9 & 0x2)
    min_ = bool(status_9 & 0x4)
    max_ = bool(status_9 & 0x8)

    duty = bool(status_10 & 0x8)

    dc = bool(status_11 & 0x8)
    ac = bool(status_11 & 0x4)
    auto = bool(status_11 & 0x2)
    freq_duty_mode = bool(status_11 & 0x1)

    hold = bool(status_12 & 0x8)

    if dc:
        mode = "DC"
    elif ac:
        mode = "AC"
    elif freq_duty_mode:
        mode = "DUTY" if duty else "FREQ"
    else:
        mode = ""

    if ol:
        value_text = "OL"
        unit = RANGE_MAP.get(function, {}).get(range_code, (0, ""))[1]
    else:
        digits = parse_digits(frame)

        decimals, unit = RANGE_MAP.get(function, {}).get(range_code, (0, ""))
        value_text = insert_decimal(digits, decimals)

        if negative and value_text != "OL":
            value_text = "-" + value_text

    return MeterReading(
        raw_hex=raw_hex,
        function=function,
        value=value_text,
        unit=unit,
        mode=mode,
        auto=auto,
        hold=hold,
        low_battery=low_battery,
        ol=ol,
        rel=rel,
        min_=min_,
        max_=max_,
    )


def read_frames(port: str = PORT):
    ser = serial.Serial(
        port=port,
        baudrate=BAUDRATE,
        bytesize=8,
        parity="N",
        stopbits=1,
        timeout=1,
    )

    buffer = bytearray()

    print(f"Reading {port} at {BAUDRATE} 8N1...")
    print("Press Ctrl+C to stop.\n")

    while True:
        data = ser.read(64)

        if not data:
            continue

        buffer.extend(data)

        # Frame ending from document: 0D 8A
        while b"\x0D\x8A" in buffer:
            before, sep, after = buffer.partition(b"\x0D\x8A")
            frame = before + sep
            buffer = after

            # Protocol frame should be exactly 14 bytes.
            # If extra bytes appear before frame, keep the last 14.
            if len(frame) > 14:
                frame = frame[-14:]

            if len(frame) != 14:
                print("Partial/invalid frame:", frame.hex(" ").upper())
                continue

            try:
                reading = parse_frame(frame)

                flags = []
                if reading.auto:
                    flags.append("AUTO")
                if reading.hold:
                    flags.append("HOLD")
                if reading.low_battery:
                    flags.append("BATT")
                if reading.rel:
                    flags.append("REL")
                if reading.min_:
                    flags.append("MIN")
                if reading.max_:
                    flags.append("MAX")

                flag_text = " ".join(flags)

                print(
                    f"{reading.mode} {reading.function}: "
                    f"{reading.value} {reading.unit} "
                    f"{flag_text}"
                )
                print(f"RAW: {reading.raw_hex}")
                print()

            except Exception as e:
                print("Parse error:", e)
                print("RAW:", frame.hex(" ").upper())
                print()


if __name__ == "__main__":
    read_frames()
