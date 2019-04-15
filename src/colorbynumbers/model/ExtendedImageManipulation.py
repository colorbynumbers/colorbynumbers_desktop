# Created by Lionel Kornberger at 2019-04-12
from PIL import ImageFilter
from ExtendedImage import *


class ExtendedImageManipulation:

    @staticmethod
    def reduce_colors(image, color_amount):
        manipulated_image = image.convert("P", dither=None, palette=1, colors=color_amount)
        return ExtendedImage(manipulated_image.convert("RGB"))

    @staticmethod
    def refine_edge(image):
        return ExtendedImage(image.filter(ImageFilter.MedianFilter(size=5)))
