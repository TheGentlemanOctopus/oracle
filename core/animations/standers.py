from animation import Animation

import time
import numpy as np
import colorsys

from numpy import pi

class Standers(Animation):
    layout_type = "Layout"

    def __init__(self, layout, 
        wavelength=4, 
        amplitude=0.21, 
        frequency=2.6,
        hue=0.58,
        saturation=0.71,
        fft_channel=0.9
    ):
        """
            Shifts pixel colors along a hue range in the order that the led strips woulf be laid in
            period is the number of seconds it takes a color to lap the cube
            hue_range defines the range of colors used as a prop of the color wheel
        """
        super(Brendo, self).__init__()

        self.layout = layout

        self.add_param("wavelength", wavelength, 0.5, 10)
        self.add_param("amplitude", amplitude, 0, 1)
        self.add_param("frequency", frequency, 0.5, 10)
        self.add_param("saturation", saturation, 0, 1)
        self.add_param("fft_channel", fft_channel, 0, 6)
        
        self.add_param("hue", hue, 0, 1)

    def update(self):
        pixels = self.layout.pixels

        w = self.params["frequency"].value
        A = self.params["amplitude"].value
        l = self.params["wavelength"].value
        sat = self.params["saturation"].value
        fft_index = int(self.params["fft_channel"].value)

        hue = self.params["hue"].value
        t = time.time()

        x = np.linspace(0, 1, len(pixels))

        s = sat + (1-sat)*self.fft[fft_index]
        v = 1

        for i, pixel in enumerate(pixels):
            h = (hue + A*np.sin(2*pi*x[i]/l)*np.cos(w*t)) % 1

            pixel.set_hsv(h,s,v)