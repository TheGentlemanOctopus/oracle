import csv
import datetime
import time

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

        # Recording flag
        self.record_file = None
        self.record_start_time = time.time()

    def main(self):
        self.fft_server.run()

    def process_in_queue(self):
        """
            Handles instructions for recording
        """
        while True:
            item = self.get_in_queue()
            if item is None:
                break

            if item=="start_record":
                self.start_record()

            elif item=="stop_record":
                self.stop_record()

            else:
                # TODO: log
                pass

    def start_record(self):
        """
            Initialises a file for csv recoding
        """

        # Filename for csv
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        filename = "fft_%s.csv"%now
        self.record_file = open(filename, "w")
        self.record_start_time = time.time()

    def stop_record(self):
        """
            Stops the recording of a csv recording
        """
        if self.record_file is not None:
            self.record_file.close()
            self.record_file = None

    def record(self, fft):
        """
            Records a sample
            Col 1 is time, Cols 2-9 are the fft bands
        """
        if self.record_file is None:
            return

        elapsed = time.time() - self.record_start_time
        csv_data = [elapsed] + fft

        self.record_file.write(",".join([str(x) for x in csv_data]) + "\n")

    def get_out_queue(self):
        """
            No wait by default
            Saves having to do an empty check and safer
        """
        # HACK: This should go in the main loop somehow but fft_server is blocking atm
        self.process_in_queue()

        fft_bands = get_nowait(self.out_queue)

        if fft_bands is not None:
            self.record(fft_bands)
            fft_bands = fft_message([band/1024.0 for band in fft_bands])
        
        return fft_bands
