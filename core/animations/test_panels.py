from animation import Animation
from core.utilities import logging_handler_setup
from scipy import signal
import numpy as np
import time
import random

import colorsys


''' right 8 extra pixel '''

fmap = {
    'stats' : {
        'total_pixels' : 1025,
        'r_pixels' : 319,
        'c_pixels' : 386,
        'l_pixels' : 320
    },
    'right' : [[0,   27],
                [28,  43],
                [44,  65],
                [66,  81],
                [82,  91],
                [92,  111],
                [112, 135],
                [136, 152],
                [153, 165],
                [166, 191],
                [192, 214],
                [215, 240],
                [241, 263],
                [264, 298],
                [299, 318]],
    'centre' : [[0,   27],
                [28,  53],
                [54,  66],
                [67,  80],
                [81,  89],
                [90,  102],
                [103, 128],
                [129, 155],
                [156, 224],
                [225, 241],
                [242, 272],
                [273, 289],
                [290, 318],
                [319, 338],
                [339, 355],
                [356, 385]],
    'left'  :   [[0,   27],
                [28,  43],
                [44,  65],
                [66,  81],
                [82,  91],
                [92,  111],
                [112, 136],
                [137, 153],
                [154, 166],
                [167, 192],
                [193, 215],
                [216, 241],
                [242, 264],
                [265, 299],
                [300, 319]]
}



class FaceSection():

    modes = ['blank','fill','burst','ripple','fade','vu']
    mode = 'blank'

    def __init__(self, length=10):


        self.length = length


        self.master_col = [0.5,0.5,0.5]
        self.target_master_col = [0.5,0.5,0.5]

        self.ramp_up = 1.0
        self.ramp_down = 1.0

        self.period = 50.0 # second
        self.width = 0.5

        self.cycle_start = time.time()

        self.temp_pixels = np.array([[0.0,0.0,0.0]]*self.length)

        self.logger = logging_handler_setup('face section')

    def update(self, *args):


        t_delta = time.time()-self.cycle_start
        if t_delta > self.period:
            self.cycle_start = time.time()

        t_phase_b = t_delta / self.period
        carrier = np.sin(t_phase_b)

        if self.check_beat(args[0][8:10]):
            # self.logger.debug('new panel')
            panel_it = random.randint(0,len(fmap['left'])-1)
            h = random.uniform(carrier-.1, carrier+.1)

            for x in xrange(fmap['left'][panel_it][0],fmap['left'][panel_it][1]+1):
                self.temp_pixels[x] = colorsys.hsv_to_rgb(h,.9,.9)

                # self.pixels[x+self.start].set_hsv(h,0.9,.9)

        # print 'before decay', self.temp_pixels
        self.temp_pixels = self.decay_pixels()
        # print 'after decay', self.temp_pixels
        return self.temp_pixels
        
    def decay_pixels(self):
        i = np.vectorize(self.add_random)
        return i(self.temp_pixels,-.01,0.0)
        
    def add_random(self,x,lower,upper):
        return x + random.uniform(lower,upper)

    def check_beat(self, beats):
        if sum(beats) > 0:
            return True
        else:
            return False

 

class TestPanels(Animation):
    layout_type = "Layout"

    end = 30
    pixel_its = [0,0,0]
    pixel_it = 0
    beats = [0]*7

    def __init__(self, layout, 
        r=1.0, 
        g=0.0, 
        b=0.0

    ):
        super(TestPanels, self).__init__()
        self.layout = layout

        strip_length =512

        self.add_param("r", r, 0, 1)
        self.add_param("g", g, 0, 1)
        self.add_param("b", b, 0, 1)
        
        self.left = FaceSection(length=fmap['stats']['l_pixels'])


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
        
        # self.mouth.master_col = [0.0, self.fft[0], 0.0]

        for old_pix, new_pix in zip(self.layout.pixels, self.left.update(self.fft)):
            # print old_pix.color, new_pix
            old_pix.color = new_pix



    

