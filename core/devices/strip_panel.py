from device import Device
from pixel import Pixel
import numpy as np
import time

from core.layouts.panel import Panel

class StripPanel(Device):
    """
        A simple device for device purposes, just a linear array of pixels
    """
    def __init__(self, channel, origin, led_spacing, strip_spacing, num_pixels_x, num_strips_y):
        super(StripPanel, self).__init__()

        self.panel = Panel(origin, led_spacing, strip_spacing, num_pixels_x, num_strips_y)

        self.pixels_by_channel = {
            channel: self.pixels
        }

    # Makes the self.pixels method act as a variable
    @property
    def pixels(self):
        """
            Returned in the order that strips should be laid
        """
        return np.concatenate([strip.pixels for strip in self.panel.strips])

    def update(self):
        t = time.time()
        for pixel in self.pixels:
            pixel.r = 0.5*(1+ np.sin(pixel.location[0]/np.pi + t))
            pixel.g = 0.5*(1+ np.cos(pixel.location[0]/np.pi + t))
            pixel.b = 0.5*(1+ np.sin(pixel.location[0]/np.pi + t + np.pi/2))

if __name__ == "__main__":
    start = [0,0,0]
    direction = [1,0,0]
    spacing = 1 
    num_pixels = 10

    strip = CubeStrip(start, direction, spacing, num_pixels)
    
    for pixel in strip.pixels:
        print pixel.location
