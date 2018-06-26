from animation import Animation
import utils

import time
import numpy as np

class Carousel(Animation):
    # TODO: only works on generic animations atm
    layout_type="Layout"

    def __init__(self, layout, animations, transition_time=3):
        """
            THE CAROUSEL
            goes round-and-round-and-round-and-round-and-round-and-round
            animations should be an array with entries:
            {
                type: string,
                args: **kwargs
            }
        """
        super(Carousel, self).__init__()

        self.layout = layout

        self.add_param("transition_time", transition_time, 1, 100)

        self.next_switch = time.time() + transition_time

        self.animation_dict = utils.possible_animations()

        # Make sure animations are constructable to avoid disappointment later
        self.animations = animations
        for ani_data in animations:
            if "name" not in ani_data:
                raise Exception("name not defined in one of carousel's animations")

            if ani_data["name"] not in animation_dict:
                raise Exception("Unknown or incompatible animation %s"%ani_data["name"])
            animation = self.animation_dict[name]

            args = ani_data["args"] if "args" in ani_data else {}

            # Test pattern can be constructed to avoid disappointment later
            animation(layout, **args)

        self.current_animation = Animation()

    def update(self):
        """
            Update-o
        """
        pass