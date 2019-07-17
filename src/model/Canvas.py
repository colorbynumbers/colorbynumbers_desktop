# Created by Lionel Kornberger at 2019-04-01
from numpy import ones, uint8

WHITE = 255


class Canvas:

    def __init__(self, height, width):
        self.canvas = WHITE * ones((height, width, 3), uint8)

    def draw_dot(self, x, y):
        pass
