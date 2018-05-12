from device import Device
from pixel import Pixel
import numpy as np
import time
import matplotlib.pyplot as plt

class CubeStrip(Device):
    def __init__(self, channel, start, direction, spacing, num_pixels):
        self.pixels = []
        for i in range(num_pixels):
            self.pixels.append(Pixel(np.array(start) + i*spacing*np.array(direction)))


        self.pixels_by_channel = {
            channel: self.pixels
        }

    def update(self):
        t = time.time()
        for pixel in self.pixels:
            pixel.r = 0.5*(1+ np.sin(pixel.location[0]/np.pi + t))
            pixel.g = 0.5*(1+ np.cos(pixel.location[0]/np.pi + t))
            pixel.b = 0.5*(1+ np.sin(pixel.location[0]/np.pi + t + np.pi/2))

        return self.pixels

if __name__ == "__main__":
    start = [0,0,0]
    direction = [1,0,0]
    spacing = 1 
    num_pixels = 10

    strip = CubeStrip(start, direction, spacing, num_pixels)
    
    for pixel in strip.pixels:
        print pixel.location
