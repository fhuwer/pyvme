from time import sleep
from enum import Enum
from ..vme import VMEModule


class V2495(VMEModule):
    def __init__(self, controller, address):
        super().__init__(controller, address)
