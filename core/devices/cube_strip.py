from output_device import OutputDevice
from pixel import Pixel
import numpy as np
import time

from core.layouts.strip import Strip

class CubeStrip(OutputDevice):
    """
        A simple device for device purposes, just a linear array of pixels
    """
    def __init__(self, channel, start, direction, spacing, num_pixels):
        super(CubeStrip, self).__init__()

        self.strip = Strip(start, direction, spacing, num_pixels)

        self.pixels_by_channel = {
            channel: self.strip.pixels
        }

    def update(self):
        t = time.time()
        for pixel in self.strip.pixels:
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
