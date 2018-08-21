from animation import Animation
from core.utilities import logging_handler_setup
from panel_utils import fmap
from scipy import signal


import numpy as np
import time
import colorsys 
import random

class FaceSection():

    def __init__(self, length=10,section='left'):
        self.length = length
        self.section = section

        self.cycle_start = time.time()
        self.temp_pixels = np.array([[0.0,0.0,0.0]]*self.length)
        self.logger = logging_handler_setup('face section - %s'%self.section)
       

    def update(self, fft, carrier, hue):
        print fmap['centre'][8][0],fmap['centre'][9][1]+1
        for x in xrange(fmap['centre'][8][0],fmap['centre'][9][1]+1):
            self.temp_pixels[x] = colorsys.hsv_to_rgb(.5,1.0,fft[3])

        return self.temp
        
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



class Centre(FaceSection):

    def __init__(self, length,section='centre'):
        FaceSection.__init__(self,length,section=section)

    def update(self, fft, hue):
        for x in xrange(fmap[self.section][8][0],fmap[self.section][8][1]+1):
            self.temp_pixels[x] = colorsys.hsv_to_rgb(hue,1.0,sum(fft)/7.0)
        for x in xrange(fmap[self.section][10][0],fmap[self.section][10][1]+1):
            self.temp_pixels[x] = colorsys.hsv_to_rgb(hue,1.0,sum(fft)/7.0)
        return self.temp_pixels

class Side(FaceSection):

    def __init__(self, length,section='left'):
        FaceSection.__init__(self,length,section=section)

    def update(self, fft, hue):
        for x in xrange(fmap[self.section][1][0],fmap[self.section][5][1]+1):
            self.temp_pixels[x] = colorsys.hsv_to_rgb(hue,1.0,sum(fft)/7.0)
        for x in xrange(fmap[self.section][8][0],fmap[self.section][8][1]+1):
            self.temp_pixels[x] = colorsys.hsv_to_rgb(hue,1.0,sum(fft)/7.0)
        
        return self.temp_pixels

        

