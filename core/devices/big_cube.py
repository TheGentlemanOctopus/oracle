import numpy as np

from device import Device
from core.layouts.strip import Strip

class BigCube(Device):
    """
        Big daddy cube
    """

    def __init__(self, channel, spacing):
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
        ])

        # TODO: Set cube length and orientation
        edge_length = 2

        # An eulerian tour around a cube with two strips per edge
        # Elements are from-to tuples that are indices to vertices array
        route = np.array([(0, 1), (1, 0), (0, 2), (2, 0), (0, 4), (4, 5), (5, 1), (1, 3), (3, 1), (1, 5), (5, 4), (4, 7), (7, 2), (2, 3), (3, 2), (2, 7), (7, 6), (6, 3), (3, 6), (6, 5), (5, 6), (6, 7), (7, 4), (4, 0)])

        # Create strips
        pixels_per_edge = int(float(edge_length)/spacing)
        self.strips = []
        for path in route:
            start = vertices[path[0]]
            end = vertices[path[1]]

            direction = end - start

            self.strips.append(Strip(start, direction, spacing, pixels_per_edge))


        # Form pixels by channel dict
        self.pixels_by_channel = {
            channel: np.concatenate([strip.pixels for strip in self.strips])
        }