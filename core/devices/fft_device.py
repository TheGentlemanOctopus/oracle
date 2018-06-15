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
        self.fft_server = FftServer(self.out_queue, **fft_server_kwargs)

    def main(self):
        self.fft_server.run()

