from core.devices.pixel import Pixel

import numpy as np

class Strip:
    """
        A strip of Leds
    """
    def __init__(self, start, direction, spacing, num_pixels):
        self.pixels = []
        for i in range(num_pixels):
            self.pixels.append(Pixel(np.array(start) + i*spacing*np.array(direction)))