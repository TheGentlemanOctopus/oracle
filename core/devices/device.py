import time
from multiprocessing import Queue

class Device(object):
    """Generic Device"""
    frame_rate = 30

    def __init__(self):
        # For sending pixels out
        self.out_queue = Queue()

        # A dictionary where the key is the channel and the value is an array of pixel objects
        self.pixels_by_channel = {}

    def main(self):
        while True:
            self.update()
            self.put(self.pixels_by_channel_255)
            time.sleep(1.0/self.frame_rate)

    @property
    def pixels_by_channel_255(self):
        all_pixels = {}
        for channel, pixel_list in self.pixels_by_channel.items():
            all_pixels[channel] = [pixel.color_255 for pixel in pixel_list]

        return all_pixels

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

        