import numpy as np

from output_device import OutputDevice
from core.layouts.strip import Strip
from core.layouts.pixel_list import PixelList

from core.animations.spiral_out_fast import SpiralOutFast
from core.animations.panel_utils import fmap

class FacePanelDevice(OutputDevice):
    """
        A generic pixels by channel device that made be used for displaying the individual panels as a series of strips
    """
    def __init__(self, led_spacing, strip_spacing, channel):
        super(FacePanelDevice, self).__init__()

        self.pixels_by_channel = {}

        # For placing strips
        start = np.array(([0,0,0])).astype(float)
        direction = np.array([1,0,0]).astype(float)
        strip_offset = np.array([0, strip_spacing, 0]).astype(float)

        # Form one strip per face panel
        pixels = []
        for pix_orders in fmap['right']:
            pixel_count = pix_orders[1] - pix_orders[0]
            strip = Strip(start, direction, led_spacing, pixel_count)

            pixels.extend(strip.pixels)
            start += strip_offset


        for pix_orders in fmap['centre']:
            pixel_count = pix_orders[1] - pix_orders[0]
            strip = Strip(start, direction, led_spacing, pixel_count)

            pixels.extend(strip.pixels)
            start += strip_offset
            

        for pix_orders in fmap['left']:
            pixel_count = pix_orders[1] - pix_orders[0]
            strip = Strip(start, direction, led_spacing, pixel_count)

            pixels.extend(strip.pixels)
            start += strip_offset    
        print pixels
        self.pixels_by_channel[int(channel)] = pixels
        # A generic layout that can be used with generic patterns
        self.layout = PixelList(pixels)
        self.animation = SpiralOutFast(self.layout)