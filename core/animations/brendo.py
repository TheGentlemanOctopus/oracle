from animation import Animation

import time
import numpy as np
import colorsys

from numpy import pi

from travellers import update_pixels as update_traveller
from standers import update_pixels as update_stander

class Brendo(Animation):
    layout_type = "Layout"

    def __init__(self, layout, 
        num_sections=10,
        fft_channel=1,
        tr_width=0.1, 
        tr_speed=0.11, 
        tr_amplitude=0.83,
        tr_spacing=0.33,
        tr_hue=0.58,
        tr_saturation=0.71,
    ):
        """
            Shifts pixel colors along a hue range in the order that the led strips woulf be laid in
            period is the number of seconds it takes a color to lap the cube
            hue_range defines the range of colors used as a prop of the color wheel
        """
        super(Brendo, self).__init__()

        self.layout = layout

        self.add_param("num_sections", num_sections, 1, 10)

        # Standers
        self.add_param("wavelength", wavelength, 0.5, 10)
        self.add_param("amplitude", amplitude, 0, 1)
        self.add_param("frequency", frequency, 0.5, 10)
        self.add_param("saturation", saturation, 0, 1)
        self.add_param("fft_channel", fft_channel, 0, 6)
        self.add_param("hue", hue, 0, 1)

        # Travellers
        self.add_param("width", width, 0, 1)
        self.add_param("speed", speed, -1, 1)
        self.add_param("amplitude", amplitude, 0, 1)
        self.add_param("spacing", spacing, 0, 1)

    def update(self):
        pixels = self.layout.pixels

        # Traveller params
        w = self.params["width"].value
        a = self.params["amplitude"].value
        v = self.params["speed"].value
        spacing = self.params["spacing"].value
     
        # Standers
        w = self.params["frequency"].value
        A = self.params["amplitude"].value
        l = self.params["wavelength"].value
        sat = self.params["saturation"].value
        hue = self.params["hue"].value
      
        fft_index = int(self.params["fft_channel"].value)
        mod = self.fft[fft_index]

        num_sections = int(self.params["num_sections"].value)

        indices = np.linspace(0, len(pixels), num_sections+1).astype(int)

        # Strip em!
        strips = []
        for i in range(len(indices)-1):
            strips.append(pixels[indices[i]:indices[i+1]])

        curr_pattern = True
        for strip in strips:
            curr_pattern = not curr_pattern

            if curr_pattern:
                update_stander(strip, w, A, l, sat, hue, mod)
            
            else:
                update_traveller(strip, w, a, v, spacing, self.fft)





