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
    def __init__(self, led_spacing, strip_spacing, channel, hw_chan_length):
        super(FacePanelDevice, self).__init__()

        self.pixels_by_channel = {}

        # For placing strips
        start = np.array(([0,-3,0])).astype(float)
        direction = np.array([1,0,0]).astype(float)
        strip_offset = np.array([0, strip_spacing, 0]).astype(float)

        # Form one strip per face panel
        pixels = []
        for pix_orders in fmap['left']:
            pixels.extend(gen_strip(pix_orders, start, direction, led_spacing))
            start += strip_offset
        pixels.extend(gen_strip([fmap['stats']['l_pixels']+1, hw_chan_length], start, direction, led_spacing))
        start += strip_offset

        for pix_orders in fmap['centre']:
            pixels.extend(gen_strip(pix_orders, start, direction, led_spacing))
            start += strip_offset
        pixels.extend(gen_strip([fmap['stats']['c_pixels']+1, hw_chan_length], start, direction, led_spacing))
        start += strip_offset

        for pix_orders in fmap['right']:
            pixels.extend(gen_strip(pix_orders, start, direction, led_spacing))
            start += strip_offset
        pixels.extend(gen_strip([fmap['stats']['r_pixels']+1, hw_chan_length], start, direction, led_spacing))

        self.pixels_by_channel[int(channel)] = pixels
        # A generic layout that can be used with generic patterns
        self.layout = PixelList(pixels)
        self.animation = SpiralOutFast(self.layout)

def gen_strip(pix_orders, start, direction, led_spacing):
    pixel_count = (pix_orders[1] + 1) - pix_orders[0]
    strip = Strip(start, direction, led_spacing, pixel_count)
    return strip.pixels