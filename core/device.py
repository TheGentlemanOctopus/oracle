import time
from multiprocessing import Queue

class Device(object):
    """Generic Device"""
    frame_rate = 30
    out_queue = Queue()
    pixels = []

    def main(self):
        while True:
            self.put([pixel.color_255 for pixel in self.update()])
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
    device.frame_rate = 30

    device.main()
    while True:
        print(device.out_queue.get())

        