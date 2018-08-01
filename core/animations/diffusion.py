from animation import Animation

import numpy as np
from scipy.spatial import Delaunay
from sklearn.neighbors import kneighbors_graph
import matplotlib.pyplot as plt

class Diffusion(Animation):
    def __init__(self, layout, num_neighbours=5):
        super(Diffusion, self).__init__()
        self.layout = layout

        points = np.array([p.location for p in self.layout.pixels])

        # TODO: I think triangulation would be better, this tends to give stitchy results
        self.neighbours = kneighbors_graph(points, num_neighbours, mode='connectivity', include_self=False).toarray()

    def update(self):
        pass