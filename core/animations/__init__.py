import numpy as np

class Animation(object):
    """
        The animation class can be used to generate a pattern for a device
        The params dict represents 
    """
    self.fft_data = np.zeros([0,0,0,0,0,0,0])

    def __init__(self, **params):
        """
            Params represent high parrern parameters that should be configured when developing a pattern
            E.g hue
        """
        self.params = params

    def process_input(data):
        """
            Represents real time dictionary of data the an animcation may react upon (eg fft data)
        """
        for input_type, value in data.items():
            if input_type=="fft":
                self.fft_data = value

            else:
                # TODO: Log if fft data is not available
                pass
