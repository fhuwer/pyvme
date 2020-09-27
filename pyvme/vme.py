class VMEModule:
    def __init__(self, controller, address):
        self.controller = controller
        self.base_address = address

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        del self.controller

    def read(self, address):
        return self.controller.read(self.base_address + address)

    def read_string(self, address_start, address_end):
        return self.controller.read_string(
            self.base_address + address_start, self.base_address + address_end
        )

    def write(self, address, data):
        self.controller.write(self.base_address + address, data)
