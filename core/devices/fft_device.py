from device import get_nowait
from input_device import InputDevice
from core.udp.fft_server import FftServer

from core.devices.output_device import fft_message

class FftDevice(InputDevice):
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

    def get_out_queue(self):
        """
            No wait by default
            Saves having to do an empty check and safer
        """
        fft_bands = get_nowait(self.out_queue)

        if fft_bands is not None:
            fft_bands = fft_message([band/1024.0 for band in fft_bands])
        
        return fft_bands
