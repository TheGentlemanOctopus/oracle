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



    def __init__(self, length=10,section='left'):


        self.length = length
        self.section = section


        self.cycle_start = time.time()

        self.temp_pixels = np.array([[0.0,0.0,0.0]]*self.length)

        self.logger = logging_handler_setup('face section - %s'%self.section)

        

    def update(self, fft, carrier):

        if self.check_beat(fft[8:10]):
            panel_it = random.randint(0,len(fmap[self.section])-1)
            h = random.uniform(carrier-.1, carrier+.1)

            for x in xrange(fmap[self.section][panel_it][0],fmap[self.section][panel_it][1]+1):
                self.temp_pixels[x] = colorsys.hsv_to_rgb(h,.9,.9)

        self.temp_pixels = self.decay_pixels()
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

 

class PanelBeat(Animation):
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
        super(PanelBeat, self).__init__()
        self.layout = layout

        strip_length =512

        self.add_param("r", r, 0, 1)
        self.add_param("g", g, 0, 1)
        self.add_param("b", b, 0, 1)
        
        self.left = FaceSection(length=fmap['stats']['l_pixels'],section='left')
        self.centre = FaceSection(length=fmap['stats']['c_pixels'],section='centre')
        self.right = FaceSection(length=fmap['stats']['r_pixels'],section='right')
        self.cycle_start = time.time()

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
        
        period = 50 #- ((1.01-fft[1])*3)
        t_delta = time.time()-self.cycle_start
        if t_delta > period:
            self.cycle_start = time.time()

        t_phase = t_delta / period

        self.carrier = np.sin(t_phase)

        for old_pix, new_pix in zip(self.layout.pixels[0:fmap['stats']['l_pixels']], self.left.update(self.fft, self.carrier)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[512:512+fmap['stats']['c_pixels']], self.centre.update(self.fft, self.carrier)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[1024:1024+fmap['stats']['r_pixels']], self.right.update(self.fft, self.carrier)):
            old_pix.color = new_pix


        t = np.linspace(0, 1, 512*3)
        sig = np.sin(2 * np.pi * (t+(t_phase*5)))
        i = signal.square((2 * np.pi * 25 * (t-(t_phase*5))), duty=(sig+1)/2)
        i+=1
        i/2

        bass_factor = np.power((self.fft[4]*10),3) / 1000.0

        # for x in xrange(len(i)):
        #     if i[x] > .8:
        #         # r = colorsys.hsv_to_rgb((self.carrier+(self.fft[0]/2.))%1.0,1.0,1.0)
        #         r = colorsys.hsv_to_rgb((self.carrier+(.2))%1.0,1.0,1.0)
        #         p = [(c[0]+c[1])/2.0 for c in zip(r,self.pixels[x].color)]
        #         self.pixels[x].color = p

    

