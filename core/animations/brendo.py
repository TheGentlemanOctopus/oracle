from animation import Animation

import time
import numpy as np
import colorsys

from numpy import pi

import travellers 
import standers

from utils import add_params

class Brendo(Animation):
    layout_type = "Layout"

    def __init__(self, layout, 
        shift_rate=0,
        num_sections=10,
        **kwargs
    ):
        """
            Shifts pixel colors along a hue range in the order that the led strips woulf be laid in
            period is the number of seconds it takes a color to lap the cube
            hue_range defines the range of colors used as a prop of the color wheel
        """
        super(Brendo, self).__init__()

        self.layout = layout

        self.add_param("num_sections", num_sections, 1, 10)
        self.add_param("shift_rate", shift_rate, 0, 30)

        # Travellers
        traveller_params = {"tr_"+key: value for key,value in travellers.params.items()}
        standers_params = {"st_"+key: value for key,value in standers.params.items()}

        add_params(self, traveller_params, strict=False, **kwargs)
        add_params(self, standers_params, strict=False, **kwargs)

    def update(self):
        # Get Shwifty
        shift_rate = self.params["shift_rate"].value
        n = int(time.time()*shift_rate)%len(self.layout.pixels)

        pixels = self.layout.pixels[n:] + self.layout.pixels[:n]

        # Slice them and dice them      
        num_sections = int(self.params["num_sections"].value)
        indices = np.linspace(0, len(pixels), num_sections+1).astype(int)

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
     
        travellers.update_pixels(pixels, w, a, v, spacing, hue, hue_range, sat, self.fft)

    def update_stander(self, pixels):
        w = self.params["st_frequency"].value
        A = self.params["st_amplitude"].value
        l = self.params["st_wavelength"].value
        sat = self.params["st_saturation"].value
        hue = self.params["st_hue"].value
      
        fft_index = int(self.params["st_fft_channel"].value)
        mod = self.fft[fft_index]

        standers.update_pixels(pixels, w, A, l, sat, hue, mod)
