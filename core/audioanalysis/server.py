from multiprocessing import Process, Queue, Lock
from core.audioanalysis.beatdetection import BeatDetect
import time
import socket

class UdpServer():

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

        self.connected = True

        return True

    def disconnect(self):
        self.sock.shutdown()
        self.sock.close()

    def send(self, msg):

        result = self.sock.sendto(msg, (self.ip, self.port_s))
        if result < len(msg):
            print 'not all bytes sent'
            self.connected = False
            return False
        else:
            return True

    def receive(self):
        mStr, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
        return mStr, addr



class AudioServer(Process):
    ''' This calls UdpServer then applies processing (currently beatdetection) on 
    the data stream. 

    The output is FFT & beat [fft0...fft6 beat0...beat6]
    '''
    def __init__(self, *beat_args, udp_ip='localhost', udp_port_rec=10000, udp_port_send=10001):
        Process.__init__(self)

        self.udp_ip = udp_ip
        self.udp_port_rec = udp_port_rec
        self.udp_port_send = udp_port_send
        self.beat_args = beat_args

        self.out_queue = Queue()
        self.audio_data = []

        pass

    def get_queue(self):
        return self.out_queue

    def data_out(self, data):
        self.out_queue.put(data)

    def run(self):

        self.server = UdpServer(udp_ip=self.udp_ip, 
                udp_port_rec=self.udp_port_rec, 
                udp_port_send=self.udp_port_send)
        self.server.connect()

        if self.server.connected:
            time.sleep(5)
            result = self.server.send('Start')

            history_length = 30
            bin_history = [[] for x in xrange(7)]    
            
            beat_detectors = [BeatDetect(wait=self.beat_args['wait'], threshold=self.beat_args['threshold'], history=history_length) for x in xrange(7)]

            
            ''' populate history '''
            while (len(bin_history[0]) < history_length):
                ''' get data '''

                mStr, addr = self.server.receive() # buffer size is 1024 bytes
                data = [int(e) if e.isdigit() else e for e in mStr.split(',')]
                # print "received message:", data, len(data), type(data)
                for x in xrange(7):
                    bin_history[x].append(data[x])


            while True:

                ''' get data '''
                mStr, addr = self.server.receive() # buffer size is 1024 bytes
                fft_data = [int(e) if e.isdigit() else e for e in mStr.split(',')]
                
                beat_data = []
                for x in xrange(7):
                    bin_history[x].pop(0)
                    bin_history[x].append(fft_data[x])
                    beat_data.append(
                        beat_detectors[x].detect(bin_history[x][:])
                        )
                self.data_out(fft_data+beat_data)



if __name__ == '__main__':

    s = AudioServer(
            udp_ip='localhost', 
            udp_port_rec=10001, 
            udp_port_send=10000,
            )

    audio_queue = s.out_queue

    s.daemon = True
    s.start()


    beat_t = time.time()
    while True:
        ''' read queue from server '''
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            # print 'audio data =>', audio_data
            if audio_data[7] > 0:
                now = time.time()
                dif = now - beat_t
                print dif
                beat_t = now
                print '********\n** BOOM **\n********', audio_data
            else:
                # print '.'
                pass
        time.sleep(0.00001)
        pass

    # '''