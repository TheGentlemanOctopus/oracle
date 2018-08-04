from animation import Animation
from core.utilities import logging_handler_setup
from panel_utils import fmap

from scipy import signal
import numpy as np
import time
import random

import colorsys



class FaceSection():



    def __init__(self, length=10,section='left'):


        self.length = length
        self.section = section


        self.cycle_start = time.time()

        self.temp_pixels = np.array([[0.0,0.0,0.0]]*self.length)

        self.logger = logging_handler_setup('face section - %s'%self.section)
        self.fire_waves = []
        self.fire_decay_time = []
        self.fire_decay_time_delta = []

        self.fire_reset_time = []
        self.fire_reset_time_delta = []
        for panel_index in range(len(fmap[self.section])):
            self.fire_waves.append(0.0) 
            self.fire_decay_time.append(0)
            self.fire_decay_time_delta.append(0)

            self.fire_reset_time.append(0)
            self.fire_reset_time_delta.append(0)
            
    def update(self, fft, reset_time, decay_time):

        if self.check_beat(fft[8:10]):
        
            panel_count = 0
            while True:
                panel_it = random.randint(0,len(fmap[self.section])-1)
                if self.fire_reset_time_delta[panel_it] > reset_time:
                    self.fire_waves[panel_it] = 0.5
                    self.fire_reset_time[panel_it] = time.time()
                    break
                else:
                    panel_count = panel_count+1
                    if panel_count > len(fmap[self.section])-1:
                        break





        for panel_index, panel in enumerate(fmap[self.section]):

            for x in xrange(panel[0],panel[1]+1):
                
                rh = np.sin(2*np.pi*self.fire_reset_time_delta[panel_index]*x) % 0.15
                # print rh
                rs = 1
                rv = np.sin(2*np.pi*self.fire_waves[panel_index]*x)
                

                # yh = 0.1
                # ys = 1
                # yv = np.sin(2*np.pi*self.fire_waves[panel_index]*(x+5))
                

                # print(h,s,v)

                self.temp_pixels[x] = (np.array(colorsys.hsv_to_rgb(rh,rs,rv)))# + (np.array(colorsys.hsv_to_rgb(yh,ys,yv)))

            
            self.fire_reset_time_delta[panel_index] = time.time() - self.fire_reset_time[panel_index]
            self.fire_decay_time_delta[panel_index] = time.time() - self.fire_decay_time[panel_index]
            
            if self.fire_decay_time_delta[panel_index] > decay_time:
                self.fire_waves[panel_index] = self.fire_waves[panel_index] * 0.9
                self.fire_decay_time[panel_index] = time.time()
        # self.temp_pixels = self.decay_pixels()
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

 

class FireGlow(Animation):
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
        super(FireGlow, self).__init__()
        self.layout = layout

        strip_length =512

        self.add_param("r", r, 0, 1)
        self.add_param("g", g, 0, 1)
        self.add_param("b", b, 0, 1)
        # self.add_param("fire_decay", fire_decay, 0, 10)
        
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
        fire_reset = 2
        fire_decay = 0.01


        self.clear_pixels()
        
        period = 5 #- ((1.01-fft[1])*3)
        t_delta = time.time()-self.cycle_start
        if t_delta > period:
            self.cycle_start = time.time()

        t_phase = t_delta / period

        self.carrier = np.sin(t_phase)
        for old_pix, new_pix in zip(self.layout.pixels[0:fmap['stats']['l_pixels']], self.left.update(self.fft, fire_reset, fire_decay)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[512:512+fmap['stats']['c_pixels']], self.centre.update(self.fft, fire_reset, fire_decay)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[1024:1024+fmap['stats']['r_pixels']], self.right.update(self.fft, fire_reset, fire_decay)):
            old_pix.color = new_pix

    
