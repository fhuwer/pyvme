from enum import Enum
from ctypes import Structure, c_long, c_bool


class BoardTypes(Enum):
    """
    Board types

    Attributes:
        V1718 (int): V1718 USB-VME bridge
        V2718 (int): V2718 PCI-VME bridge with optical link
        V2818 (int): PCI board with optical link
        V2719 (int): Optical link piggy-back
        V3818 (int): PCIe baord with up to 4 optical links
    """

    V1718 = 0
    V2718 = 1
    A2818 = 2
    A2719 = 3
    A3818 = 4


class DataWidth(Enum):
    """
    Data width.

    Attributes:
        D8 (int): 8-bit data
        D16 (int): 16-bit data
        D32 (int): 32-bit data
        D64 (int): 64-bit data
        D16 (int): 16-bit data swapped
        D32 (int): 32-bit data swapped
        D64 (int): 64-bit data swapped
    """

    D8 = 0x01
    D16 = 0x02
    D32 = 0x04
    D64 = 0x08
    D16_swapped = 0x12
    D32_swapped = 0x14
    D64_swapped = 0x18


class AddressModifier(Enum):
    """
    VME cycles address modifiers

    Attributes:
        A16_SUPERVISORY (int): A16 supervisory access
        A16_NON_PRIVILEGED (int): A16 non-privileged
        A16_LOCK (int): A16 lock command

        A24_SUPERVISORY_BLOCK (int): A24 supervisory block transfer
        A24_SUPERVISORY_PROGRAM (int): A24 supervisory program access
        A24_SUPERVISORY_DATA (int): A24 supervisory data access
        A24_SUPERVISORY_BLOCK_64 (int): A24 supervisory block transfer

        A24_NON_PRIVILEGED_BLOCK (int): A24 non-privileged block transfer
        A24_NON_PRIVILEGED_PROGRAM (int): A24 non-privileged program access
        A24_NON_PRIVILEGED_DATA (int): A24 non-privileged 64-bit block transfer
        A24_NON_PRIVILEGED_BLOCK_64 (int): A24 non-privileged block transfer
        A24_LOCK (int): A24 lock

        A32_SUPERVISORY_BLOCK (int): A32 supervisory block transfer
        A32_SUPERVISORY_PROGRAM (int): A32 supervisory program access
        A32_SUPERVISORY_DATA (int): A32 supervisory data access
        A32_SUPERVISORY_BLOCK_64 (int): A32 supervisory block transfer

        A32_NON_PRIVILEGED_BLOCK (int): A32 non-privileged block transfer
        A32_NON_PRIVILEGED_PROGRAM (int): A32 non-privileged program access
        A32_NON_PRIVILEGED_DATA (int): A32 non-privileged 64-bit block transfer
        A32_NON_PRIVILEGED_BLOCK_64 (int): A32 non-privileged block transfer
        A32_LOCK (int): A32 lock

        CR_CSR (int): CR/CSR space
    """

    A16_SUPERVISORY = 0x2D
    A16_NON_PRIVILEGED = 0x29
    A16_LOCK = 0x2C

    A24_SUPERVISORY_BLOCK = 0x3F
    A24_SUPERVISORY_PROGRAM_ACCESS = 0x3E
    A24_SUPERVISORY_DATA_ACCESS = 0x3D
    A24_SUPERVISORY_BLOCK_64 = 0x3C

    A24_NON_PRIVILEGED_BLOCK = 0x3B
    A24_NON_PRIVILEGED_PROGRAM = 0x3A
    A24_NON_PRIVILEGED_DATA = 0x39
    A24_NON_PRIVILEGED_BLOCK_64 = 0x38
    A24_LOCK = 0x32

    A32_SUPERVISORY_BLOCK = 0x0F
    A32_SUPERVISORY_PROGRAM = 0x0E
    A32_SUPERVISORY_DATA = 0x0D
    A32_SUPERVISORY_BLOCK_64 = 0x0C

    A32_NON_PRIVILEGED_BLOCK = 0x0B
    A32_NON_PRIVILEGED_PROGRAM = 0x0A
    A32_NON_PRIVILEGED_DATA = 0x09
    A32_NON_PRIVILEGED_BLOCK_64 = 0x08
    A32_LOCK = 0x05

    CR_CSR = 0x2F


