import time
from multiprocessing import Queue, Lock, Condition
import numpy as np

from device import Device
from core.utilities.sleep_timer import SleepTimer
from core.animations import animations_by_layout, possible_animations
from core.animations.animation import Animation
from core.layouts.layout import Layout
from core.utilities import round_to_exponent

class OutputDevice(Device):
    """
        Component of a scene that runs as its own process 
        TODO: abstract for output/input device
    """
    fps = 30

    def __init__(self):
        """
            This base constructor should be called by every subclass
        """
        super(OutputDevice, self).__init__()

        # A dictionary where the key is the channel (int) and the value is a list of pixel objects
        self.pixels_by_channel = {}

        # The current active animation
        self.layout = Layout()
        self.animation = Animation()
        self.animation_cv = Condition()
        self.animation_queue = Queue()

    def main(self, *args):
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

    def set_animation(self, name, **params):
        """
            Switches the current animation
            Params is a set of initialisation parameters
        """
        poss_animations = self.possible_animations()

        if name not in poss_animations:
            # TODO: Log error
            return

        # Construct new animation
        new_animation = poss_animations[name](self.layout, **params)
        new_animation.fft = self.animation.fft
        self.animation = new_animation

    def possible_animations(self):
        return possible_animations(self.layout.__class__.__name__)

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
            Each item should be a list where first element is the command and second is the args
        """

        # Clear the queue
        while True:
            item = self.get_in_queue()
            # print item
            # Break when finished
            if item is None:
                break

            # Skip over faulty data
            if not isinstance(item, list) or len(item)!=2:
                # TODO: log fault
                continue

            data_type, data = item

            # Process the item
            if data_type == "fft":
                self.animation.fft = data

            elif data_type == "animation":
                # Make sure something is put in queue to avoid deadlock
                try:
                    self.set_animation(data["name"], **data["params"])

                except Exception as e:
                    # TODO: Log
                    pass

                finally:
                    self.animation_queue.put({
                        "name": self.animation.__class__.__name__,
                        "params": [{
                            "name": name,
                            "min": float(param.min),
                            "max": float(param.max),
                            "value": param.value,
                            "step": param.step
                        } for (name, param) in self.animation.params.items()]
                    })

            elif data_type == "param":
                if not isinstance(data, list) or len(data)!=2:
                    # TODO: Log
                    continue

                param_name, param_value = data

                if param_name not in self.animation.params:
                    # TODO: log
                    continue

                self.animation.params[param_name].value = param_value

            else:
                # TODO: log fault
                pass

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

def fft_message(fft):
    """
        forms the message expected in OutputDevice in_queues
        fft should be an array of 7 numbers representing the bands
    """
    return ["fft", fft]

def switch_animation_message(name, **params):
    """
        Used to switch an animation
        params is a dictionary of animation parameters
    """

    return ["animation", {
        "name": name,
        "params": params
    }]

def update_param_message(param_name, value):
    return ["param", [param_name, value]]

if __name__ == '__main__':
    # TODO: Put this in a unit test or whatever
    device = Device()
    device.frame_rate = 30

    device.main()
    while True:
        print(device.out_queue.get())

        