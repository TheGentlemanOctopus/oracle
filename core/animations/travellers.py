from animation import Animation

import time
import numpy as np
import colorsys

from numpy import pi

class Travellers(Animation):
    layout_type = "Layout"

    def __init__(self, layout, 
        width=0.2, 
        speed=0.1, 
        amplitude=1,
        hue=0.58,
        saturation=0.71,
        fft_channel=0.9
    ):
        """
            Shifts pixel colors along a hue range in the order that the led strips woulf be laid in
            period is the number of seconds it takes a color to lap the cube
            hue_range defines the range of colors used as a prop of the color wheel
        """
        super(Travellers, self).__init__()

        self.layout = layout

        self.add_param("width", width, 0, 1)
        self.add_param("speed", speed, 0, 1)
        self.add_param("amplitude", amplitude, 0, 1)

        # TODO: Speed
        # self.add_param("saturation", saturation, 0, 1)

        # self.add_param("fft_channel", fft_channel, 0, 6)
        # self.add_param("hue", hue, 0, 1)

    def update(self):
        pixels = self.layout.pixels

        w = self.params["width"].value
        a = self.params["amplitude"].value
        v = self.params["speed"].value
     
        # sat = self.params["saturation"].value
        # fft_index = int(self.params["fft_channel"].value)

        # hue = self.params["hue"].value
        t = time.time()

        x = np.linspace(0, 1, len(pixels))
        r = gaussian(x, a, (v*t)%1, w)

        for i, pixel in enumerate(pixels):
            pixel.r = r[i]
            pixel.g = 0
            pixel.b = 0


def gaussian(x, a, b, c):
    """
        a: height
        b: center
        c: width
    """
    return a*np.exp( -(x-b)**2/c**2 )
