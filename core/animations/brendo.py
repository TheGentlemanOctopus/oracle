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
        tr_hue=0.3,
        tr_hue_range=0.6,
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

        # Travellers
        self.add_param("tr_width", tr_width, 0, 1)
        self.add_param("tr_speed", tr_speed, -1, 1)
        self.add_param("tr_amplitude", tr_amplitude, 0, 1)
        self.add_param("tr_spacing", tr_spacing, 0, 1)
        self.add_param("tr_hue", tr_hue, 0, 1)
        self.add_param("tr_hue_range", tr_hue_range, 0, 1)
        self.add_param("tr_saturation", tr_saturation, 0, 1)

    def update(self):
        pixels = self.layout.pixels
      
        num_sections = int(self.params["num_sections"].value)
        indices = np.linspace(0, len(pixels), num_sections+1).astype(int)

        # Strip em!
        strips = []
        for i in range(len(indices)-1):
            strips.append(pixels[indices[i]:indices[i+1]])

        # Update
        curr_pattern = True
        for strip in strips:
            curr_pattern = not curr_pattern

            if curr_pattern:
                self.update_stander(strip)
            
            else:
                self.update_traveller(strip)


    def update_traveller(self, pixels):
        w = self.params["tr_width"].value
        a = self.params["tr_amplitude"].value
        v = self.params["tr_speed"].value
        spacing = self.params["tr_spacing"].value
        hue = self.params["tr_hue"].value
        hue_range = self.params["tr_hue_range"].value
        sat = self.params["tr_saturation"].value
     
        update_traveller(pixels, w, a, v, spacing, hue, hue_range, sat, self.fft)

    def update_stander(self, pixels):
        pass

