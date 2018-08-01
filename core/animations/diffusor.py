from animation import Animation

import numpy as np
from scipy.spatial import Delaunay
from sklearn.neighbors import kneighbors_graph
import matplotlib.pyplot as plt
import random

class Diffusor(Animation):
    def __init__(self, layout, num_neighbours=4):
        """
            An animation with diffusion (blurring) capabilities
            Performs k-nearest neighbour to find the neighbours used for blurring
        """
        super(Diffusion, self).__init__()
        self.layout = layout

        points = np.array([p.location for p in self.layout.pixels])

        # Adjacency Matrix: https://en.wikipedia.org/wiki/Adjacency_matrix
        # TODO: I think triangulation would be better, this tends to give stitchy results
        self.points_graph = kneighbors_graph(points, num_neighbours, 
            mode='connectivity', 
            include_self=False
        ).toarray()

        # TODO: Move this somewhere more generic
        self.pixels_np = np.array(self.pixels)

        # How quickly pixels blur (0->1)
        self.add_param("blur_speed", 0.5, 0, 1)

    def blur(self):
        """
            Blur (diffuse) pixels by averaging over neighbouring pixel intensities for each color
        """
        blur_speed = self.params["blur_speed"].value

        # Loop over each pixel
        for i, pixel in enumerate(self.pixels):
            # Find the neighbs
            neighbour_indices = np.nonzero(self.points_graph[i])
    
            # Average across each color
            # TODO: DRY this up
            blur_intensity = np.mean([p.r for p in self.pixels_np[neighbour_indices]])
            pixel.r = blur_speed*blur_intensity + (1-blur_speed)*pixel.r

            blur_intensity = np.mean([p.g for p in self.pixels_np[neighbour_indices]])
            pixel.g = blur_speed*blur_intensity + (1-blur_speed)*pixel.g

            blur_intensity = np.mean([p.b for p in self.pixels_np[neighbour_indices]])
            pixel.b = blur_speed*blur_intensity + (1-blur_speed)*pixel.b

    def update(self, blur_prob=0.2, num_heated_pixels=100):
        """
            Blurs pixels and adds random heat to random pixels sometimes
            For illustrative purposes rather than actually pattern to be used
        """
        # Blur it up
        self.blur()

        # HACK : Setting heat_count here if its not previously defined
        #   Doing this because I want to show how blur works and don't want extra 
        #   vars that aren't useful in general inherited in the object
        try:
           self.heat_count
        except AttributeError:
           self.heat_count=0

        # Add some HEAT, sometimes
        if random.random() < blur_prob:
            self.add_random_heat(num_heated_pixels)

    def add_random_heat(self, num_pixels, r_max=1, g_max=0.1, b_max=1):
        """
            Adds red and blue heat to a consecutive set of pixels from a random starting point
            max is 0->1  
        """ 
        # TODO: DRY this up
        start = random.choice(range(len(self.pixels)))
        for pixel in self.pixels[start:start+num_pixels]:
            pixel.r = random.random()*r_max

        start = random.choice(range(len(self.pixels)))
        for pixel in self.pixels[start:start+num_pixels]:
            pixel.g = random.random()*g_max

        start = random.choice(range(len(self.pixels)))
        for pixel in self.pixels[start:start+num_pixels]:
            pixel.b = random.random()*b_max 