class IOSources(Enum):
    """
    IO sources

    Attributes:
        MANUAL (int): Manual (button) or software controlled
        INPUT_SOURCE_0 (int): Input line 0
        INPUT_SOURCE_1 (int): Input line 1
        COINCIDENCE (int): Inputs coincidence
        VME_SIGNAL (int): Signals from VME bus
        MISC_SIGNALS (int): Various internal signals
    """

    MANUAL = 0
    INPUT_SOURCE_0 = 1
    INPUT_SOURCE_1 = 2
    COINCIDENCE = 3
    VME_SIGNAL = 4
    MISC_SIGNALS = 6


class TimeUnits(Enum):
    """
    Time base units to specify pulses period and width.

    Attributes:
        UNIT_25ns (int): Time unit is 25 ns
        UNIT_1600ns (Int): TIme unit is 1.6 microseconds
        UNIT_410us (Int): TIme unit is 410 microseconds
        UNIT_104ms (Int): TIme unit is 104 milliseconds
    """

    UNIT_25ns = 0
    UNIT_1600ns = 1
    UNIT_410us = 2
    UNIT_104ms = 3


class Polarity(Enum):
    """
    Polarity.

    Attributes:
        ACTIVE_HIGH (int): Active high (normal polarity / LED on on signal high)
        ACTIVE_LOW (int): Active low (inverted polarity / LED on on signal low)
    """

    ACTIVE_HIGH = 0
    ACTIVE_LOW = 1


class Registers(Enum):
    """
    Accessible registers.

    Attributes:
        STATUS (int): Status register
        VME_CONTROL (int): VME control register
        FIRMWARE_RELEASE (int): Firmware Release register
        FIRMWARE_DOWNLOAD (int): Firmware Download register
        FLASH_ENABLE (int): Flash enable register
        VME_IRQ_LINES_ENABLE (int): VME IRQ Lines Enable register
        INPUT (int): Input register
        OUTPUT (int): Output register
        INPUT_MULITPLEXER (int): Input multiplexer register
        OUTPUT_MULITPLEXER (int): Output multiplexer register
        LED_POLARITY (int): Led polarity register
        OUTPUT_CLEAR (int): Output clear register
        INPUT_MULITPLEXER_CLEAR (int): Input multiplexer clear register
        OUTPUT_MULITPLEXER_CLEAR (int): Output multiplexer clear register
        LED_POLARITY_CLEAR (int): Led polarity clear register
        PULSER_A0 (int): Period and width of Pulser A
        PULSER_A1 (int): Num pulses and range of Pulser A
        PULSER_B0 (int): Period and width of Pulser B
        PULSER_B1 (int): Num pulses and range of Pulser B
        SCALER_0 (int): Limit and Autores of Scaler A
        SCALER_1 (int): Counter value of Scaler A
        DISPLAY_AD_LOW (int): Display AD[15:0]
        DISPLAY_AD_HIGH (int): Display AD[31:16]
        DISPLAY_DT_LOW (int): Display DT[15:0]
        DISPLAY_DT_HIGH (int): Display DT[31:16]
        DISPLAY_CONTROL_1 (int): Display Control left bar
        DISPLAY_CONTROL_2 (int): Display Control left bar
        LOC_MON_AD_LOW (int): Loc. Mon. AD[15:0]
        LOC_MON_AD_HIGH (int): Loc. Mon. AD[31:16]
        LOC_MON_CONTROLS (int): Loc. Mon. Controls
    """

    STATUS = 0x00
    VME_CONTROL = 0x01
    FIRMWARE_RELEASE = 0x02
    FIRMWARE_DOWNLOAD = 0x03
    FLASH_ENABLE = 0x04
    VME_IRQ_LINES_ENABLE = 0x06
    INPUT = 0x08
    OUTPUT = 0x0A
    INPUT_MULITPLEXER = 0x0B
    OUTPUT_MULITPLEXER = 0x0C
    LED_POLARITY = 0x0D
    OUTPUT_CLEAR = 0x10
    INPUT_MULITPLEXER_CLEAR = 0x11
    OUTPUT_MULITPLEXER_CLEAR = 0x12
    LED_POLARITY_CLEAR = 0x13
    PULSER_A0 = 0x16
    PULSER_A1 = 0x17
    PULSER_B0 = 0x19
    PULSER_B1 = 0x1A
    SCALER_0 = 0x1C
    SCALER_1 = 0x1D
    DISPLAY_AD_LOW = 0x20
    DISPLAY_AD_HIGH = 0x21
    DISPLAY_DT_LOW = 0x22
    DISPLAY_DT_HIGH = 0x23
    DISPLAY_CONTROL_1 = 0x24
    DISPLAY_CONTROL_2 = 0x25
    LOC_MON_AD_LOW = 0x28
    LOC_MON_AD_HIGH = 0x29
    LOC_MON_CONTROLS = 0x2C


