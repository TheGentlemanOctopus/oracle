from device import Device 
from pixel import Pixel

class Lonely(Device):
    """Lonely pixel :("""

    def setup(self):
        self.pixels = [Pixel([0,0,0], color=[0, 100, 255])]

    def update(self):
        return self.pixels

