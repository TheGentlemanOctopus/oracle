import numpy as np

from core.layouts.layout import Layout
from param import Param

from core.utilities import logging_handler_setup

class Animation(object):
    """
        The animation class is used to generate a pattern for an OutputDevice
        The params dict represents high level Params represent
        high level parameters that are configured during development or live
    """

    # Name of the layout class name as a string that the animation should be constructed with
    # "Layout" indicates a generic animation that can operate on any layout
    layout_type = "Layout"

    def __init__(self):
        # Dictionary of parameters, useful for higher level code
        # to be able to retrieve an animation's params
        self.params = {}

        # Initialise _fft var. This should only be get/set from the properties below
        self._fft = np.zeros((14,))

        # This defines the layout used for animation
        self.layout = Layout()
        
        self.name = self.__class__.__name__
        # Make a logger object
        self.logger = logging_handler_setup(self.name)


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

    def add_param(self, name, value, minimum, maximum):
        """
            Adds a parameter to the dict
        """
        self.params[name] = Param(value, minimum, maximum)

    def update(self):
        """
            This method is called to update the pixel colors
        """
        pass

    @property
    def pixels(self):
        return self.layout.pixels