class StatusRegisterBits(Enum):
    """
    Bits for status register decoding.

    Attributes:

        SYSTEM_RESET (int): VME is in system reset state
        SYSTEM_CONTROLLER (int): The bridge is the VME system controller
        DTACK (int): Last access has generated a DTACK signal
        BUS_ERROR (int): Last access has generated a bus error
        DIP_0 (int): Dip Switch position 0 state
        DIP_1 (int): Dip Switch position 1 state
        DIP_2 (int): Dip Switch position 2 state
        DIP_3 (int): Dip Switch position 3 state
        DIP_4 (int): Dip Switch position 4 state
        USBTYPE (int): USB Speed: 0 = Full; 1 = High
    """

    SYSTEM_RESET = 0x0001
    SYSTEM_CONTROLLER = 0x0002
    DTACK = 0x0010
    BUS_ERROR = 0x0020
    DIP_0 = 0x0100
    DIP_1 = 0x0200
    DIP_2 = 0x0400
    DIP_3 = 0x0800
    DIP_4 = 0x1000
    USB_TYPE = 0x8000


class InputRegisterBits(Enum):
    """
    Bits for input register decoding.

    Attributes:
        IN0 (int): Input line 0 signal level.
        IN1 (int): Input line 1 signal level.
        COINCIDENCE (int): Coincidence of input signal level.
        PULSER_A_OUTPUT (int): Pulser A output signal level.
        PULSER_B_OUTPUT (int): Pulser B output signal level.
        SCALER_END_COUNTER (int): Scaler end counter signal level.
        LOCATION_MONITOR (int): Location monitor signal level.
    """

    IN0 = 0x0001
    IN1 = 0x0002
    COINCIDENCE = 0x0004
    PULSER_A_OUTPUT = 0x0008
    PULSER_B_OUTPUT = 0x0010
    SCALER_END_COUNTER = 0x0020
    LOCATION_MONITOR = 0x0040


class OutputRegisterBits(Enum):
    """
    Bits for input register decoding.

    Attributes:
        PULSER_A_START (int): Pulser A start signal level.
        PULSER_A_RESET (int): Pulser A reset signal level.
        PULSER_B_START (int): Pulser B start signal level.
        PULSER_B_RESET (int): Pulser B reset signal level.
        SCALER_GATE (int): Scaler gate signal level.
        SCALER_RESET (int): Scaler reset counter signal level.
        OUTPUT_0 (int): Output line 0 signal level.
        OUTPUT_1 (int): Output line 1 signal level.
        OUTPUT_2 (int): Output line 2 signal level.
        OUTPUT_3 (int): Output line 3 signal level.
        OUTPUT_4 (int): Output line 4 signal level.
    """

    PULSER_A_START = 0x0001
    PULSER_A_RESET = 0x0002
    PULSER_B_START = 0x0004
    PULSER_B_RESET = 0x0008
    SCALER_GATE = 0x0010
    SCALER_RESET = 0x0020
    OUTPUT_0 = 0x0040
    OUTPUT_1 = 0x0080
    OUTPUT_2 = 0x0100
    OUTPUT_3 = 0x0200
    OUTPUT_4 = 0x0400


