from animation import Animation
import utils

import time
import random
import itertools
import numpy as np

default_animation_set = [
    {"type": "LavaLamp"},
    {"type": "SwoopyTown"},
    {"type": "SpiralOutFast"}
]

class Carousel(Animation):
    # TODO: only works on generic animations atm
    layout_type="Layout"

    def __init__(self, layout, 
        animations=default_animation_set, 
        min_transition_time=30,
        max_transition_time=200
    ):
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

        self.add_param("min_transition_time", min_transition_time, 1, 200)
        self.add_param("max_transition_time", max_transition_time, 1, 300)

        self.next_switch = time.time() + self.generate_switch_time()

        self.animation_dict = utils.possible_animations(layout.__class__.__name__)
        if "Carousel" in self.animation_dict:
            del self.animation_dict["Carousel"]

        # round-and-round-and-round-and-round-and-round-and-round
        self.animations = itertools.cycle(animations)

        # Make sure all animations are constructable to avoid disappointment later
        self.current_animation = Animation()
        for i in animations:
            self.next_animation()

        # Set first animation as current
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

    def generate_switch_time(self):
        mini, maxi = sorted([
            self.params["min_transition_time"].value,
            self.params["max_transition_time"].value
        ]) 

        return mini + random.random()*(maxi - mini)

    def update(self):
        """
            Update-o
        """
        if time.time() > self.next_switch:
            self.next_switch += self.generate_switch_time()
            self.next_animation()

        # Update
        self.current_animation.fft = self.fft
        self.current_animation.update()
