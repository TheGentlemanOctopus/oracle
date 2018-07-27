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
        self.raw_record_file = None
        self.processed_record_file = None
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
        self.raw_record_file = open("raw_"+filename, "w")
        self.processed_record_file = open("processed_"+filename, "w")

        self.record_start_time = time.time()

    def stop_record(self):
        """
            Stops the recording of a csv recording
        """
        if self.raw_record_file is not None:
            self.raw_record_file.close()
            self.raw_record_file = None

        if self.processed_record_file is not None:
            self.processed_record_file.close()
            self.processed_record_file = None

    @property
    def elapsed(self):
        """
            Returns elapsed time of fft recording
        """
        return time.time() - self.record_start_time

    def record_processed(self, fft):
        """
            Records a sample
            Col 1 is time, Cols 2-9 are the fft bands
        """
        if self.processed_record_file is None:
            return

        csv_data = [self.elapsed] + fft

        self.processed_record_file.write(",".join([str(x) for x in csv_data]) + "\n")

    def record_raw(self, message):
        """
            Writes the line in format [elasped time, ",", message]
        """
        if self.raw_record_file is None:
            return

        csv_data = [self.elapsed, message]
        self.raw_record_file.write(",".join([str(x) for x in csv_data]) + "\n")

    def get_out_queue(self):
        """
            No wait by default
            Saves having to do an empty check and safer
        """
        # HACK: This should go in the main loop somehow but fft_server is blocking atm
        self.process_in_queue()

        item = get_nowait(self.out_queue)

        # Empty queue check
        if item is None:
            return

        # Item format check
        if not isinstance(item, list) or len(item)!=2:
            #TODO: log
            return

        msg_type, msg = item

        # Process Message
        if msg_type=="raw":
            self.record_raw(msg)

        elif msg_type=="processed":
            self.record_processed(msg)
            return fft_message([band/1024.0 for band in msg])

