from device import Device 

class Lonely(Device):
    """Lonely pixel :("""

    def update(self):
        return [[0, 100, 255]]