import time
from multiprocessing import Queue, Lock
from core.utilities.sleep_timer import SleepTimer

class Device(object):
    """
        Component of a scene that runs as its own process 
        TODO: abstract for output/input device
    """
    fps = 30

    def __init__(self):
        """
            This base constructor should be called by every subclass
        """
        # Output queue
        self.out_queue = Queue()

        # Input Queue
        self.in_queue = Queue()

        # Mutex for the queues
        self.queue_mutex = Lock()

        # A dictionary where the key is the channel (int) and the value is a list of pixel objects
        self.pixels_by_channel = {}

    def main(self):
        """
            This should be called to start the process
        """
        sleep_timer = SleepTimer(1.0/self.fps)
        while True:
            sleep_timer.start()

            self.process_in_queue()
            self.update()
            self.put(self.pixel_colors_by_channel_255)

            sleep_timer.sleep()

    @property
    def pixel_colors_by_channel_255(self):
        """
            same as pixels_by_channel but with pixel colors only scaled to an 8-bit range
        """
        all_pixels = {}
        for channel, pixel_list in self.pixels_by_channel.items():
            all_pixels[channel] = [pixel.color_255 for pixel in pixel_list]

        return all_pixels

    def process_in_queue(self):
        while not self.in_queue.empty():
            item = self.in_queue.get()
            
            # TODO

    def put(self, data):
        """
            Clears output queue and appends data
        """
        # Get the mutex
        with self.queue_mutex:
            while not self.out_queue.empty():
                self.out_queue.get()

            self.out_queue.put(data)

    def update(self):
        """
            Updates the pixel colors, should be defined by subclasses          
        """
        raise NotImplementedError("pls define update")


if __name__ == '__main__':
    # TODO: Put this in a unit test or whatever
    device = Device()
    device.frame_rate = 30

    device.main()
    while True:
        print(device.out_queue.get())

        