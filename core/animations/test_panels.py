from animation import Animation
from core.utilities import logging_handler_setup
from scipy import signal
import numpy as np
import time
import random



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

# right_face_panels = [[0,   27],
#                 [28,  43],
#                 [44,  65],
#                 [66,  81],
#                 [82,  91],
#                 [92,  111],
#                 [112, 135],
#                 [136, 152],
#                 [153, 165],
#                 [166, 191],
#                 [192, 214],
#                 [215, 240],
#                 [241, 263],
#                 [264, 298],
#                 [299, 318]]

# centre_face_panels = [[0,   27],
#                 [28,  53],
#                 [54,  66],
#                 [67,  80],
#                 [81,  89],
#                 [90,  102],
#                 [103, 128],
#                 [129, 155],
#                 [156, 224],
#                 [225, 241],
#                 [242, 272],
#                 [273, 289],
#                 [290, 318],
#                 [319, 338],
#                 [339, 355],
#                 [356, 385]]

# left_face_panels = [[0,   27],
#                 [28,  43],
#                 [44,  65],
#                 [66,  81],
#                 [82,  91],
#                 [92,  111],
#                 [112, 136],
#                 [137, 153],
#                 [154, 166],
#                 [167, 192],
#                 [193, 215],
#                 [216, 241],
#                 [242, 264],
#                 [265, 299],
#                 [300, 319]]





class FaceSection():

    modes = ['blank','fill','burst','ripple','fade','vu']
    mode = 'blank'

    def __init__(self, pixels_ref, pixel_index=[0,0]):

        self.start = pixel_index[0]
        self.end = pixel_index[1]
        self.length = self.end - self.start

        self.pixels = pixels_ref

        self.master_col = [0.5,0.5,0.5]
        self.target_master_col = [0.5,0.5,0.5]

        self.ramp_up = 1.0
        self.ramp_down = 1.0

        self.period = 30.0 # second
        self.width = 0.5

        self.cycle_start = time.time()

        self.temp_pixels = [[0,0,0]] * fmap['stats']['total_pixels']

        self.logger = logging_handler_setup('face section')

    def update(self, *args):


        t_delta = time.time()-self.cycle_start
        if t_delta > self.period:
            self.cycle_start = time.time()

        t_phase_b = t_delta / self.period


        carrier = np.sin(t_phase_b)
        carrierb = np.sin(t_phase_b)

        self.logger.debug("Carrier value %d"%carrier)

        if self.check_beat(args[0][8:10]):
            # print 'beat'
            panel_it = random.randint(0,len(fmap['left'])-1)

            h = random.uniform(carrier-.1, carrier+.1)
            v = random.uniform(carrier-.1, carrier+.1)
            # b = random.uniform(0.0, 1.0)


            for x in xrange(fmap['left'][panel_it][0],fmap['left'][panel_it][1]+1):
                self.pixels[x+self.start].set_hsv(h,0.9,.9)


        # print r
        

    def check_beat(self, beats):
        # print beats
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

        # face_it = 15
        # s = centre_face_panels[face_it][0]
        # f = centre_face_panels[face_it][1]
        # self.mouth = FaceSection(self.layout.pixels, pixel_index=[face_panels[face_it][0],face_panels[face_it][1]])
        self.left = FaceSection(self.layout.pixels, pixel_index=[0,318])

        # self.middle = FaceSection(self.layout.pixels, pixel_index=[512,512+385])
        # self.right = FaceSection(self.layout.pixels, pixel_index=[(512*2),(512*2)+318])
        



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
        
        # self.mouth.master_col = [0.0, self.fft[0], 0.0]
        self.left.update(self.fft) 
        # self.middle.update(self.fft) 
        # self.right.update(self.fft)   

        # self.eye.master_col = [self.fft[1], 0.0, 0.0]
        # self.eye.update()  
        # self.nose.master_col = [self.fft[3], 0.2, 0.7]
        # self.nose.update(self.fft) 

    

