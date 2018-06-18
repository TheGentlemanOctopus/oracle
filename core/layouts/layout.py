import numpy as np

class Layout(object):
    """
        At the moment serves nothing more than a placeholder
    """
    def pixels(self):
        """
            This should be overridden so each layout has a generic way to generate a list of pixels
        """
        return np.array([])