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

if __name__ == "__main__":
    pixel = Pixel([0,0,0])

    print pixel.color