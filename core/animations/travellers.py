from animation import Animation

import time
import numpy as np
import colorsys

from numpy import pi
from utils import add_params

params = {
    "width": [0.1, 0, 1], 
    "speed": [0.11, -1, 1], 
    "amplitude": [0.83, 0, 1],
    "spacing": [0.33, 0, 1],
    "hue": [0.3, 0, 1],
    "hue_range": [0.6, 0, 1],
    "saturation": [0.71, 0, 1],
    "fft_channel": [0.9, 0, 6]
}

class Travellers(Animation):
    layout_type = "Layout"

    def __init__(self, layout, **kwargs):
        """
            Shifts pixel colors along a hue range in the order that the led strips woulf be laid in
            period is the number of seconds it takes a color to lap the cube
            hue_range defines the range of colors used as a prop of the color wheel
        """
        super(Travellers, self).__init__()

        self.layout = layout

        add_params(self, params, **kwargs)

    def update(self):
        pixels = self.layout.pixels

        w = self.params["width"].value
        a = self.params["amplitude"].value
        v = self.params["speed"].value
        spacing = self.params["spacing"].value
        hue = self.params["hue"].value
        hue_range = self.params["hue_range"].value
        sat = self.params["saturation"].value
     
        update_pixels(pixels, w, a, v, spacing, hue, hue_range, sat, self.fft)


def update_pixels(pixels, 
    width, 
    amplitude, 
    speed, 
    spacing, 
    hue,
    hue_range,
    sat,
    fft
):
    x = np.linspace(0, 1, len(pixels))

    w = width
    v = speed
    t = time.time()
    a = amplitude

    # A sum of spatial gaussians
    g = np.zeros(len(pixels))
    for center in np.arange(0, 1, spacing):
        g = g + gaussian(np.mod(x-v*t, 1), a, center, w)

    # Hue-e hoo haha
    # hue = np.linspace(0, 1, len(pixels))

    for i, pixel in enumerate(pixels):
        h = (g[i]*hue_range + hue)%1
        s = g[i]
        v = g[i]

        pixel.set_hsv(h,s,v)


def gaussian(x, a, b, c):
    """
        a: height
        b: center
        c: width
    """
    return a*np.exp( -(x-b)**2/c**2 )
