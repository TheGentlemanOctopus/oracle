from device import Device 
from pixel import Pixel
import time
import numpy as np

class Lonely(Device):
    """Lonely pixel :("""

    def __init__(self, channel):
        self.pixel = Pixel([0,0,0])

        self.pixels_by_channel = {
            channel: [self.pixel]
        }

    def update(self):
        t = time.time()
        self.pixel.r = (1+np.sin(t))/2.0
        self.pixel.g = (1+np.cos(t))/2.0
        self.pixel.b = 0.5

        return self.pixels

