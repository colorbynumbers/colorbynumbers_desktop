# Created by Lionel Kornberger at 2019-04-12
import numpy as np
from PIL import ImageFilter, Image

from Surface.IterativeSurfaceHandling import IterativeSurfaceHandling

ZERO = 0
ONE = 1

AGGRESSIVE_DE_SPECKLE: int = 15
NORMAL_DE_SPECKLE: int = 7

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
    def reduce_colors(image, n_colors, min_surface):
        from skimage import color
        from sklearn.cluster import KMeans
        from sklearn.utils import shuffle

        image = color.rgb2lab(image)
        width, height, dimension, image = ImageManipulation.__transform_to_2D_np_array__(image)

        image_sample = shuffle(image, random_state=0)[:1000]
        k_means = KMeans(n_clusters=n_colors, random_state=0).fit(image_sample)
        labels = k_means.predict(image)

        labels, surface_dict = IterativeSurfaceHandling().remove_small_areas(labels, width, height, min_surface,
                                                                             n_colors)

        image, canvas, img_numbers = ImageManipulation.__recreate_image__(k_means.cluster_centers_, labels, width,
                                                                          height, dimension, )
        image = color.lab2rgb(image)

        canvas = Image.fromarray(np.uint8(canvas))
        canvas.paste(img_numbers, (0, 0), img_numbers)
        return Image.fromarray(np.uint8(image * 255)), canvas

    @staticmethod
    def __scale_image(image):
        size = 2200, 2200
        image.thumbnail(size, Image.ANTIALIAS)

    @staticmethod
    def __recreate_image__(centers, labels, width, height, dimension):
        image = np.zeros((width, height, dimension))
        canvas = np.zeros((width, height, dimension))
        canvas.fill(255)
        from PIL import Image

        img_numbers = Image.new('RGBA', (height, width), (255, 0, 0, 0))

        label_idx = 0
        for i in range(width):
            for j in range(height):
                image[i][j] = centers[labels[label_idx]]
                write_number = ImageManipulation.__should_write_number(j, i)
                ImageManipulation.__draw_dot(image, i, j, canvas, write_number)
                label_idx += 1
        return image, canvas, img_numbers

    @staticmethod
    def __should_write_number(j, i):
        return i % 21 == 0

    @staticmethod
    def __draw_dot(image, i, j, canvas, write_number):
        if j > 0 and not np.array_equal(image[i][j], image[i][j - 1]):

            canvas[i][j] = np.array([0, 0, 0], dtype=float)

            if j > 10 and write_number:

                enough_room = True
                for k in range(j, -1, -1):
                    if not np.array_equal(image[i][j], image[i][k]):
                        if j - k < 10:
                            enough_room = False
                            break
                        else:
                            break

        if i > 0 and not np.array_equal(image[i][j], image[i - 1][j]):
            canvas[i - 1][j] = np.array([0, 0, 0], dtype=float)

    @staticmethod
    def __transform_to_2D_np_array__(np_array):
        width, height, dimension = tuple(np_array.shape)
        assert dimension == 3
        image = np.reshape(np_array, (width * height, dimension))
        return width, height, dimension, image

    @staticmethod
    def refine_edge(image, is_aggressive):

        ImageManipulation.__scale_image(image)

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
