from device import Device 
from pixel import Pixel
import time
import numpy as np

class Lonely(Device):
    """Lonely pixel :("""

    def setup(self):
        self.pixels = [Pixel([0,0,0])]

    def update(self):
        t = time.time()
        self.pixels[0].r = (1+np.sin(t))/2.0
        self.pixels[0].g = (1+np.cos(t))/2.0
        self.pixels[0].b = 0.5

        return self.pixels

