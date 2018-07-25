import numpy as np
import time
from multiprocessing import Process, Queue

# import matplotlib.pyplot as plt

from audiostream import Audio
from fft import Fft
# from beatdetection import BeatDetect
import socket

class UdpClient():

    '''
    initialise with your ip 
    start udp on incoming port and listen for messages

    if not connected, wait for message 'Start'

        when received start sending fft over udp
        [63, 160, 400, 1000, 2500, 6250, 16000]

    else read audio

    '''

    def __init__(self, udp_ip='localhost', udp_port_rec=10000, udp_port_send=10001):

        self.ip = udp_ip
        self.port_r = udp_port_rec
        self.port_s = udp_port_send
        self.connected = False
        


    def connect(self, timeout=10):
        start_time = time.time()


        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.ip, self.port_r))


        while not self.connected:
            print 'waiting for server to connect...'
            self.__listen_for_start()
            time.sleep(0.1)
            if (time.time() - start_time) > timeout:
                print 'failed to connect before timeout'
                return False
        return True

    def disconnect(self):
        self.sock.shutdown()
        self.sock.close()

    def __listen_for_start(self):

        data, server = self.sock.recvfrom(1024)
        print server, data

        if len(data) > 0:
            
            ''' compare data message '''
            if(data == 'Start'):
                print 'connected'
                self.connected = True
            return True
        else:
            print 'empty packet received'
            return False


    def send(self, msg):

        result = self.sock.sendto(msg, (self.ip, self.port_s))
        # print result
        if result < len(msg):
            print 'not all bytes sent'
            ''' try again '''
            result = self.sock.sendto(msg, (self.ip, self.port_s))
            if result < len(msg):
                self.connected = False
            return False
        else:
            return True


class FftClient(Process):

    def __init__(self, 
            process_period=0.02,
            udp_ip='localhost', 
            udp_port_rec=10000, 
            udp_port_send=10001,
            datasize=2048,
            frate=44100,
            mode='mic'):
        Process.__init__(self)

        self.process_period = process_period
        self.udp_ip = udp_ip
        self.udp_port_rec = udp_port_rec
        self.udp_port_send = udp_port_send
        self.datasize = datasize
        self.frate = frate
        self.mode = mode
        pass


    def run(self):

        print 'create client'
        client = UdpClient(udp_ip=self.udp_ip, 
                        udp_port_rec=self.udp_port_rec, 
                        udp_port_send=self.udp_port_send)
        client.connect()

        if client.connected:
            print 'client connected'

            ''' 1 - get source '''
            datasize = 2048
            frate = 44100

            self.mode = 'mic'
            if self.mode == 'wav':
                audio = Audio(source={'input':'wav','path':'resources/DaftPunk.wav','datasize':self.datasize},
                        output=True)
            if self.mode == 'mic':
                audio = Audio(source={'input':'mic','datasize':self.datasize, 'rate':self.frate},
                        output=False)

            ''' create fft '''
            fft = Fft(datasize=datasize,frate=frate, gain=10e-4, saturation_point=1024)
            data = audio.sample_and_send()
            fft.configure_fft(data)
            fft.getDominantF()
            fft.splitLevels()     
            fft.normalize_bin_values()

            last_tick = time.time()

            while True:

                ''' wait until next cycle '''
                if (time.time() - last_tick) > self.process_period:
                    last_tick = time.time()

                    data = audio.sample_and_send()
                    fft.run_fft(data)
                    fft.getDominantF()
                    fft.splitLevels()     
                    # fft.set_freq_bins_max()
                    fft.normalize_bin_values()

                    msg = ','.join([str(i) for i in fft.stats['bin_values_normalized']])
                    print msg
                    if not client.send(msg):
                        ''' wait for reconnect '''
                else:
                    time.sleep(.0001)

        else:
            print 'client not connected'


        client.disconnect()

if __name__ == '__main__':

    c = FftClient(process_period=0.02,
            udp_ip='localhost', 
            udp_port_rec=5003, 
            udp_port_send=5009,
            datasize=2048,
            frate=44100,
            mode='mic')

    c.daemon = True
    c.start()

    while True:
        time.sleep(1)
        pass


