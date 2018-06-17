import numpy as np

class Animation(object):
    """
        The animation class is used to generate a pattern for an OutputDevice
        The params dict represents high level Params represent high parameters 
        that are configured during development (or live :)
    """
    def __init__(self):
        # Dictionary of parameters, useful for higher level code
        # to be able to retrieve an animation's params
        self.params = {}

        # An array of fft band intensities from bass to treble
        self._fft = np.zeros((7,))

    @property
    def fft(self):
        """
            FFT is an array of 7 band intensities from bass to treble
        """
        return self._fft

    # This decorator is similar to @property but for setting
    # Ensures fft data is always a np array
    @fft.setter
    def fft(self, value):
        self._fft = np.array(value)

    def add_param(self, name, value):
        """
            Adds a parameter to the dict
            TODO: Add min/max features. Will be useful for avoiding acceptions
        """
        self.params[name] = value

    def update(self):
        """
            This method is called to update the pixel colors
        """
        pass
