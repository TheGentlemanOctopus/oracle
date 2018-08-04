from animation import Animation
from core.utilities import logging_handler_setup
from panel_utils import fmap
from scipy import signal
import numpy as np
import time
import colorsys



class FaceSection():

    modes = ['blank','fill','burst','ripple','fade','vu']
    mode = 'blank'

    def __init__(self, length=10,section='left'):

        
        self.length = length
        self.section = section

        self.period = 10.0 # second
        self.width = 0.5

        self.cycle_start = time.time()

        self.fft_history = np.array([0.0]*(self.length+1))

        self.temp_pixels = np.array([[0.0,0.0,0.0]]*self.length)


    def update(self, *args):

        fft = args[0]
        speed = self.period #- ((1.01-fft[1])*3)
        # print speed
        t_delta = time.time()-self.cycle_start
        if t_delta > speed:
            self.cycle_start = time.time()

        t_phase_b = t_delta / speed

        t = np.linspace(0, 1, self.length+1)

        t_sin = np.linspace(t_phase_b, t_phase_b+3, self.length+1)
        accent_wave = np.sin(t_sin)

        self.fft_history = np.insert(self.fft_history[0:-1],0,fft[3])

        # sig = signal.sawtooth((2 * np.pi * 2 * (t+t_phase_b)), width=0.75)
        # base_col = signal.square((2 * np.pi * 25 * (t+t_phase_b)), duty=(sig+1)/2)
        # base_col = signal.square((2 * np.pi * 25 * (t+t_phase_b)), duty=0.75)
        
        # base_hue = (0.1+(fft[1]*0.4))
        base_hue = (t_phase_b+(.1*fft[1]))
        # hues = np.array([base_hue]*(self.length+1))


        bass_square = signal.square((2 * np.pi * 3 * (t+t_phase_b)), duty=fft[2]*.7)
        bass_square+=1
        bass_square/=2

        bass_squareb = signal.square((2 * np.pi * 2 * (t-t_phase_b)), duty=fft[4]*.3)
        bass_squareb+=1
        bass_squareb/=2

        hues = ((np.array([base_hue]*(self.length+1))) + (accent_wave*fft[1]*.001))%1.0

        bass_square+=bass_squareb
        bass_square/2


        hues+=((bass_square*0.5)%1.0)

        hues+= ((self.fft_history*0.2)%1.0)
        # # hues+=1
        # # hues/=2

        # base_col+=sig
        # base_col+=1
        # base_col/=2
        # base_col+=0.2
        # base_col = np.clip(base_col, 0,1)

        # values = base_col

        # accent_col = signal.square((2 * np.pi * (25*fft[3]) * (t+t_phase_b*3)),duty=fft[1])
        

        # # values+= accent_col 
        # hues += accent_col

        # hues = np.clip(hues, 0,1)

        # hues = np.mod(hues,1.0)
        # # print hues
        ''' --- '''
        # base_col = signal.square((2 * np.pi * (25*fft[3]) * (t+t_phase_b*3)))

        # b = signal.sawtooth((2 * np.pi * 6 * (t+t_phase_b)), width=0.25)*fft[1]
        # b+=1
        # b/=2

        # g = signal.sawtooth((2 * np.pi * 2 * (t-t_phase_b)), width=0.75)*fft[2]
        # g+=1
        # g/=1

        # r = signal.square((2 * np.pi * (25*fft[3]) * (t+t_phase_b*3)))
        # r+=1
        # r/=2
        # r*=fft[3]

        # b_bass = signal.sawtooth((2 * np.pi * 1 * (t+t_phase_b)), width=0.25)*fft[1]
        # b_bass+=1
        # b_bass/=4

        # b+=b_bass
        # b = np.clip(0,.99,b)

        # r-=b_bass
        # r = np.clip(0,1,r)
        # g-=b_bass
        # g = np.clip(0,1,g)

        # print r
        for x in xrange(0,self.length):
            # self.pixels[x+self.start].color = (r[x],g[x],b[x])

            self.temp_pixels[x] = colorsys.hsv_to_rgb(hues[x],0.9,bass_square[x])


            # self.pixels[x+self.start].set_hsv(hues[x],0.9,bass_square[x])

        return self.temp_pixels
 


