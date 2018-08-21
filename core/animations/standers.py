from animation import Animation

import time
import numpy as np
import colorsys

from numpy import pi

params = {
    "wavelength": [4, 0.5, 10],
    "amplitude": [0.21, 0, 1],
    "frequency": [2.6, 0.5, 10],
    "saturation": [0.71, 0, 1],
    "hue": [0.58,0, 1],
    "fft_channel": [1, 0, 6]
}


class Standers(Animation):
    layout_type = "Layout"

    def __init__(self, layout, **kwargs):
        """
            Shifts pixel colors along a hue range in the order that the led strips woulf be laid in
            period is the number of seconds it takes a color to lap the cube
            hue_range defines the range of colors used as a prop of the color wheel
        """
        super(Standers, self).__init__()

        self.layout = layout

        # Sort out params
        for name, value in kwargs.items():
            if not name in params:
                raise Exception("Unknonwn params: %s"%name)

            params[name][0] = value
        
        for name, value in params.items():
            self.add_param(name, value[0], value[1], value[2])

    def update(self):
        pixels = self.layout.pixels

        w = self.params["frequency"].value
        A = self.params["amplitude"].value
        l = self.params["wavelength"].value
        sat = self.params["saturation"].value
        hue = self.params["hue"].value
      
        fft_index = int(self.params["fft_channel"].value)
        mod = self.fft[fft_index]

        update_pixels(pixels, w, A, l, sat, hue, mod)

def update_pixels(pixels, 
    w,
    A,
    l,
    sat,
    hue,
    mod
):
    t = time.time()

    x = np.linspace(0, 1, len(pixels))

    s = sat + (1-sat)*mod
    v = 1

    for i, pixel in enumerate(pixels):
        h = (hue + A*np.sin(2*pi*x[i]/l)*np.cos(w*t)) % 1

        pixel.set_hsv(h,s,v)
