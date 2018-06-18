from animation import Animation

import time
import numpy as np

class SwoopyTown(Animation):
    layout_type="Layout"

    def __init__(self, pixel_list, period=1, wavelength=2):
        """
            Swoopy spatially driven pattern for testing
        """

        super(SwoopyTown, self).__init__()

        self.layout = pixel_list

        self.add_param("period", period)
        self.add_param("wavelength", wavelength)

    def update(self):
        pixels = self.layout.pixels

        t = time.time()
        f = 1.0/self.params["period"]
        w = self.params["wavelength"]

        for pixel in pixels:
            x,y,z = pixel.location

            h = 0.5*(1 + np.sin(2*np.pi*f*t + w*x))
            s = 0.5*(1 + np.sin(2*np.pi*f*t+ w*y))
            v = 0.5*(1 + np.sin(2*np.pi*f*t + w*z))

            pixel.set_hsv(h,s,v)