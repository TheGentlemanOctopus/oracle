from device import Device
from core.udp.fft_server import FftServer

class FftDevice(Device):
    """
        A wrapper around the hack fft server
        TODO: merge fft_server into this
    """
    def __init__(self, **fft_server_kwargs):
        super(FftDevice, self).__init__()

        # Wrap it up!
        self.fft_server = FftServer(**fft_server_kwargs)
        self.fft_server.fft_queue = self.out_queue

    def main(self):
        self.fft_server.start()
        print "STARTED fft server"

