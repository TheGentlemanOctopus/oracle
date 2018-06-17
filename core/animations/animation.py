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
        self.fft = np.zeros((7,))

    def add_param(self, name, value):
        """
            Adds a parameter to the dict
            TODO: Add min/max features. Will be useful to avoid acceptions
        """
        self.params[name] = value

    def process_input(self, data):
        """
            Represents real time dictionary of data the an animcation may react upon (eg fft data)
        """
        for input_type, value in data.items():
            if input_type=="fft":
                self.fft = value

            else:
                # TODO: Log if fft data is not available
                pass

    def update(self):
        """
            This method is called to update the pixel colors
        """
        pass
