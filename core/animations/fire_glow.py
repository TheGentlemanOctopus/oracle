from animation import Animation
from core.utilities import logging_handler_setup
from panel_utils import fmap, spatial_fmap

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

        self.panel_on = []

        for panel_index in range(len(spatial_fmap[self.section])):
            self.fire_waves.append(0.0) 
            self.fire_decay_time.append(0)
            self.fire_decay_time_delta.append(0)

            self.fire_reset_time.append(0)
            self.fire_reset_time_delta.append(0)

            self.panel_on.append(False)

        self.time_start = 0
        self.time_delta = 0
        self.time_period = 0
            
    def update(self, fft, reset_time, decay_time, colour_time):

        self.time_delta = time.time() - self.time_start
        self.time_period = (np.sin(self.time_delta/colour_time) + 1) * 0.425
        # print self.time_period



        if self.check_beat(fft[7:11]):
        
            panel_count = 0


            for panel_it in range(len(spatial_fmap[self.section])):
                
                if self.fire_reset_time_delta[panel_it] > reset_time:
                    self.panel_on[panel_it] = False

                if self.panel_on[panel_it] == False:
                    self.fire_waves[panel_it] = 0.7
                    self.fire_reset_time[panel_it] = time.time()
                    self.panel_on[panel_it] = True
                    break   



        for panel_index, panel in enumerate(spatial_fmap[self.section]):
            pixel_length = panel[1]+1-panel[0]
            for x in xrange(panel[0],panel[1]+1):
                x_duty = (float(x-panel[0])*self.fire_waves[panel_index])/float(pixel_length)
                rh = (np.sin(x) % 0.15) + self.time_period
                rs = 1.0
                rv = np.sin(x_duty*self.fire_decay_time[panel_index])%1
                self.temp_pixels[x] = (np.array(colorsys.hsv_to_rgb(rh,rs,rv)))

            
            self.fire_reset_time_delta[panel_index] = time.time() - self.fire_reset_time[panel_index]
            self.fire_decay_time_delta[panel_index] = time.time() - self.fire_decay_time[panel_index]
            
            if self.fire_decay_time_delta[panel_index] > decay_time:
                self.fire_waves[panel_index] = self.fire_waves[panel_index]*0.5
                self.fire_decay_time[panel_index] = time.time()
            


        return self.temp_pixels

        
    def decay(self, data):
        i = np.vectorize(self.add_random)
        return i(data,-.05,0.0)

        
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
        fire_reset = 2,
        fire_decay = 0.05,
        colour_time = 5
    ):
        super(FireGlow, self).__init__()
        self.layout = layout

        strip_length =512

        self.add_param("fire_reset", fire_reset, 0.001, 10)
        self.add_param("fire_decay", fire_decay, 0.001, 0.5)
        self.add_param("colour_time", colour_time, 0.001, 10)
        
        self.left = FaceSection(length=fmap['stats']['l_pixels'],section='left')
        self.centre = FaceSection(length=fmap['stats']['c_pixels'],section='centre')
        self.right = FaceSection(length=fmap['stats']['r_pixels'],section='right')
        self.cube = FaceSection(length=fmap['stats']['cube_pixels'],section='cube')
        self.cycle_start = time.time()

    def clear_pixels(self):
        for i in range(len(self.pixels)):
            self.layout.pixels[i].color = (0, 0, 0)

    def update(self):
        ''' TODO: create mid frame beat polling & toggle beat state 
        between frames so that only one beat per frame can happen '''
        
        fire_reset = self.params["fire_reset"].value
        fire_decay = self.params["fire_decay"].value
        colour_time = self.params["colour_time"].value

        self.clear_pixels()
        
        period = 5 #- ((1.01-fft[1])*3)
        t_delta = time.time()-self.cycle_start
        if t_delta > period:
            self.cycle_start = time.time()

        t_phase = t_delta / period

        self.carrier = np.sin(t_phase)
        for old_pix, new_pix in zip(self.layout.pixels[0:fmap['stats']['l_pixels']], self.left.update(self.fft, fire_reset, fire_decay, colour_time)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[512:512+fmap['stats']['c_pixels']], self.centre.update(self.fft, fire_reset, fire_decay, colour_time)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[1024:1024+fmap['stats']['r_pixels']], self.right.update(self.fft, fire_reset, fire_decay, colour_time)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[1536:1536+fmap['stats']['cube_pixels']], self.cube.update(self.fft, fire_reset, fire_decay, colour_time)):
            old_pix.color = new_pix
    
