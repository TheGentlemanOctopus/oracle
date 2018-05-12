import time
from multiprocessing import Queue

class Device(object):
    """Generic Device"""
    def __init__(self, frame_rate=30):
        self.out_queue = Queue()
        self.frame_rate = frame_rate

    def main(self):
        while True:
            self.put([pixel.color for pixel in self.update()])
            time.sleep(1.0/self.frame_rate)

    def put(self, data):
        # TODO: Make clear function with the following...
        while not self.out_queue.empty():
            self.out_queue.get()

        self.out_queue.put(data)

    def update(self):
        raise NotImplementedError("pls define update")

if __name__ == '__main__':
    device = Device()
    device.main()
    while True:
        print(device.out_queue.get())

        