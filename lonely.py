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
        self.pixels[0].r = (255.0/2)*(1+np.sin(t))
        self.pixels[0].g = (255.0/2)*(1+np.cos(t))
        self.pixels[0].b = 100

        return self.pixels

