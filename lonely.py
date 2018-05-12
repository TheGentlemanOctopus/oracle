from device import Device 
from pixel import Pixel

class Lonely(Device):
    """Lonely pixel :("""

    def update(self):
        pixel = Pixel([0,0,0], color=[0, 100, 255])
        return [pixel]