import numpy as np
import time
import random
import colorsys
from core.utilities import logging_handler_setup

''' right 8 extra pixels '''
''' Map of the panels on the face '''
fmap = {
    'stats' : {
        'total_pixels' : 1025,
        'r_pixels' : 319,
        'c_pixels' : 386,
        'l_pixels' : 320,
        'cube_pixel' : 348
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
                [300, 319]],
    'cube'  :   [[0,  28],
                [29,  57],
                [58,  86],
                [87,  115],
                [116, 144],
                [145, 173],
                [174, 202],
                [203, 231],
                [232, 260],
                [261, 289],
                [290, 318],
                [319, 347]]

}
