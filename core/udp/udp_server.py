import socket


class UdpServer():

    def __init__(self, udp_ip='localhost', udp_port_rec=10000, udp_port_send=10001):

        self.ip = udp_ip
        self.port_r = udp_port_rec
        self.port_s = udp_port_send
        self.connected = False
        self.misread_count = 0


    def connect(self, timeout=10):
        ''' is there a way to detect failed socket binding? '''

        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.bind((self.ip, self.port_r))

        self.sock.settimeout(timeout)

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
        try:
            mStr, addr = self.sock.recvfrom(1024)
            if len(mStr) < 1:
                print 'udp_server, received unsufficient data'
                self.misread_count += 1
            return mStr, addr
        except socket.timeout, e:
            return '',''

        
