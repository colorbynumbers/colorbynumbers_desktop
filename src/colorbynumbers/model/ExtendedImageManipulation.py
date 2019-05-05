# Created by Lionel Kornberger at 2019-04-12
import numpy as np
from PIL import ImageFilter, Image
from ExtendedImage import *


class ExtendedImageManipulation:

    @staticmethod
    def reduce_colors(image, n_colors):
        from skimage import color
        from sklearn.cluster import KMeans
        from sklearn.utils import shuffle

        image = color.rgb2lab(image)
        width, height, dimension, image = ExtendedImageManipulation.__transform_to_2D_np_array__(image)

        image_sample = shuffle(image, random_state=0)[:1000]
        k_means = KMeans(n_clusters=n_colors, random_state=0).fit(image_sample)
        labels = k_means.predict(image)

        image = ExtendedImageManipulation.__recreate_image__(k_means.cluster_centers_, labels, width, height, dimension)
        image = color.lab2rgb(image)
        return ExtendedImage(Image.fromarray(np.uint8(image * 255)))

    @staticmethod
    def __recreate_image__(centers, labels, width, height, dimension):
        image = np.zeros((width, height, dimension))
        label_idx = 0
        for i in range(width):
            for j in range(height):
                image[i][j] = centers[labels[label_idx]]
                label_idx += 1
        return image

    @staticmethod
    def __transform_to_2D_np_array__(np_array):
        width, height, dimension = tuple(np_array.shape)
        assert dimension == 3
        image = np.reshape(np_array, (width * height, dimension))
        return width, height, dimension, image

    @staticmethod
    def refine_edge(image):
        return ExtendedImage(image.filter(ImageFilter.MedianFilter(size=11)))
