from ctypes import cdll, c_short, c_int32, c_uint32, c_char, byref, create_string_buffer, string_at
from time import time
from .exceptions import check_error
from ._vmetypes import (
    AddressModifier,
    DataWidth,
    BoardTypes,
    TimeUnits,
    IOSources,
    Polarity,
    Registers,
    Display,
)


try:
    lib_vme = cdll.LoadLibrary("libCAENVME.so")
except OSError:
    pass


def locking(func):
    def inner(self, *args, **kwargs):
        start = time()
        while self._busy:
            if time() - start > 5:
                raise TimeoutError("Thread locked for over 5 seconds.")
        self._busy = True
        try:
            result = func(self, *args, **kwargs)
        except Exception as e:
            self._busy = False
            raise e
        self._busy = False
        return result

    return inner


class VMEController:
    def __init__(self, controller_board_type, link=0, board=0):
        self.handle = c_int32()
        check_error(
            lib_vme.CAENVME_Init(
                controller_board_type.value, link, board, byref(self.handle)
            )
        )
        self._busy = False

    @property
    def busy(self):
        return self._busy

    def __del__(self):
        lib_vme.CAENVME_End(self.handle)

    @locking
    def read(self, address, width=DataWidth.D16):
        data = c_uint32()
        check_error(
            lib_vme.CAENVME_ReadCycle(
                self.handle,
                address,
                byref(data),
                AddressModifier.A24_NON_PRIVILEGED_DATA.value,
                width.value,
            )
        )
        return data.value

    @locking
    def read_string(self, address_start, address_end):
        buffer = []
        for address in range(address_start, address_end + 0x02, 2):
            data = self.read(address)
            buffer.append(chr(data >> 8))
            buffer.append(chr(data & 0xFF))
        return "".join(buffer).strip()

    @locking
    def write(self, address, data, width=DataWidth.D16):
        data_ = c_uint32(data)
        check_error(
            lib_vme.CAENVME_WriteCycle(
                self.handle,
                address,
                byref(data_),
                AddressModifier.A24_NON_PRIVILEGED_DATA.value,
                width.value,
            )
        )


