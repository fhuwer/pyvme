from time import sleep
from enum import Enum
from ..vme import VMEModule


class V895(VMEModule):
    NUM_CHANNELS = 16

    def __init__(self, controller, address):
        super().__init__(controller, address)

    def set_threshold(self, channel, value):
        print(f"Set {0x02 * channel:x} to {value}")
        if not 0 <= channel < 16:
            raise ValueError("Channel needs to be between 0 and 15")
        if not 1 <= value <= 255:
            raise ValueError("Threshold out of range, allowed 1 to 255 (in mV)")
        self.write(0x02 * channel, value)
        print(f"Set {0x02 * channel:x} to {value}")

    def set_inhibit_pattern(self, pattern):
        if not 0 <= pattern < 1 << 17:
            raise ValueError("Pattern out of range, allowed are only 16 bit.")
        self.write(0x4A, pattern)

    def set_output_width(self, range_, value):
        """
        Set output width

        Args:
            range_ (int): Range - can be 0 (for channels 0-7) or 1 (for channels 8-15)
            value (int): Time 0-255 corresponds to 5ns-40ns (non-linear)
        """
        if not 0 <= value <= 255:
            raise ValueError("Output width out of range, allowed 0-255 (5ns-40ns)")
        if range_ == 0:
            self.write(0x40, value)
        elif range_ == 1:
            self.write(0x42, value)
        else:
            raise ValueError("Channel range needs to be 0 or 1")

    def set_majority_threshold(self, threshold):
        if not 0 <= threshold <= 20:
            raise ValueError("Threshold out of range, allowed 0-20")
        self.write(0x48, int((threshold * 50 - 25) / 4))

    @property
    def model(self):
        return self.read_string(0xFC, 0xFC)

    @property
    def serial_number(self):
        return self.read(0xFE)
