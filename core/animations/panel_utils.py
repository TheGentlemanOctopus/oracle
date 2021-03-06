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
        'cube_pixels' : 348
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


spatial_fmap = {
    'right' : [ fmap['right'][13],
                fmap['right'][14],
                fmap['right'][0],
                fmap['right'][12],
                fmap['right'][10],
                fmap['right'][11],
                fmap['right'][1],
                fmap['right'][2],
                fmap['right'][3],
                fmap['right'][9],
                fmap['right'][8],
                fmap['right'][5],
                fmap['right'][4],
                fmap['right'][7],
                fmap['right'][6]],

    'centre' : [fmap['centre'][13],
                fmap['centre'][12],
                fmap['centre'][15],
                fmap['centre'][14],
                fmap['centre'][9],
                fmap['centre'][10],
                fmap['centre'][11],
                fmap['centre'][8],
                fmap['centre'][3],
                fmap['centre'][5],
                fmap['centre'][4],
                fmap['centre'][2],
                fmap['centre'][6],
                fmap['centre'][7],
                fmap['centre'][1],
                fmap['centre'][0]],

    'left'  :  [fmap['left'][13],
                fmap['left'][14],
                fmap['left'][0],
                fmap['left'][12],
                fmap['left'][10],
                fmap['left'][11],
                fmap['left'][1],
                fmap['left'][2],
                fmap['left'][3],
                fmap['left'][9],
                fmap['left'][8],
                fmap['left'][5],
                fmap['left'][4],
                fmap['left'][7],
                fmap['left'][6]],

    'cube'  :  [fmap['cube'][0],
                fmap['cube'][1],
                fmap['cube'][2],
                fmap['cube'][3],
                fmap['cube'][4],
                fmap['cube'][5],
                fmap['cube'][6],
                fmap['cube'][7],
                fmap['cube'][8],
                fmap['cube'][9],
                fmap['cube'][10],
                fmap['cube'][11]]

}
