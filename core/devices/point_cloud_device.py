import numpy as np

from output_device import OutputDevice
from pixel import Pixel

from core.layouts.pixel_list import PixelList
from core.animations.spiral_out_fast import SpiralOutFast
import core.point_clouds as point_clouds

import json

class PointCloudDevice(OutputDevice):
    """
        A generic device that is just a list of points
    """
    def __init__(self, channel, pixels=None):
        super(PointCloudDevice, self).__init__()


        pixel_list = None

        # A direct list of pixels
        if isinstance(pixels, list):
            pixel_list = pixels
        
        # A path
        elif isinstance(pixels, basestring):

            # Load from file
            with open(point_clouds.path+pixels) as f:
                data = json.load(f)

            pixel_list = []
            for point in data:
                pixel_list.append(Pixel(point["point"]))

        else:
            raise Exception("pixels must be list or a string (that indicates filepath relative to /core/point_clouds/)")

        self.pixels_by_channel = {channel: pixel_list}
        self.layout = PixelList(pixel_list)
        self.animation = SpiralOutFast(self.layout)

