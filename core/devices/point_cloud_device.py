import numpy as np

from output_device import OutputDevice
from pixel import Pixel

from core.layouts.pixel_list import PixelList
from core.animations.diffusion import Diffusion
from core.point_clouds import load_point_cloud

class PointCloudDevice(OutputDevice):
    """
        A generic device that is just a point cloud (list of points)
        pixels can either be a list of pixel objects
        or a string that indicates filepath relative to /core/point_clouds/
    """
    def __init__(self, channel, pixels=None):
        super(PointCloudDevice, self).__init__()

        pixel_list = None

        # list of pixels given directly
        if isinstance(pixels, list):
            pixel_list = pixels
        
        # path to point cloud
        elif isinstance(pixels, basestring):
            pixel_list = load_point_cloud(pixels)

        else:
            raise Exception("pixels must be list or a string (that indicates filepath relative to /core/point_clouds/)")

        # Set her up
        self.pixels_by_channel = {channel: pixel_list}
        self.layout = PixelList(pixel_list)
        self.animation = Diffusion(self.layout)

