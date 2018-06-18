import numpy as np

from output_device import OutputDevice
from core.layouts.strip import Strip
import colorsys
import time

from core.layouts.big_cube import BigCube
from core.animations.big_cube_walk import BigCubeWalk

class BigCubeDevice(OutputDevice):
    """
        A device with a big cube only
    """

    def __init__(self, channel, led_spacing, strip_spacing):
        super(BigCubeDevice, self).__init__()

        self.layout = BigCube(led_spacing, strip_spacing)

        # TODO: Generalise so we can actively switch between animation sets
        self.animation = BigCubeWalk(self.big_cube)

        # Form pixels by channel dict
        self.pixels_by_channel = {
            channel: self.big_cube.pixels
        }

