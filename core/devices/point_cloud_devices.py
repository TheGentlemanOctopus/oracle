import numpy as np

from output_device import OutputDevice
from core.layouts.pixel_list import PixelList
from core.animations.spiral_out_fast import SpiralOutFast


class PointCloudDevice(OutputDevice):
    """
        A generic device that is just a list of points
    """
    def __init__(self, pixels, channel):
        super(PointCloudDevice, self).__init__()

        self.pixels_by_channel = {channel: pixels}
        self.layout = PixelList(pixels)
        self.animation = SpiralOutFast(self.layout)
