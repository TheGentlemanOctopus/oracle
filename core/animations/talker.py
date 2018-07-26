from animation import Animation

import numpy as np
import time

class Talker(Animation):
    layout_type = "Layout"

    end = 30
    pixel_its = [0,0,0]
    pixel_it = 0
    beats = [0]*7

    def __init__(self, layout, 
        r=1.0, 
        g=0.0, 
        b=0.0, 

    ):
        super(Talker, self).__init__()
        self.layout = layout

        self.add_param("r", r, 0, 1)
        self.add_param("g", g, 0, 1)
        self.add_param("b", b, 0, 1)

        self.buff_len = 1500

        print 'LENGTH OF pixels', len(self.layout.pixels)

        self.clear_pixels()

    def clear_pixels(self):
        for i in range(len(self.pixels)):
            self.layout.pixels[i].color = (0, 0, 0)

    def update(self):
        ''' TODO: create mid frame beat polling & toggle beat state 
        between frames so that only one beat per frame can happen '''
        
        r = self.params["r"].value
        g = self.params["g"].value
        b = self.params["b"].value

        self.clear_pixels()
        for x in xrange(3):

            if self.check_beat(ch_range=[x,x+1]):
                self.pixel_its[x] = (self.pixel_its[x]+1)%30
            self.layout.pixels[self.pixel_its[x]].color = (self.fft[x], self.fft[x+2], self.fft[x+1])    
                

       
        

    def check_beat(self, ch_range=[0,3]):
        if sum(self.fft[7+ch_range[0]:7+ch_range[1]]) > 0:
            return True
        else:
            return False