from input_device import InputDevice
from core.udp.fft_server import FftServer

class FftDevice(InputDevice):
    def main(self, **fft_server_kwargs):
        fft_server = FftServer(**fft_server_kwargs)
        fft_server.start()

