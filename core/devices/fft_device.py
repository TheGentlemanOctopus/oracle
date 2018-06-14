from input_device import InputDevice
from core.udp.fft_server import FftServer

class FftDevice(InputDevice):
    """
        A wrapper around the hack fft server
        TODO: merge fft_server into this
    """
    def main(self, **fft_server_kwargs):
        fft_server = FftServer(**fft_server_kwargs)

        self.out_queue = fft_server.fft_queue

        fft_server.start()

