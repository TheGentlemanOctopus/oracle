import csv
import datetime
import time

from core.udp.udp_server import UdpServer

import numpy as np

class PrintFft():
    """
        Prints values read from udp for testing
    """
    def __init__(self, udp_ip='127.0.0.1', udp_port_send=5003, udp_port_rec=5009):
        
        self.udp_ip = udp_ip
        self.udp_port_send = udp_port_send
        self.udp_port_rec = udp_port_rec
        
        self.main()


    def __del__(self):
        if self.server.connected:
            self.server.disconnect()

    def start_client_stream(self, msg='Start'):
        print 'start_client_stream'
        active = False
        while not active:
            print 'Sending start command to fft client'
            if self.server.send('Start'):
                ''' wait for first data for success '''
                print 'send sucessed'
                mStr, addr = self.server.receive() 
                print 'Wait to receive'
                if len(mStr) > 0:
                    ''' success '''
                    print 'Wait to receive->success'
                    active = True
                else:
                    print 'Wait to receive->fail'
                    active = False
            else:
                print 'Sending start byte attempted, but failed'
                return False

            print "Still waiting for fft to send first udp"
            time.sleep(.5)
        return active


    def main(self):
        print 'main audio device'
        self.server = UdpServer(udp_ip=self.udp_ip, 
                udp_port_rec=self.udp_port_rec, 
                udp_port_send=self.udp_port_send)
        self.server.connect(timeout=.5)

        
        active = False
        while self.server.connected:
            time.sleep(1)

            print 'Sending start byte'
            if self.start_client_stream('Start'):

                active = True

                while active:

                    mStr, addr = self.server.receive() # buffer size is 1024 bytes

                    if len(mStr) > 0:
                        
                        fft_data = [int(e) if e.isdigit() else e for e in mStr.split(',')]  
                        
                        print "%-*d %-*d %-*d %-*d %-*d %-*d %-*d" % (5,fft_data[0],5,fft_data[1],5,fft_data[2],5,fft_data[3],5,fft_data[4],5,fft_data[5],5,fft_data[6])

                    else:
                        print 'No data read from UDP, misread count:', self.server.misread_count
                        if self.server.misread_count > 1:
                            active = False
                    
            else:
                print 'Is socket connected properly?'
                
 


if __name__ == '__main__':

    s = PrintFft()

 

