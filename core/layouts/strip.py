from core.devices.pixel import Pixel
from layput import Layout

import numpy as np
from numpy.linalg import norm

class Strip(Layout):
    """
        Represents a strip of Leds
        start/direction are two element arrays (x,y)
        spacing/num_pixels are scalars
    """
    def __init__(self, start, direction, spacing, num_pixels):
        normed_direction = direction/norm(direction)

        self.pixels = []
        for i in range(num_pixels):
            self.pixels.append(Pixel(np.array(start) + i*spacing*normed_direction))