class V2718(VMEController):
    def __init__(self, link=0, board=0):
        super().__init__(BoardTypes.V2718, link, board)

    @property
    def firmware_release(self):
        release = c_char()
        lib_vme.CAENVME_BoardFWRelease(self.handle, byref(release))
        return release

    @locking
    def set_pulser_configuration(
        self, pulser, period, width, unit, num_pulses, start_signal, reset_signal
    ):
        """
        Set the pulser configuration.

        Args:
            pulser (int): Pulser selection (either 0 or 1).
            period (int): Period of the pulse in units of unit parameter.
            width (int): Width of the pulse in units of unit parameter.
            unit (TimeUnits): Unit for the pulser.
            num_pulses (int): Number of pulses (0 means infinite).
            start_signal (IOSources): Signal for the start of the pulser.
            stop_signal (IOSources): Signal for the stop of the pulser.
        """
        if not 0 <= pulser <= 1:
            raise ValueError("Only pulsers 0 or 1 are available")
        check_error(
            lib_vme.CAENVME_SetPulserConf(
                self.handle,
                pulser,
                period,
                width,
                unit.value,
                num_pulses,
                start_signal.value,
                reset_signal.value,
            )
        )

    @locking
    def get_pulser_configuration(self, pulser):
        """
        Get the pulser configuration.

        Returns:
            dict: Dictionary with the configuration parameters.
        """
        if not 0 <= pulser <= 1:
            raise ValueError("Only pulsers 0 or 1 are available")
        period = c_uint32()
        width = c_uint32()
        unit = c_uint32()
        num_pulses = c_uint32()
        start_signal = c_uint32()
        reset_signal = c_uint32()

        check_error(
            lib_vme.CAENVME_GetPulserConf(
                self.handle,
                pulser,
                byref(period),
                byref(width),
                byref(unit),
                byref(num_pulses),
                byref(start_signal),
                byref(reset_signal),
            )
        )
        return dict(
            period=period.value,
            width=width.value,
            unit=TimeUnits(unit.value),
            num_pulses=num_pulses.value,
            start_signal=IOSources(start_signal.value),
            reset_signal=IOSources(reset_signal.value),
        )

    @locking
    def set_scaler_configuration(
        self, limit, auto_reset, source_signal, gate_signal, reset_signal
    ):
        """
        Set the scaler configuration.

        Args:
            limit (int): The counter limit for the scaler.
            auto_reset (bool): Enable/disable the counter auto reset.
            source_signal (IOSources): Source for the counter.
            gate_signal (IOSources): Input for the gate.
            reset_signal (IOSources): Input for the reset.
        """
        check_error(
            lib_vme.CAENVME_SetScalerConf(
                self.handle,
                limit,
                auto_reset,
                source_signal.value,
                gate_signal.value,
                reset_signal.value,
            )
        )

    @locking
    def get_scaler_configuration(self):
        """
        Get the scaler configuration.

        Returns:
            dict: Dictionary with the configuration parameters.
        """
        limit = c_short()
        auto_reset = c_short()
        source_signal = c_uint32()
        gate_signal = c_uint32()
        reset_signal = c_uint32()

        check_error(
            lib_vme.CAENVME_GetScalerConf(
                self.handle,
                byref(limit),
                byref(auto_reset),
                byref(source_signal),
                byref(gate_signal),
                byref(reset_signal),
            )
        )
        return dict(
            limit=limit.value,
            auto_reset=auto_reset.value == 1,
            source_signal=IOSources(source_signal.value),
            gate_signal=IOSources(gate_signal.value),
            reset_signal=IOSources(reset_signal.value),
        )

    @locking
    def set_output_configuration(
        self, output_channel, polarity, led_polarity, source_signal
    ):
        """
        Set the output configuration.

        Args:
            output_channel (int): The output channel to configure (0 - 4).
            polarity (Polarity): Polarity to set to.
            led_polarity (Polarity): LED polarity.
            source (IOSources): The source signal to propagate to the output line.
        """
        if not 0 <= output_channel <= 4:
            raise IndexError("Only channels between 0 and 4 are available.")
        check_error(
            lib_vme.CAENVME_SetOutputConf(
                self.handle,
                output_channel,
                polarity.value,
                led_polarity.value,
                source_signal.value,
            )
        )

    @locking
    def get_output_configuration(self, output_channel):
        """
        Get the output configuration.

        Returns:
            dict: Dictionary with the configuration parameters.
        """
        if not 0 <= output_channel <= 4:
            raise IndexError("Only channels between 0 and 4 are available.")

        polarity = c_uint32()
        led_polarity = c_uint32()
        source_signal = c_uint32()

        check_error(
            lib_vme.CAENVME_GetOutputConf(
                self.handle,
                output_channel,
                byref(polarity),
                byref(led_polarity),
                byref(source_signal),
            )
        )
        return dict(
            polarity=Polarity(polarity.value),
            led_polarity=Polarity(led_polarity.value),
            source_signal=IOSources(source_signal.value),
        )

    @locking
    def set_input_configuration(self, input_channel, polarity, led_polarity):
        """
        Set the input configuration.

        Args:
            input_channel (int): The input channel to configure (0 - 1).
            polarity (Polarity): Polarity to set to.
            led_polarity (Polarity): LED polarity.
            source (IOSources): The source signal to propagate to the output line.
        """
        if not 0 <= input_channel <= 1:
            raise IndexError("Only channels between 0 and 1 are available.")
        check_error(
            lib_vme.CAENVME_SetInputConf(
                self.handle, input_channel, polarity.value, led_polarity.value
            )
        )

    @locking
    def get_input_configuration(self, input_channel):
        """
        Get the input configuration.

        Returns:
            dict: Dictionary with the configuration parameters.
        """
        if not 0 <= input_channel <= 1:
            raise IndexError("Only channels between 0 and 1 are available.")

        polarity = c_uint32()
        led_polarity = c_uint32()
        source_signal = c_uint32()

        check_error(
            lib_vme.CAENVME_GetInputConf(
                self.handle,
                input_channel,
                byref(polarity),
                byref(led_polarity),
                byref(source_signal),
            )
        )
        return dict(
            polarity=Polarity(polarity.value),
            led_polarity=Polarity(led_polarity.value),
            source_signal=IOSources(source_signal.value),
        )

    @locking
    def read_register(self, register):
        """
        Read a register.

        Args:
            register (Register): Register to read from
        """
        data = c_uint32()
        check_error(
            lib_vme.CAENVME_ReadRegister(self.handle, register.value, byref(data))
        )
        return data.value

    @locking
    def set_output_register(self, mask):
        """
        Write to output register.

        Args:
            mask (int): Mask (see OutputRegisterBits)
        """
        check_error(lib_vme.CAENVME_SetOutputRegister(self.handle, mask))

    @locking
    def clear_output_register(self, mask):
        """
        Clear bits in output register.

        Args:
            mask (int): Mask (see OutputRegisterBits)
        """
        check_error(lib_vme.CAENVME_ClearOutputRegister(self.handle, mask))

    @locking
    def pulse_output_register(self, mask):
        """
        Pulse bits in output register by setting and then clearing them.

        Args:
            mask (int): Mask (see OutputRegisterBits)
        """
        check_error(lib_vme.CAENVME_PulseOutputRegister(self.handle, mask))

    @locking
    def read_display(self):
        """
        The function reads the VME data display on the front panel of the module.

        Returns:
            Display: Front panel display info
        """
        display = Display()
        check_error(lib_vme.CAENVME_ReadDisplay(self.handle, byref(display)))
        return display

    @locking
    def reset_system(self):
        """ Reset the system """
        check_error(lib_vme.CAENVME_SystemReset(self.handle))

    @locking
    def reset_scaler_count(self):
        """ Reset the scaler count """
        check_error(lib_vme.CAENVME_ResetScalerCount(self.handle))

    @locking
    def enable_scaler_gate(self):
        """ Enable the scaler gate """
        check_error(lib_vme.CAENVME_EnableScalerGate(self.handle))

    @locking
    def disable_scaler_gate(self):
        """ Disable the scaler gate """
        check_error(lib_vme.CAENVME_DisableScalerGate(self.handle))

    @locking
    def get_scaler_count(self):
        """
        Read the scaler count.

        Returns:
            int: Scaler count
        """
        return self.read_register(Registers.SCALER_1)

    @locking
    def start_pulser(self, pulser):
        """
        Start the pulser

        Args:
            pulser (int): Pulser to start (0 <= pulser <= 1)
        """
        if not 0 <= pulser <= 1:
            raise ValueError("Only pulsers 0 or 1 are available")
        check_error(lib_vme.CAENVME_StartPulser(self.handle, pulser))

    @locking
    def stop_pulser(self, pulser):
        """
        Disable the scaler gate

        Args:
            pulser (int): Pulser to start (0 <= pulser <= 1)
        """
        if not 0 <= pulser <= 1:
            raise ValueError("Only pulsers 0 or 1 are available")
        check_error(lib_vme.CAENVME_StopPulser(self.handle, pulser))
