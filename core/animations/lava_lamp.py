from animation import Animation

import random
import time
import color_utils

import numpy as np

class LavaLamp(Animation):
    def __init__(self, layout,
        color_speed=1.2, 
        blob_speed=0.3, 
        blob_size=0.3, 
        warp_speed=5
    ):
        super(LavaLamp, self).__init__()
        self.layout = layout

        self.add_param("color_speed", color_speed, 0, 4)
        self.add_param("blob_speed", blob_speed, 0, 1)
        self.add_param("blob_size", blob_size, 0, 1)
        self.add_param("warp_speed", warp_speed, 0, 5)

        self.pattern_time = 0
        self.real_time = 0
        
        self.start_time = time.time()

        pixels = self.pixels
        self.x = np.array([pixel.location[0] for pixel in pixels], dtype=np.float16)
        self.y = np.array([pixel.location[1] for pixel in pixels], dtype=np.float16)
        self.z = np.array([pixel.location[2] for pixel in pixels], dtype=np.float16)

        self.x += color_utils.cos_lookup(self.x + np.float16(0.2)*self.z, offset=0, period=1, minn=0, maxx=0.6)
        self.y += color_utils.cos_lookup(self.x, offset=0, period=1, minn=0, maxx=0.3)
        self.z += color_utils.cos_lookup(self.y + self.z, offset=0, period=1.5, minn=0, maxx=0.2)


    def update(self):
        """Compute the color of a given pixel.
    
        t: time in seconds since the program started.
        ii: which pixel this is, starting at 0
        coord: the (x, y, z) position of the pixel as a tuple
        n_pixels: the total number of pixels
        random_values: a list containing a constant random value for each pixel
    
        Returns an (r, g, b) tuple in the range 0-255
    
        """
 
        pixels = self.pixels
        coordinates = [pixel.location for pixel in pixels]
        n_pixels = len(pixels)

        blob_speed = self.params["blob_speed"].value
        blob_size = self.params["blob_size"].value
        warp_speed = self.params["warp_speed"].value
        color_speed = self.params["color_speed"].value

        #Warp speed
        current_time = (time.time() - self.start_time)

        speed = np.mean(self.fft)
        self.pattern_time = self.pattern_time + (warp_speed*speed+1)*(self.real_time - current_time)
        self.real_time = current_time

        #TODO: param for this, or swallow it with warp speed
        t = self.pattern_time*np.float16(0.6)


        r = color_utils.cos_lookup(self.x, offset=t*color_speed, period=2, minn=0, maxx=1)
        g = color_utils.cos_lookup(self.y, offset=t*color_speed, period=2, minn=0, maxx=1)
        b = color_utils.cos_lookup(self.z, offset=t*color_speed, period=2, minn=0, maxx=1)


        r = color_utils.contrast_np(r, 0.5, 1.5)
        g = color_utils.contrast_np(g, 0.5, 1.5)
        b = color_utils.contrast_np(b, 0.5, 1.5)
    
    #     # shift the color of a few outliers
    #     if random_values[ii] < 0.03:
    #         r, g, b = b, g, r
    
        # black out regions
        r2 = color_utils.cos_lookup(self.x, offset=t*blob_speed + 12.345, period=3, minn=0, maxx=1)
        g2 = color_utils.cos_lookup(self.y, offset=t*blob_speed + 24.536, period=3, minn=0, maxx=1)
        b2 = color_utils.cos_lookup(self.z, offset=t*blob_speed + 34.675, period=3, minn=0, maxx=1)
        clampdown = (r2 + g2 + b2)/2



        #Only things 0.8+ get color
        clampdown = color_utils.remap(clampdown, 0.8, 0.9, 0, 1)
        clampdown = color_utils.clamp(clampdown, -blob_size, 1)

        r *= clampdown
        g *= clampdown
        b *= clampdown

        # color scheme: fade towards blue-and-orange
    #     g = (r+b) / 2
        g = g * 0.6 + ((r+b) / 2) * 0.4

        # r *= 256
        # g *= 256
        # b *= 256        

        # apply gamma curve
        # only do this on live leds, not in the simulator
        #r, g, b = ccolor_utils.gamma((r, g, b), 2.2)

        for i in range(len(pixels)):
            pixels[i].color = (r[i], g[i], b[i])