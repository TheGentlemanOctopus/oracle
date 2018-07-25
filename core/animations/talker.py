from animation import Animation

import numpy as np
import time

class Talker(Animation):
    layout_type = "Layout"

    def __init__(self, layout, 
        r=.5, 
        g=.5, 
        b=.5, 

    ):
        super(Talker, self).__init__()
        self.layout = layout

        self.add_param("r", r_slowness, 0, 1)
        self.add_param("g", g_slowness, 0, 1)
        self.add_param("b", b_slowness, 0, 1)

        self.buff_len = 1500

    def update(self):
        overall_slowness = self.params["overall_slowness"].value
        r_slowness = overall_slowness*self.params["r_slowness"].value
        g_slowness = overall_slowness*self.params["g_slowness"].value
        b_slowness = overall_slowness*self.params["b_slowness"].value

        current_time = np.float16((time.time() - self.start_time))
        dt = current_time - self.previous_time
        self.previous_time = current_time

        self.t = np.append(self.t, current_time)
        
        self.r = np.append(self.r, np.mean([self.fft[0], self.fft[1]], dtype=np.float16))
        self.g = np.append(self.g, np.mean([self.fft[2], self.fft[3]], dtype=np.float16))
        self.b = np.append(self.b, np.mean([self.fft[4], self.fft[5], self.fft[6]], dtype=np.float16))

        if len(self.t) > self.buff_len:
            self.t = self.t[1:]
            self.r = self.r[1:]
            self.g = self.g[1:]
            self.b = self.b[1:]

        domain_r = np.linspace(current_time, current_time - r_slowness, len(self.pixels)) 
        domain_g = np.linspace(current_time, current_time - g_slowness, len(self.pixels)) 
        domain_b = np.linspace(current_time, current_time - b_slowness, len(self.pixels))

        r = np.interp(domain_r, self.t, self.r)
        g = np.interp(domain_r, self.t, self.g)
        b = np.interp(domain_r, self.t, self.b)

        for i in range(len(self.pixels)):
            self.layout.pixels[i].color = (r, g, b)