class Square():

    def __init__(self,length=29):

        self.length = length
        self.strip_length = length/4
        self.temp_pixels = np.array([[0.0,0.0,0.0]]*self.length)

    def update(self,fft,hue):
        self.fill()
        vu_level = sum(fft[:7])/7.0
        colA = colorsys.hsv_to_rgb(hue,.90,.90)
        colB = colorsys.hsv_to_rgb((hue+.5)%1.0,.90,.90)
        self.vu_fill(vu_level,colA,colB)

        return self.temp_pixels


    def vu_fill(self, vu_value, colorA, colorB):
        pixel_target = int(vu_value*(self.length))
        # print pixel_target
        # pixel_target = 29*3
        self.vu_up(pixel_target,colorA)
        self.vu_down(pixel_target,colorA, colorB)



    def vu_up(self,pixel_target,color):
        ''' bottom up '''
        for x in xrange(0,pixel_target,1):
            self.temp_pixels[x] += color


    def vu_down(self,pixel_target,color,overlapcol):
        ''' top down '''
        for x in xrange(self.length-1,self.length-(pixel_target+1),-1):
            if np.array_equal(self.temp_pixels[x], np.array([0.0,0.0,0.0])):
                self.temp_pixels[x] += color
            else:
                self.temp_pixels[x] = overlapcol
        
    def fill(self,c=[0.0,0.0,0.0]):
        for x in xrange(len(self.temp_pixels)):
            self.temp_pixels[x] = np.array(c)


class Cube():

    def __init__(self, length=10,section='left'):

        
        self.length = length
        self.section = section
        self.square_length = self.length/3

        self.temp_pixels = np.array([[0.0,0.0,0.0]]*self.length)

        self.squareA = Square(length=self.length/3)
        self.hue = 0.1



    def update(self, *args):

        # self.clear_pixels()
        fft = args[0]
        vu_level = fft[2]
        

        
        self.temp_pixels[:self.square_length] = self.squareA.update(fft,self.hue)
        self.temp_pixels[self.square_length:2*self.square_length] = self.temp_pixels[:self.square_length]
        self.temp_pixels[2*self.square_length:3*self.square_length] = self.temp_pixels[:self.square_length]

        self.hue = (self.hue+0.001)%1.0
        return self.temp_pixels
 
    def clear_pixels(self):
        for x in xrange(len(self.temp_pixels)):
            self.temp_pixels[x] = np.array([0.0,0.0,0.0])


class Waves(Animation):
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
        super(Waves, self).__init__()
        self.layout = layout

        self.add_param("r", r, 0, 1)
        self.add_param("g", g, 0, 1)
        self.add_param("b", b, 0, 1)

        self.left = FaceSection(length=fmap['stats']['l_pixels'],section='left')
        self.centre = FaceSection(length=fmap['stats']['c_pixels'],section='centre')
        self.right = FaceSection(length=fmap['stats']['r_pixels'],section='right')
        self.cube = Cube(length=fmap['stats']['cube_pixels'],section='cube')

        # self.cube = Cube(length=300,section='cube')

        self.logger = logging_handler_setup('hsv test')
        self.logger.info('Animation waves')



    def clear_pixels(self):
        for i in range(len(self.pixels)):
            self.layout.pixels[i].color = (0, 0, 0)

    def update(self):
        ''' TODO: create mid frame beat polling & toggle beat state 
        between frames so that only one beat per frame can happen '''
        
        r = self.params["r"].value
        g = self.params["g"].value
        b = self.params["b"].value

        # self.clear_pixels()

        
        for old_pix, new_pix in zip(self.layout.pixels[0:fmap['stats']['l_pixels']], self.left.update(self.fft)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[512:512+fmap['stats']['c_pixels']], self.centre.update(self.fft)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[1024:1024+fmap['stats']['r_pixels']], self.right.update(self.fft)):
            old_pix.color = new_pix

        for old_pix, new_pix in zip(self.layout.pixels[1536:1536+fmap['stats']['cube_pixels']], self.cube.update(self.fft)):
            old_pix.color = new_pix

        # for old_pix, new_pix in zip(self.layout.pixels[0:0+fmap['stats']['cube_pixels']], self.cube.update(self.fft)):
        #     old_pix.color = new_pix


    def check_beat(self, ch_range=[0,3]):
        if sum(self.fft[7+ch_range[0]:7+ch_range[1]]) > 0:
            return True
        else:
            return False

