from time import sleep
from enum import Enum
from ..vme import VMEModule


class V6533BoardStatus(Enum):
    CHANNEL_0_ALARM = 0
    CHANNEL_1_ALARM = 1
    CHANNEL_2_ALARM = 2
    CHANNEL_3_ALARM = 3
    CHANNEL_4_ALARM = 4
    CHANNEL_5_ALARM = 5
    BOARD_POWER_FAIL = 8
    BOARD_OVER_POWER = 9
    BOARD_MAX_VOLTAGE_UNCALIBRATED = 10
    BOARD_MAX_CURRENT_UNCALIBRATED = 11


class V6533ChannelStatus(Enum):
    ON = 0
    RAMP_UP = 1
    RAMP_DOWN = 2
    OVER_CURRENT = 3
    OVER_VOLTAGE = 4
    UNDER_VOLTAGE = 5
    MAXV = 6
    MAXI = 7
    TRIP = 8
    OVER_POWER = 9
    OVER_TEMPERATURE = 10
    DISABLED = 11
    INTERLOCK = 12
    UNCALIBRATED = 13
    RESERVED = 14


class HVChannel:
    CHANNEL_OFFSET = 0x80

    def __init__(self, module, channel):
        self.module = module
        self.channel = channel

    @property
    def voltage(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0x80) * 0.1

    @voltage.setter
    def voltage(self, voltage):
        self.module.write(
            self.CHANNEL_OFFSET * self.channel + 0x80, int(float(voltage) / 0.1)
        )

    @property
    def measured_voltage(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0x88) * 0.1

    @property
    def current_limit(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0x84) * 0.05

    @current_limit.setter
    def current_limit(self, current):
        self.module.write(
            self.CHANNEL_OFFSET * self.channel + 0x84, int(float(current) / 0.05)
        )

    @property
    def imon_range(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0xB4) == 1

    @imon_range.setter
    def imon_range(self, low_range):
        self.module.write(self.CHANNEL_OFFSET * self.channel + 0xB4, int(low_range))

    @property
    def measured_current(self):
        sleep(0.1)
        if self.imon_range:
            return self.module.read(self.CHANNEL_OFFSET * self.channel + 0xB8) * 0.005
        else:
            return self.module.read(self.CHANNEL_OFFSET * self.channel + 0x8C) * 0.05

    @property
    def enabled(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0x90) == 1

    @enabled.setter
    def enabled(self, value):
        if value:
            return self.module.write(self.CHANNEL_OFFSET * self.channel + 0x90, 1)
        else:
            return self.module.write(self.CHANNEL_OFFSET * self.channel + 0x90, 0)

    @property
    def status(self):
        return V6533ChannelStatus(
            self.module.read(self.CHANNEL_OFFSET * self.channel + 0x94)
        )

    @property
    def trip_time(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0x98) * 0.1

    @trip_time.setter
    def trip_time(self, time):
        self.module.write(self.CHANNEL_OFFSET * self.channel + 0x98, int(time / 0.1))

    @property
    def voltage_limit(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0x9C) * 0.1

    @voltage_limit.setter
    def voltage_limit(self, limit):
        self.module.write(self.CHANNEL_OFFSET * self.channel + 0x9C, int(limit / 0.1))

    @property
    def ramp_down_rate(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0xA0)

    @ramp_down_rate.setter
    def ramp_down_rate(self, rate):
        self.module.write(self.CHANNEL_OFFSET * self.channel + 0xA0, int(rate))

    @property
    def ramp_up_rate(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0xA4)

    @ramp_up_rate.setter
    def ramp_up_rate(self, rate):
        self.module.write(self.CHANNEL_OFFSET * self.channel + 0xA4, int(rate))

    @property
    def power_down_mode(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0xA8) == 1

    @power_down_mode.setter
    def power_down_mode(self, use_ramp):
        self.module.write(self.CHANNEL_OFFSET * self.channel + 0xA8, use_ramp)

    @property
    def polarity(self):
        return 1 if self.module.read(self.CHANNEL_OFFSET * self.channel + 0xAC) else -1

    @property
    def temperature(self):
        return self.module.read(self.CHANNEL_OFFSET * self.channel + 0xB0)

    def power_on(self):
        self.enabled = True

    def power_off(self):
        self.enabled = False


class V6533(VMEModule):
    NUM_CHANNELS = 6

    def __init__(self, controller, address):
        super().__init__(controller, address)
        self.channels = [HVChannel(self, i) for i in range(self.NUM_CHANNELS)]

    @property
    def max_voltage(self):
        return float(self.read(0x0050))

    @property
    def max_current(self):
        return self.read(0x0054)

    @property
    def status(self):
        print(self.read(0x0058))
        return V6533BoardStatus(self.read(0x0058))

    @property
    def firmware_release(self):
        release = self.read(0x005C)
        return (release >> 8, release & 0xFF)

    @property
    def num_channels(self):
        return self.read(0x8100)

    @property
    def description(self):
        return self.read_string(0x8102, 0x8114)

    @property
    def model(self):
        return self.read_string(0x8116, 0x811C)

    @property
    def serial_number(self):
        return self.read(0x811E)

    @property
    def fpga_firmware_release(self):
        release = self.read(0x8120)
        return (release >> 8, release & 0xFF)
