from output_device import OutputDevice
from pixel import Pixel
import numpy as np
import time

from core.layouts.strip import Strip
from core.animations.swoopy_town import SwoopyTown

class CubeStrip(OutputDevice):
    """
        A simple device for device purposes, just a linear array of pixels
    """
    def __init__(self, channel, start, direction, spacing, num_pixels):
        super(CubeStrip, self).__init__()

        self.layout = Strip(start, direction, spacing, num_pixels)

        self.animation = SwoopyTown(self.layout)

        self.pixels_by_channel = {
            channel: self.layout.pixels
        }

