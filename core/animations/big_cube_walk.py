from animation import Animation
from core.layouts.big_cube import BigCube

import time
import numpy as np
import colorsys

class BigCubeWalk(Animation):
    layout_type = "BigCube"

    def __init__(self, big_cube, period=5, hue_range=0.2):
        """
            Shifts pixel colors along a hue range in the order that the led strips woulf be laid in
            period is the number of seconds it takes a color to lap the cube
            hue_range defines the range of colors used as a prop of the color wheel
        """
        super(BigCubeWalk, self).__init__()

        self.layout = big_cube

        self.add_param("period", period, 0.5, 10)
        self.add_param("hue_range", hue_range, 0, 1)

    def update(self):
        pixels = self.layout.pixels

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
