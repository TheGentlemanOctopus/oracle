import csv
import datetime
import time

from device import get_nowait
from input_device import InputDevice
# from core.udp.fft_server import FftServer
from core.udp.udp_server import UdpServer
from core.audioanalysis.beat_detection import BeatDetect
# from core.audioanalysis.server import AudioServer
from core.devices.output_device import fft_message
from core.utilities import logging_handler_setup

import numpy as np

class AudioDevice(InputDevice):
    """
        A wrapper around the hack fft server.
        This class creats a udp server for the fft data,
        processes the data through beat detection, then 
        sends a 14 element array in to the queue. Thats
        [0...fft....6,7....beats.....13]
    """
    def __init__(self, **fft_server_kwargs):
        super(AudioDevice, self).__init__()


        self.udp_ip = fft_server_kwargs['arduino_ip']
        self.udp_port_rec = fft_server_kwargs['data_port']
        self.udp_port_send = fft_server_kwargs['start_port']
        self.beat_args = fft_server_kwargs['beat_args']
        self.quiet_timeout = fft_server_kwargs['quiet_timeout']
        self.min_volume = fft_server_kwargs['no_mic_level']
        self.no_sound_frequency = fft_server_kwargs['no_sound_frequency']
        self.sw_gain = fft_server_kwargs['sw_gain']
        self.simulated_sine_amplitude = fft_server_kwargs['simulated_sine_amplitude']

        self.quiet = {
            'too_quiet' : False,
            'elapsed_time' : 0.0,
            'too_quiet_start' : 0.0
        }

        self.audio_data = []

        # Recording flag
        self.raw_record_file = None
        self.processed_record_file = None
        self.record_start_time = time.time()

        self.sine_start = time.time()
        self.beat_it = 0

        self.logger = logging_handler_setup('Audio Device')
        self.logger.info('Init audio device')

    def __del__(self):
        if self.server.connected:
            self.server.disconnect()

    def start_client_stream(self, msg='Start'):
        ''' initiate fft client with start message 
            if no bytes written, loop around and wait 5 seconds 
            before trt'ying again '''
        self.logger.debug('start_client_stream')
        active = False
        while not active:
            self.logger.debug('Sending start command to fft client')
            if self.server.send('Start'):
                ''' wait for first data for success '''
                self.logger.debug('send sucessed')
                mStr, addr = self.server.receive() 
                self.logger.debug('Wait to receive')
                if len(mStr) > 0:
                    ''' success '''
                    self.logger.debug('Wait to receive->success')
                    active = True
                else:
                    self.logger.debug('Wait to receive->fail')
                    active = False
            else:
                self.logger.error('Sending start byte attempted, but failed')
                return False

            self.logger.info("Still waiting for fft to send first udp")
            fft_data, beat_data = self.gen_default_sine(10.0)
            # self.logger.debug("fft data: %s"%str(fft_data+beat_data))
            # print fft_data
            self.data_out(["processed", fft_data+beat_data])
            time.sleep(.5)
        return active

    def main(self):
        self.logger.info('main audio device')
        self.server = UdpServer(udp_ip=self.udp_ip, 
                udp_port_rec=self.udp_port_rec, 
                udp_port_send=self.udp_port_send)
        self.server.connect(timeout=.5)

        ''' prepare history storage '''
        history_length = self.beat_args['history_length']
        bin_history = [[] for x in xrange(7)]    
        ''' create beat detection object '''
        beat_detectors = [BeatDetect(wait=self.beat_args['wait'], threshold=self.beat_args['threshold'], history=history_length) for x in xrange(7)]


        active = False
        while self.server.connected:
            # self.logger.debug('Audio device wait 1 second before sending start byte')
            time.sleep(1)

            
            self.logger.debug('Sending start byte')
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
                        
                        fft_data = [int(e)*self.sw_gain if e.isdigit() else e for e in mStr.split(',')]
                        beat_data = []
                        for x in xrange(7):
                            bin_history[x].pop(0)
                            bin_history[x].append(fft_data[x])
                            beat_data.append(
                                beat_detectors[x].detect(bin_history[x][:])
                                )

                        ''' react according to audio condition '''
                        if self.calc_volume(fft_data) < self.min_volume:
                            if not self.quiet['elapsed_time'] > 0.0:
                                self.quiet['too_quiet_start'] = time.time()
                            
                            self.quiet['elapsed_time'] = time.time()-self.quiet['too_quiet_start']

                            if self.quiet['elapsed_time'] > self.quiet_timeout:
                                ''' go to sine wave '''
                                self.too_quiet = True
                            else:
                                ''' stay with fft '''
                                self.too_quiet = False
                            
                        else:
                            self.quiet['elapsed_time'] = 0.0
                            self.too_quiet = False
                            
                        if self.too_quiet:
                            self.logger.debug("Too quiet")
                            fft_data, beat_data = self.gen_default_sine(120.0)
                        
                        self.data_out(["processed", fft_data+beat_data])


                    else:
                        self.logger.error('No data read from UDP, misread count: %d'%(self.server.misread_count))
                        if self.server.misread_count > 1:
                            active = False
                    

            else:
                self.logger.error('Is socket connected properly?')
                self.logger.info('Sending simulated audio sine wave')  
                msg_fft, msg_beats = self.gen_default_sine(10.0)
                self.data_out(["processed", msg_fft+msg_beats])
 

    def gen_default_sine(self, bpm):
        ''' generates a sine wave (120bpm) with beats
        for when audio data isnt being received '''

        period = 60.0/float(bpm) # 120 bpm = 60 seconds / 120

        t_delta = time.time()-self.sine_start
        beat_data = [1,0,0,0,0,0,0]
        
        if t_delta > period:
            # self.logger.debug('beat ch %d'%self.beat_it )
            self.sine_start = time.time()
            beat_data[self.beat_it] = 1
            self.beat_it = (self.beat_it+1)%7
            # print 'beat @', t_delta

        t_phase = t_delta / period
        vu = int( ( (np.sin(t_phase)+1) /2.0 ) *self.simulated_sine_amplitude)
        levels = [vu,vu,vu,vu,vu,vu,vu]
        return levels, beat_data


    def calc_volume(self,fft_channels):
        # print sum(fft_channels)/len(fft_channels)
        return sum(fft_channels)/len(fft_channels)
            

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
            # for x in xrange(7):
            #     msg[x] = msg[x]/1024.0

            return fft_message([band/1024.0 for band in msg[:7]] + msg[7:])

