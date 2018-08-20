from animation import Animation

import time
import numpy as np
import colorsys

from numpy import pi

class Brendo(Animation):
    layout_type = "Layout"

    def __init__(self, layout, wavelength=1, amplitude=1, frequency=1):
        """
            Shifts pixel colors along a hue range in the order that the led strips woulf be laid in
            period is the number of seconds it takes a color to lap the cube
            hue_range defines the range of colors used as a prop of the color wheel
        """
        super(Brendo, self).__init__()

        self.layout = layout

        self.add_param("wavelength", wavelength, 0.5, 10)
        self.add_param("amplitude", amplitude, 0.5, 10)
        self.add_param("frequency", frequency, 0.5, 10)

    def update(self):
        pixels = self.layout.pixels

        w = self.params["frequency"].value
        A = self.params["amplitude"].value
        l = self.params["wavelength"].value
        t = time.time()

        x = np.linspace(0, 1, len(pixels))

        s = 1
        v = 1

        for i, pixel in enumerate(pixels):
            h = 2*A*np.sin(2*pi*x[i]/l)*np.cos(w*t)

            pixel.set_hsv(h,s,v)

        return

        period = self.params["period"].value
        hue_range = self.params["hue_range"].value

        # Shift pixel ordering according to period phase
        shift = int(len(pixels)*(time.time() % period)/period)
        pixels = np.concatenate([pixels[shift:], pixels[:shift]])

        # One lap of the color wheel in the order
        s = 1 # Saturation
        v = 1 # Value
        for i, h in enumerate(np.linspace(0, hue_range, len(pixels))):
            
            # shift hue with weighted fft avg that favours bass :)
            weights = np.array(range(len(self.fft)))[::-1]
            h_shift = np.average(self.fft, weights=weights)
            h_shifted = (h + h_shift) % 1

            pixel = pixels[i]
            pixel.r, pixel.g, pixel.b = colorsys.hsv_to_rgb(h_shifted,s,v)
