from core.devices.pixel import Pixel
from strip import Strip
import numpy as np

class Panel:
    """
        Represents a panel of Leds
        Origin is a  two element array (x,y)
        led_spacing/strip_spacing/num_pixels_x/num_strips_y are scalars
    """
    def __init__(self, origin, led_spacing, strip_spacing, num_pixels_x, num_strips_y):

        self.strips = []
        direction = np.array([1,0,0])
        direction_multiplier = np.array([-1,0,0])
        sign = 1

        for i in range(num_strips_y):
            direction = direction * direction_multiplier
            sign = sign * -1


            if(sign == -1):
                strip_translate = np.array([((num_pixels_x -1)  * led_spacing), (i * strip_spacing), 0])

            else:
                strip_translate = np.array([0, (i * strip_spacing), 0])

            start = np.array(origin) + strip_translate  
            print start
            self.strips.append(Strip(start, direction, led_spacing, num_pixels_x))
