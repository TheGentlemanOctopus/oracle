class Pixel(object):
    """docstring for Pixel"""
    def __init__(self, location, color=None):
        self.location = tuple(location)
        self.color = color if color else [0,0,0]