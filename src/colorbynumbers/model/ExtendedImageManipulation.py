# Created by Lionel Kornberger at 2019-04-12
import numpy as np
from PIL import ImageFilter, Image
from model.ExtendedImage import *

AGGRESSIVE_DE_SPECKLE: int = 11
NORMAL_DE_SPECKLE: int = 5


class ExtendedImageManipulation:

    @staticmethod
    def reduce_colors(image, n_colors):
        from skimage import color
        from sklearn.cluster import KMeans
        from sklearn.utils import shuffle

        ExtendedImageManipulation.__scale_image(image)

        image = color.rgb2lab(image)
        width, height, dimension, image = ExtendedImageManipulation.__transform_to_2D_np_array__(image)

        image_sample = shuffle(image, random_state=0)[:1000]
        k_means = KMeans(n_clusters=n_colors, random_state=0).fit(image_sample)
        labels = k_means.predict(image)

        image = ExtendedImageManipulation.__recreate_image__(k_means.cluster_centers_, labels, width, height, dimension)
        image = color.lab2rgb(image)
        return ExtendedImage(Image.fromarray(np.uint8(image * 255)))

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
            return ExtendedImage(image.filter(ImageFilter.MedianFilter(size=AGGRESSIVE_DE_SPECKLE)))
        else:
            return ExtendedImage(image.filter(ImageFilter.MedianFilter(size=NORMAL_DE_SPECKLE)))

    @staticmethod
    def detect_edges(image, n_color):
        print("in detect_edges")
        npimage = np.asarray(image)
        newimage = npimage.copy()
        # print(newimage)

        red = newimage[0, 0, 0]
        green = newimage[0, 0, 1]
        blue = newimage[0, 0, 2]

        print(newimage.shape[0])
        print(newimage.shape[1])
        print(newimage.shape[2])

        current_red = 0
        current_green = 0
        current_blue = 0

        counter = 0
        border = False
        newLine = False

        for row in range(newimage.shape[0]):
            newLine = True
            for col in range(newimage.shape[1]):
                if row == 0:
                    if col == 0:
                        counter += 1
                        continue
                    current_red = newimage[row, col, 0]
                    current_green = newimage[row, col, 1]
                    current_blue = newimage[row, col, 2]
                    if current_red != red or current_green != green or current_blue != blue:
                        red = current_red
                        green = current_green
                        blue = current_blue
                        newimage[row, col, 0] = 0
                        newimage[row, col, 1] = 0
                        newimage[row, col, 2] = 0
                        border = True
                    counter += 1
                    continue
                else:
                    if col == 0:
                        red = newimage[row - 1, col, 0]
                        green = newimage[row - 1, col, 1]
                        blue = newimage[row - 1, col, 2]
                        current_red = newimage[row, col, 0]
                        current_green = newimage[row, col, 1]
                        current_blue = newimage[row, col, 2]
                        if red == 0 and green == 0 and blue == 0:
                            counter += 1
                            continue
                        if current_red != red or current_green != green or current_blue != blue:
                            red = current_red
                            green = current_green
                            blue = current_blue
                            newimage[row, col, 0] = 0
                            newimage[row, col, 1] = 0
                            newimage[row, col, 2] = 0
                            border = True
                        counter += 1
                        continue
                    else:
                        current_red = newimage[row, col, 0]
                        current_green = newimage[row, col, 1]
                        current_blue = newimage[row, col, 2]
                        red = newimage[row - 1, col, 0]
                        green = newimage[row - 1, col, 1]
                        blue = newimage[row - 1, col, 2]
                        if current_red != red or current_green != green or current_blue != blue:
                            if red != 0 and green != 0 and blue != 0:
                                red = current_red
                                green = current_green
                                blue = current_blue
                                newimage[row, col, 0] = 0
                                newimage[row, col, 1] = 0
                                newimage[row, col, 2] = 0
                                border = True
                                counter += 1
                                continue
                        red = newimage[row, col - 1, 0]
                        green = newimage[row, col - 1, 1]
                        blue = newimage[row, col - 1, 2]
                        if current_red != red or current_green != green or current_blue != blue:
                            if red != 0 and green != 0 and blue != 0:
                                red = current_red
                                green = current_green
                                blue = current_blue
                                newimage[row, col, 0] = 0
                                newimage[row, col, 1] = 0
                                newimage[row, col, 2] = 0
                                border = True
                        counter += 1
                        continue

        from skimage import color
        Image.fromarray(newimage).show()
        newimage = color.lab2rgb(newimage)
        newimage = ExtendedImage(newimage.fromarray(np.uint8(newimage * 255)))
        return newimage
