from animation import Animation
import utils

import time
import itertools
import numpy as np

default_set = [
    {"type": "SwoopyTown"},
    {"type": "SpiralOutFast"}
]

class Carousel(Animation):
    # TODO: only works on generic animations atm
    layout_type="Layout"

    def __init__(self, layout, animations=default_set, transition_time=3):
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

        self.animation_dict = utils.possible_animations(layout.__class__.__name__)
        if "Carousel" in self.animation_dict:
            del self.animation_dict["Carousel"]

        # round-and-round-and-round-and-round-and-round-and-round
        self.animations = itertools.cycle(animations)

        # Make sure all animations are constructable to avoid disappointment later
        self.current_animation = Animation()
        for i in animations:
            self.next_animation()

    def next_animation(self):
        """
            Switches up the animation
        """
        ani_data = self.animations.next()

        if "type" not in ani_data:
            raise Exception("type not defined in one of carousel's animations")
        ani_type = ani_data["type"]

        if ani_data["type"] not in self.animation_dict:
            raise Exception("Unknown or incompatible animation %s"%ani_data["type"])
        args = ani_data["args"] if "args" in ani_data else {}

        # Construct
        self.current_animation = self.animation_dict[ani_type](self.layout, **args)

    def update(self):
        """
            Update-o
        """
        switch_time = self.params["transition_time"].value

        if time.time() > self.next_switch:
            self.next_switch += switch_time
            self.next_animation()

        # Update
        self.current_animation.fft = self.fft
        self.current_animation.update()
