# Created by Lionel Kornberger at 2019-04-12
import numpy as np
from PIL import ImageFilter, Image

ZERO = 0
ONE = 1

AGGRESSIVE_DE_SPECKLE: int = 11
NORMAL_DE_SPECKLE: int = 5

DIN_SIZE = {
    "DIN A1": (7016, 9933),
    "DIN A2": (4961, 7016),
    "DIN A3": (3508, 4961),
    "DIN A4": (2480, 3508),
    "DIN A5": (1748, 2480)

}


class ImageManipulation:

    @staticmethod
    def convert_gray_to_rgb(image):
        if np.asarray(image).shape == (image.height, image.width):
            return Image.fromarray(np.squeeze(np.stack((image,) * 3, -1)))
        return image

    @staticmethod
    def reduce_colors(image, n_colors):
        from skimage import color
        from sklearn.cluster import KMeans
        from sklearn.utils import shuffle

        ImageManipulation.__scale_image(image)

        image = color.rgb2lab(image)
        width, height, dimension, image = ImageManipulation.__transform_to_2D_np_array__(image)

        image_sample = shuffle(image, random_state=0)[:1000]
        k_means = KMeans(n_clusters=n_colors, random_state=0).fit(image_sample)
        labels = k_means.predict(image)

        image = ImageManipulation.__recreate_image__(k_means.cluster_centers_, labels, width, height, dimension)
        image = color.lab2rgb(image)
        return Image.fromarray(np.uint8(image * 255))

    @staticmethod
    def __scale_image(image):
        size = 2200, 2200
        image.thumbnail(size, Image.ANTIALIAS)

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
    def refine_edge(image, is_aggressive):
        if is_aggressive:
            return image.filter(ImageFilter.MedianFilter(size=AGGRESSIVE_DE_SPECKLE))
        else:
            return image.filter(ImageFilter.MedianFilter(size=NORMAL_DE_SPECKLE))

    @staticmethod
    def resize_to_din_format(image, din_format="DIN A4"):
        # resize to match 300 dpi
        width, height = ImageManipulation.get_size_indicies(image)
        size = DIN_SIZE[din_format][width], DIN_SIZE[din_format][height]
        return image.resize(size, Image.LANCZOS)

    @staticmethod
    def is_landscape(image):
        return False if image.width < image.height else True

    @staticmethod
    def get_size_indicies(image):
        width, height = (ONE, ZERO) if ImageManipulation.is_landscape(image) else (ZERO, ONE)
        return width, height