class Talker(Animation):
    layout_type = "Layout"

    end = 30
    pixel_its = [0,0,0]
    pixel_it = 0
    beats = [0]*7

    def __init__(self, layout, 
        r=.50, 
        g=0.50, 
        b=0.50

    ):
        super(Talker, self).__init__()
        self.layout = layout

        self.centre = Centre(length=fmap['stats']['c_pixels'],section='centre')
        self.right = Side(length=fmap['stats']['r_pixels'],section='right')
        self.left = Side(length=fmap['stats']['l_pixels'],section='left')
        
        self.cycle_start = time.time()

        self.temp_pixels = np.array([[0.0,0.0,0.0]]*(fmap['stats']['c_pixels']+fmap['stats']['r_pixels']+fmap['stats']['l_pixels']+fmap['stats']['cube_pixels']))
        
        self.hue_it = random.uniform(0.0, 1.0)
        self.hue_step = 0.005
        self.blob_length_factor = 10
        self.blob_hue_range_offset = 0.3
        self.blob_hue_range_factor = 0.03
        self.blob_hue_noise_range_offset = 0.05
        self.blob_hue_noise_range_factor = 0.03

        self.add_param("hue_step", self.hue_step, 0, 0.01)
        self.add_param("blob_hue_range_offset", self.blob_hue_range_offset, 0, 50)
        self.add_param("blob_hue_range_offset", self.blob_hue_range_offset, 0, 1)
        self.add_param("blob_hue_range_factor", self.blob_hue_range_factor, 0, 0.1)
        self.add_param("blob_hue_noise_range_offset", self.blob_hue_noise_range_offset, 0, 0.1)
        self.add_param("blob_hue_noise_range_factor", self.blob_hue_noise_range_factor, 0, 0.1)

        self.beat_range = [2,4]

        self.blob_buffer = []

        self.logger = logging_handler_setup('Animation Talker')


    def clear_pixels(self):
        for i in range(len(self.pixels)):
            self.layout.pixels[i].color = (0, 0, 0)

    def update(self):
        ''' TODO: create mid frame beat polling & toggle beat state 
        between frames so that only one beat per frame can happen '''
        
        self.hue_step = self.params["hue_step"].value
        self.blob_hue_range_offset = self.params["blob_hue_range_offset"].value
        self.blob_hue_range_offset = self.params["blob_hue_range_offset"].value
        self.blob_hue_range_factor = self.params["blob_hue_range_factor"].value
        self.blob_hue_noise_range_offset = self.params["blob_hue_noise_range_offset"].value
        self.blob_hue_noise_range_factor = self.params["blob_hue_noise_range_factor"].value


        self.clear_pixels()
  
        ''' add VU stuff ''' 
        for old_pix, new_pix in zip(self.layout.pixels[:fmap['stats']['l_pixels']], self.left.update(self.fft, self.hue_it)):
            old_pix.color = new_pix  

        for old_pix, new_pix in zip(self.layout.pixels[512:512+fmap['stats']['c_pixels']], self.centre.update(self.fft, self.hue_it)):
            old_pix.color = new_pix  

        for old_pix, new_pix in zip(self.layout.pixels[1024:1024+fmap['stats']['r_pixels']], self.right.update(self.fft, self.hue_it)):
            old_pix.color = new_pix 

        self.base_animation()

        l = fmap['stats']['l_pixels']
        c = fmap['stats']['c_pixels']
        r = fmap['stats']['r_pixels']
        cu = fmap['stats']['cube_pixels']



        ''' populate pixels to send out '''
        for old_pix, new_pix in zip(self.layout.pixels[:l], self.temp_pixels[:l]):
            # print type(old_pix), type(new_pix)
            old_pix.color += new_pix 

        for old_pix, new_pix in zip(self.layout.pixels[512:512+c], self.temp_pixels[l:l+c]):
            old_pix.color += new_pix 

        for old_pix, new_pix in zip(self.layout.pixels[1024:1024+r], self.temp_pixels[l+c:l+c+r]):
            old_pix.color += new_pix  

        for old_pix, new_pix in zip(self.layout.pixels[1536:1536+cu], self.temp_pixels[l+c+r:l+c+r+cu]):
            old_pix.color += new_pix  





    def base_animation(self):



        if self.check_beat(ch_range=self.beat_range):
            self.hue_it = (self.hue_it+self.hue_step)%1.
            # print 'Beat'

            blob_length = int(self.blob_length_factor*self.fft[3])
            blob_base_hue = self.hue_it
            blob_hue_range = self.blob_hue_range_offset+(sum(self.fft[:7]/7.0)*self.blob_hue_range_factor)
            blob_hue_noise_range = self.blob_hue_noise_range_offset+(sum(self.fft[:7]/7.0)*self.blob_hue_noise_range_factor)


            t = np.linspace(0, .5, blob_length)

            # i = signal.sawtooth((2 * np.pi * 2 * (t+phase)), width=0.5)
            hues = np.sin(2 * np.pi * t)
            values = np.copy(hues)*.6
            hues *= blob_hue_range
            # print np.amax(values)

            hues+=blob_base_hue

            noise = np.sin(2 * np.pi * t*(blob_length/2.0))*blob_hue_noise_range
            hues+=noise


            for x in xrange(len(hues)):
                self.temp_pixels[x] = colorsys.hsv_to_rgb(hues[x]%1.,1.0,values[x]%1.)
            

        for x in xrange(len(self.temp_pixels)-1,0,-1):
            self.temp_pixels[x] = self.temp_pixels[x-1]
        self.temp_pixels[0] = [0.0,0.0,0.0]



    def check_beat(self, ch_range=[0,3]):
        if sum(self.fft[7+ch_range[0]:7+ch_range[1]]) > 0:
            return True
        else:
            return False

