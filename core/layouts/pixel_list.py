from layout import Layout

class PixelList(Layout):
    """
        A simple generic layout, just a list of pixels
    """
    def __init__(self, pixels):
        """
            pixels is a list of pixel objects
        """
        self.pixels = pixels
