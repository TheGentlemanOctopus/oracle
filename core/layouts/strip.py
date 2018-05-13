from core.devices.pixel import Pixel

import numpy as np

class Strip:
    """
        Represents a strip of Leds
        start/direction are two element arrays (x,y)
        spacing/num_pixels are scalars
    """
    def __init__(self, start, direction, spacing, num_pixels):
        # TODO: normalise direction
        self.pixels = []
        for i in range(num_pixels):
            self.pixels.append(Pixel(np.array(start) + i*spacing*np.array(direction)))