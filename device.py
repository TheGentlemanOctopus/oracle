import time
from multiprocessing import Queue

class Device(object):
    """Generic Device"""
    def __init__(self):
        self.out_queue = Queue()

    def main(self):
        while True:
            self.put(time.time())
            time.sleep(1.0/30)

    def put(self, data):
        # TODO: Make clear function with the following...
        while not self.out_queue.empty():
            self.out_queue.get()

        self.out_queue.put(data)

if __name__ == '__main__':
    device = Device()
    device.main()
    while True:
        print(device.out_queue.get())

        