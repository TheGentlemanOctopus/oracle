import time
from multiprocessing import Queue, Lock
import numpy as np

from device import Device
from core.utilities.sleep_timer import SleepTimer

from core.animations import animations_by_layout
from core.animations.animation import Animation
from core.layouts.pixel_list import PixelList

class OutputDevice(Device):
    """
        Component of a scene that runs as its own process 
        TODO: abstract for output/input device
    """
    fps = 30
    layout_type = "PixelList"

    def __init__(self):
        """
            This base constructor should be called by every subclass
        """
        super(OutputDevice, self).__init__()

        # A dictionary where the key is the channel (int) and the value is a list of pixel objects
        self.pixels_by_channel = {}

        # The current active animation
        self.layout = PixelList([])
        self.animation = Animation()

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

    def set_animation(self, name, params=None):
        """
            Switches the current animation
            Params is a set of initialisation parameters
        """
        if name not in animations_by_layout:
            # TODO: Log error
            return

        if params is None:
            params = {}

        # Construct new animation
        self.animation = animations_by_layout[name](layout, **params)

    def animations_list(self):
        """
            TODO: Returns a list of possible animations
        """
        pass

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
        """
            Process the entire in queue to update data
            TODO: general support for input types rather than fft data
        """

        # Clear the queue
        while True:
            item = self.get_in_queue()

            if item is None:
                break

            # Pass onto animation
            # TODO: Generalise here
            self.animation.fft = item

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
            Updates the pixel colors. Shoudn't need to be overriden in general
        """
        self.animation.update()


if __name__ == '__main__':
    # TODO: Put this in a unit test or whatever
    device = Device()
    device.frame_rate = 30

    device.main()
    while True:
        print(device.out_queue.get())

        