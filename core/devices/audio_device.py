import csv
import datetime
import time

from device import get_nowait
from input_device import InputDevice
# from core.udp.fft_server import FftServer
from core.udp.udp_server import UdpServer
from core.audioanalysis.beatdetection import BeatDetect
# from core.audioanalysis.server import AudioServer
from core.devices.output_device import fft_message

class AudioDevice(InputDevice):
    """
        A wrapper around the hack fft server
        TODO: merge fft_server into this
    """
    def __init__(self, **fft_server_kwargs):
        super(AudioDevice, self).__init__()


        self.udp_ip = fft_server_kwargs['arduino_ip']
        self.udp_port_rec = fft_server_kwargs['data_port']
        self.udp_port_send = fft_server_kwargs['start_port']
        self.beat_args = fft_server_kwargs['beat_args']


        self.audio_data = []

        # Recording flag
        self.raw_record_file = None
        self.processed_record_file = None
        self.record_start_time = time.time()

    def __del__(self):
        if self.server.connected:
            self.server.disconnect()

    def start_client_stream(self, msg='Start'):
        ''' initiate fft client with start message 
            if no bytes written, loop around and wait 5 seconds 
            before trt'ying again '''
        active = False
        while not active:
            if self.server.send('Start'):
                ''' wait for first data for success '''
                mStr, addr = self.server.receive() 
                if len(mStr) > 0:
                    ''' success '''
                    active = True
                else:
                    active = False
            else:
                print 'Error: no bytes sent'
                return False

            print 'still waiting for fft to send first udp'
            time.sleep(.5)
        return active

    def main(self):
        
        self.server = UdpServer(udp_ip=self.udp_ip, 
                udp_port_rec=self.udp_port_rec, 
                udp_port_send=self.udp_port_send)
        self.server.connect()

        ''' prepare history storage '''
        history_length = 30
        bin_history = [[] for x in xrange(7)]    
        ''' create beat detection object '''
        beat_detectors = [BeatDetect(wait=self.beat_args['wait'], threshold=self.beat_args['threshold'], history=history_length) for x in xrange(7)]


        active = False
        while self.server.connected:
            time.sleep(5)

            
            print 'sending Start'
            if self.start_client_stream('Start'):
                active = True

                ''' populate history '''
                while (len(bin_history[0]) < history_length):
                    ''' get data '''
                    mStr, addr = self.server.receive() # buffer size is 1024 bytes
                    data = [int(e) if e.isdigit() else e for e in mStr.split(',')]
                    for x in xrange(7):
                        bin_history[x].append(data[x])

                while active:

                    mStr, addr = self.server.receive() # buffer size is 1024 bytes

                    if len(mStr) > 0:
                        
                        fft_data = [int(e) if e.isdigit() else e for e in mStr.split(',')]
                        
                        beat_data = []
                        for x in xrange(7):
                            bin_history[x].pop(0)
                            bin_history[x].append(fft_data[x])
                            beat_data.append(
                                beat_detectors[x].detect(bin_history[x][:])
                                )

                        print fft_data+beat_data
                        self.data_out(["processed", fft_data+beat_data])
                    else:
                        print 'No data read from UDP, misread count:', self.server.misread_count
                        if self.server.misread_count > 1:
                            active = False
                        


            else:
                print 'is socket connected properly?'
            


            
            




    def data_out(self, data):
        self.out_queue.put(data)

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
            print type(item), len(item), item
            print 'fuck'
            return

        msg_type, msg = item

        # Process Message
        if msg_type=="raw":
            self.record_raw(msg)

        elif msg_type=="processed":
            self.record_processed(msg)
            ''' TODO: ammend for the context of beats '''
            return fft_message([band/1024.0 for band in msg])

