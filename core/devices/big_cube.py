import numpy as np

from device import Device
from core.layouts.strip import Strip
import colorsys
import time

class BigCube(Device):
    """
        Big daddy cube
    """

    def __init__(self, channel, led_spacing, strip_spacing):
        super(BigCube, self).__init__()

        # The vertices of the cube
        vertices = np.array([
            (1, -1, -1),
            (1, 1, -1),
            (-1, -1, -1),
            (-1, 1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, -1, 1)
        ]).astype(float)

        # TODO: Set cube length and orientation
        edge_length = 2

        # An eulerian tour around a cube with two strips per edge
        # Elements are from-to tuples that map to indices in the vertices array
        route = np.array([(0, 1), (1, 0), (0, 2), (2, 0), (0, 4), (4, 5), (5, 1), (1, 3), (3, 1), (1, 5), (5, 4), (4, 7), (7, 2), (2, 3), (3, 2), (2, 7), (7, 6), (6, 3), (3, 6), (6, 5), (5, 6), (6, 7), (7, 4), (4, 0)])

        # Create strips in the order they should be laid
        pixels_per_edge = int(float(edge_length)/led_spacing)
        self.strips = []
        for path in route:
            start = vertices[path[0]]
            end = vertices[path[1]]

            # A hacky(ish) way to offset strips so they are not on top of each other
            sign = 1 if path[0] > path[1] else -1
            offset = 0.5*strip_spacing*sign
            start += offset
            end += offset

            direction = end - start

            self.strips.append(Strip(start, direction, led_spacing, pixels_per_edge))


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
        return np.concatenate([strip.pixels for strip in self.strips])
    
    def update(self, period=5):
        # Period is the number of seconds it takes a color to lap the cube
        # TODO: Move period when we have pattern gen capabailities
        pixels = self.pixels

        # Shift pixel ordering according to period phase
        shift = int(len(pixels)*(time.time() % period)/period)
        pixels = np.concatenate([pixels[shift:], pixels[:shift]])

        # One lap of the color wheel in the order
        s = 1 # Saturation
        v = 1 # Value
        for i, h in enumerate(np.linspace(0, 1, len(pixels))):
            pixel = pixels[i]

            pixel.r, pixel.g, pixel.b = colorsys.hsv_to_rgb(h,s,v)



