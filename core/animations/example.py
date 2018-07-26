from animation import Animation

import numpy as np
import time

class Example(Animation):
    layout_type = "Layout"

    def __init__(self, layout, 
        r=.5, 
        g=.5, 
        b=.5, 

    ):
        super(Example, self).__init__()
        self.layout = layout

        self.add_param("r", r, 0, 1)
        self.add_param("g", g, 0, 1)
        self.add_param("b", b, 0, 1)

        self.buff_len = 1500

        print 'LENGTH OF pixels', len(self.layout.pixels)

    def update(self):
        
        r = self.params["r"].value
        g = self.params["g"].value
        b = self.params["b"].value

        

        for i in range(len(self.pixels)):
            self.layout.pixels[i].color = (r, g, b)
