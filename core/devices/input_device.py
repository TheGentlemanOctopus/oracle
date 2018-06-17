from device import Device

class InputDevice(Device):
    """
        Receives data from an external source (eg an fft chip)
        passing it onto higher level processes by putting it onto its out_queue
    """
    def __init__(self):
        super(InputDevice, self).__init__()
