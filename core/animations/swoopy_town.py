from animation import Animation

import time
import numpy as np

class SwoopyTown(Animation):
    layout_type="PixelList"

    def __init__(self, pixel_list, period=1, wavelength=2):
        """
            Swoopy spatially driven pattern for testing
        """

        super(SwoopyTown, self).__init__()

        self.layout = pixel_list

        self.add_params("period", period)
        self.add_params("wavelength", wavelength)

    def update(self):
        pixels = self.layout.pixels

        t = time.time()
        f = 1.0/self.params["period"]
        w = self.params["wavelength"]

        for pixel in pixels:
            x,y,z = pixel.location

            h = np.sin(2*np.pi*f + w*x)
            s = np.sin(2*np.pi*f + w*y)
            v = np.sin(2*np.pi*f + w*z)

            pixel.set_hsv(h,s,v)