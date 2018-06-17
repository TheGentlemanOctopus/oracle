import numpy as np

class Animation(object):
    """
        The animation class can be used to generate a pattern for a device
        The params dict represents 
    """
    def __init__(self):
        """
            Params represent high parrern parameters that should be configured when developing a pattern
            E.g hue
        """
        self.params = {}

        # An array of fft band intensities from bass to treble
        self._fft = np.zeros((7,))

    @property
    def fft(self):
        """I'm the 'x' property."""
        return self._fft

    # This decorator is similar to @property but for setting
    # Ensures fft data is always a np array
    @fft.setter
    def fft(self, value):
        self._fft = np.array(value)

    def add_param(self, name, value):
        """
            Adds a parameter to the dict
            TODO: Add min/max features. Will be useful to avoid acceptions
        """
        self.params[name] = value

    def update(self):
        """
            This method is called to update the pixel colors
        """
        pass
