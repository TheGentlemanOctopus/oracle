import numpy as np

from output_device import OutputDevice
from core.layouts.strip import Strip
from core.layouts.pixel_list import PixelList

from core.animations.spiral_out_fast import SpiralOutFast


class WonderfaceDevice(OutputDevice):
    def __init__(self, led_spacing, strip_spacing, pixels_per_channel):
        super(WonderfaceDevice, self).__init__()

        self.pixels_by_channel = {}

        start = np.array(([0,0,0])).astype(float)
        direction = np.array([1,0,0]).astype(float)
        strip_offset = np.array([0, strip_spacing, 0]).astype(float)

        pixels = []
        for channel, pixel_count in pixels_per_channel.items():
            strip = Strip(start, direction, led_spacing, pixel_count)

            pixels.extend(strip.pixels)
            self.pixels_by_channel[int(channel)] = strip.pixels

            start += strip_offset

        self.layout = PixelList(pixels)

        self.animation = SpiralOutFast(self.layout)