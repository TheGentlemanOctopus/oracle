import colorsys

class Pixel(object):
    """
        Pixel object holds location and color data
        TODO: Move this out of the device module?

        r,g,b values are stored between 0->1 because that makes math easier
    """
    def __init__(self, location, r=0, g=0, b=0):
        self.location = tuple(location)

        self.r = r
        self.g = g
        self.b = b

    @property
    def color(self):
        return (self.r, self.g, self.b)

    @color.setter
    def color(self, c):
        if len(c)!=3:
            raise Exception("Need 3 values to set color")

        self.r = c[0]
        self.g = c[1]
        self.b = c[2]

    @property
    def color_255(self):
        """
            tuple scaled for 8-bit
        """
        return (int(255*self.r), int(255*self.g), int(255*self.b))

    def set_hsv(self, h, s, v):
        """
            Sets pixel color given hsv values in range 0->1
        """ 
        self.r, self.g, self.b = colorsys.hsv_to_rgb(h,s,v)