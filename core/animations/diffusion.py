from animation import Animation

import numpy as np
from scipy.spatial import Delaunay
from sklearn.neighbors import kneighbors_graph
import matplotlib.pyplot as plt
import random

class Diffusion(Animation):
    def __init__(self, layout, num_neighbours=4):
        super(Diffusion, self).__init__()
        self.layout = layout

        points = np.array([p.location for p in self.layout.pixels])

        # TODO: I think triangulation would be better, this tends to give stitchy results
        # Adjacency Matrix: https://en.wikipedia.org/wiki/Adjacency_matrix
        self.points_graph = kneighbors_graph(points, num_neighbours, 
            mode='connectivity', 
            include_self=False
        ).toarray()

        self.pixels_np = np.array(self.pixels)

        self.add_heat(200)
        self.count = 0

        self.blur_speed = 0.5

    def add_heat(self, num_pixels):
        # For dev purposes
        start = random.choice(range(len(self.pixels)))
        for pixel in self.pixels[start:start+num_pixels]:
            pixel.r = random.random() 

        # For dev purposes
        # start = random.choice(range(len(self.pixels)))
        # for pixel in self.pixels[start:start+num_pixels]:
        #     pixel.g = random.random() 

        # For dev purposes
        start = random.choice(range(len(self.pixels)))
        for pixel in self.pixels[start:start+num_pixels]:
            pixel.b = random.random()   

    def blur(self):
        """
            Blur pixels by averaging over neighbouring pixel intensities for each color
        """
        # Loop over each pixel
        for i, pixel in enumerate(self.pixels):
            # Neighbouring pixels
            neighbour_indices = np.nonzero(self.points_graph[i])
    
            # TODO: DRY this up
            blur_intensity = np.mean([p.r for p in self.pixels_np[neighbour_indices]])
            pixel.r = self.blur_speed*blur_intensity + (1-self.blur_speed)*pixel.r

            blur_intensity = np.mean([p.g for p in self.pixels_np[neighbour_indices]])
            pixel.g = self.blur_speed*blur_intensity + (1-self.blur_speed)*pixel.g

            blur_intensity = np.mean([p.b for p in self.pixels_np[neighbour_indices]])
            pixel.b = self.blur_speed*blur_intensity + (1-self.blur_speed)*pixel.b

    def update(self):
        self.blur()

        self.count+=1
        print "count", self.count

        if self.count > 50:
            self.add_heat(100)
            self.count=0
