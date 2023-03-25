import random
import numpy as np


class Environment:

    def __init__(self, bio_density, width, height):
        self.bio_density = bio_density
        self.width = width
        self.height = height
        self.env = np.zeros((height+2, width+2), dtype=int)

    def generate_food(self):
        tiles = self.width * self.height
        food_number = int(self.bio_density * tiles)
        food_tiles = random.sample(range(tiles), food_number)
        for tile in food_tiles:
            x = (tile // self.width) + 1
            y = (tile % self.width) + 1
            self.env[y][x] = 1