class ArbiterTypes(Enum):
    """
    Types of VME Arbiter.

    Attributes:
        PRIORIZED (int): Priority Arbiter
        ROUND_ROBIN (int): Round-Robin Arbiter
    """

    PRIORIZED = 0
    ROUND_ROBIN = 1


class RequesterTypes(Enum):
    """
    Types of VME Bus Requester.

    Attributes:
        FAIR (int): Fair bus requester
        DEMAND (int): On demand bus requester
    """

    FAIR = 0
    DEMAND = 1


class ReleaseTypes(Enum):
    """
    Types of VME Bus release.

    Attributes:
        RELEASE_WHEN_DONE (int): Release When Done
        RELEASE_ON_REQUEST (int): Release On Request
    """

    RELEASE_WHEN_DONE = 0
    RELEASE_ON_REQUEST = 1


class BusReqLevels(Enum):
    """
    VME bus request levels.

    Attributes:
        BUS_REQUEST_0 (int): Bus request level 0
        BUS_REQUEST_1 (int): Bus request level 1
        BUS_REQUEST_2 (int): Bus request level 2
        BUS_REQUEST_3 (int): Bus request level 3
    """

    BUS_REQUEST_0 = 0
    BUS_REQUEST_1 = 1
    BUS_REQUEST_2 = 2
    BUS_REQUEST_3 = 3


class IRQLevels(Enum):
    """
    VME Interrupt levels.

    Attributes:
        IRQ_1 (int): Interrupt level 1
        IRQ_2 (int): Interrupt level 2
        IRQ_3 (int): Interrupt level 3
        IRQ_4 (int): Interrupt level 4
        IRQ_5 (int): Interrupt level 5
        IRQ_6 (int): Interrupt level 6
        IRQ_7 (int): Interrupt level 7
    """

    IRQ_1 = 0x01
    IRQ_2 = 0x02
    IRQ_3 = 0x04
    IRQ_4 = 0x08
    IRQ_5 = 0x10
    IRQ_6 = 0x20
    IRQ_7 = 0x40


class VMETimeouts(Enum):
    """
    VME bus timeouts.

    Attributes:
        TIMEOUT_50us (int): Timeout is 50 microseconds
        TIMEOUT_400us (int): Timeout is 400 microseconds
    """

    TIMEOUT_50us = 0
    TIMEOUT_400us = 1


class Display(Structure):
    """
    Data type to store the front panel display last access data.

    Attributes:
        address (int): VME Address
        data (int): VME Data
        am (int): Address modifier
        irq (int): IRQ levels
        data_strobe_0 (bool): Data Strobe 0 signal
        data_strobe_1 (bool): Data Strobe 1 signal
        address_strobe (bool): Address Strobe signal
        interrupt_acknowledge (bool): Interrupt Acknowledge signal
        write (bool): Write signal
        long_word (bool): Long Word signal
        data_acknowledge (bool): Data Acknowledge signal
        bus_error (bool): Bus Error signal
        system_error (bool): System Reset signal
        bus_request (bool): Bus Request signal
        bus_grant (bool): Bus Grant signal
    """

    _fields_ = [
        ("address", c_long),
        ("data", c_long),
        ("am", c_long),
        ("irq", c_long),
        ("data_strobe_0", c_bool),
        ("data_strobe_1", c_bool),
        ("address_strobe", c_bool),
        ("interrupt_acknowledge", c_bool),
        ("write", c_bool),
        ("long_word", c_bool),
        ("data_acknowledge", c_bool),
        ("bus_error", c_bool),
        ("system_error", c_bool),
        ("bus_request", c_bool),
        ("bus_grant", c_bool),
    ]
