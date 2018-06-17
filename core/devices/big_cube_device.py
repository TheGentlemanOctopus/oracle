import numpy as np

from output_device import OutputDevice
from core.layouts.strip import Strip
import colorsys
import time

from core.layouts.big_cube import BigCube

class BigCubeDevice(OutputDevice):


    def __init__(self, channel, led_spacing, strip_spacing):
        super(BigCube, self).__init__()

        self.big_cube = BigCube(led_spacing, strip_spacing)

        # Form pixels by channel dict
        self.pixels_by_channel = {
            channel: self.pixels
        }

    # Makes the self.pixels method act as a variable
    @property
    def pixels(self):
        """
            Returned in the order that strips should be laid
        """
        return self.big_cube.pixels
    
    def update(self, period=5, hue_range=0.2):
        # Period is the number of seconds it takes a color to lap the cube
        # hue_range defines the range of colors used as a prop of the color wheel
        # TODO: Move period when we have pattern gen capabailities
        pixels = self.pixels

        # Shift pixel ordering according to period phase
        shift = int(len(pixels)*(time.time() % period)/period)
        pixels = np.concatenate([pixels[shift:], pixels[:shift]])

        # One lap of the color wheel in the order
        s = 1 # Saturation
        v = 1 # Value
        for i, h in enumerate(np.linspace(0, hue_range, len(pixels))):
            # shift hue with weighted fft avg that favours bass :)
            weights = np.array(range(len(self.fft_data)))[::-1]
            h_shift = np.average(self.fft_data, weights=weights)
            h_shifted = (h + h_shift) % 1

            pixel = pixels[i]
            pixel.r, pixel.g, pixel.b = colorsys.hsv_to_rgb(h_shifted,s,v)



