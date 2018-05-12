class Pixel(object):
    """docstring for Pixel"""
    def __init__(self, location, r=0, g=0, b=0):
        self.location = tuple(location)

        self.r = r
        self.g = g
        self.b = b

    @property
    def color(self):
        return (self.r, self.g, self.b)

    @property
    def color_255(self):
        return (255*self.r, 255*self.g, 255*self.b)
    

if __name__ == "__main__":
    pixel = Pixel([0,0,0])

    print pixel.color