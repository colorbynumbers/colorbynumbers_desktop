# Created by Lionel Kornberger at 2019-04-12
import numpy as np
from PIL import ImageFilter, Image, ImageDraw, ImageFont

from model.Surface.IterativeSurfaceHandling import IterativeSurfaceHandling

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

        labels, surface_center_dict = IterativeSurfaceHandling().remove_small_areas(labels, width, height, min_surface,
                                                                                    n_colors)

        image, canvas, img_numbers = ImageManipulation.__recreate_image__(k_means.cluster_centers_, labels, width,
                                                                          height, dimension, surface_center_dict)
        image_colors = ImageManipulation.get_color_info(k_means.cluster_centers_)

        canvas = Image.fromarray(np.uint8(canvas))
        canvas_with_numbers = canvas.copy()
        canvas_with_numbers.paste(img_numbers, (0, 0), img_numbers)
        image = color.lab2rgb(image)
        return Image.fromarray(np.uint8(image * 255)), canvas, canvas_with_numbers, image_colors

    @staticmethod
    def get_color_info(cluster_center):
        from skimage import color
        image_colors = cluster_center.reshape(cluster_center.shape[0], 1, 3)
        image_colors = color.lab2rgb(image_colors)
        return np.uint8(image_colors * 255)

    @staticmethod
    def scale_image(image):
        width = 1200
        factor = (width / float(image.size[0]))
        height = int((float(image.size[1]) * float(factor)))
        return image.resize((width, height))

    @staticmethod
    def __recreate_image__(centers, labels, width, height, dimension, surface_center_dict):
        image = np.zeros((width, height, dimension))
        canvas = np.zeros((width, height, dimension))
        canvas.fill(255)
        from PIL import Image

        img_numbers = Image.new('RGBA', (height, width), (255, 0, 0, 0))

        label_idx = 0
        for i in range(width):
            for j in range(height):
                image[i][j] = centers[labels[label_idx]]
                ImageManipulation.__draw_dot(image, i, j, canvas)
                ImageManipulation.__draw_number(img_numbers, i, j, image, surface_center_dict, labels, width, height)
                label_idx += 1
        return image, canvas, img_numbers

    @staticmethod
    def __draw_dot(image, i, j, canvas):
        if j > 0 and not np.array_equal(image[i][j], image[i][j - 1]):
            canvas[i][j] = np.array([0, 0, 0], dtype=float)

        if i > 0 and not np.array_equal(image[i][j], image[i - 1][j]):
            canvas[i - 1][j] = np.array([0, 0, 0], dtype=float)

    @classmethod
    def __draw_number(cls, img_numbers, i, j, image, surface_center_dict, labels, width, height):
        gap = 4
        labels_2d = np.reshape(labels, (width, height))

        if str(i) + " " + str(j) in surface_center_dict:
            if j > gap and i > gap and i < width - gap and j < height - gap:
                enough_room = True
                if not np.array_equal(labels_2d[i][j], labels_2d[i+gap][j+gap]) or not np.array_equal(labels_2d[i][j],labels_2d[i-gap][j+gap]) or not np.array_equal(labels_2d[i][j],labels_2d[i+gap][j-gap]):
                    enough_room = False
                if enough_room:
                    '../../resources/SourceSerifPro-Regular.ttf'
                    draw = ImageDraw.Draw(img_numbers)
                    # font = ImageFont.truetype(<font-file>, <font-size>)
                    font = ImageFont.truetype("../resources/SourceSerifPro-Regular.ttf", 12,
                                              layout_engine=ImageFont.LAYOUT_RAQM)
                    # draw.text((x, y),"Sample Text",(r,g,b))
                    draw.text((j, i), str(surface_center_dict[str(i) + " " + str(j)]), fill=(0, 0, 0), font=font,
                              anchor=(j, i))

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
        width, height = ImageManipulation.get_size_indices(image)
        size = DIN_SIZE[din_format][width], DIN_SIZE[din_format][height]
        return image.resize(size, Image.LANCZOS)

    @staticmethod
    def is_landscape(image):
        return False if image.width < image.height else True

    @staticmethod
    def get_size_indices(image):
        width, height = (ONE, ZERO) if ImageManipulation.is_landscape(image) else (ZERO, ONE)
        return width, height

    @staticmethod
    def draw_rectangle_on_image(image, point_1, point_2, fill_color):

        # TODO split image in rectangles (x,y) coodinates for drawing the rectangles and the numbers
        draw = ImageDraw.Draw(image)
        draw.rectangle((point_1, point_2), fill=fill_color, outline="black", width=5)

        return image

    @staticmethod
    def calculate_rectangle_points(point, width, height):
        return point, (point[0] + width, point[1] + height)

    @staticmethod
    def draw_text_on_image(image, text, point, font_size):
        '../../resources/SourceSerifPro-Regular.ttf'
        draw = ImageDraw.Draw(image)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("../resources/SourceSerifPro-Regular.ttf", font_size)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text(point, text, (0, 0, 0), font=font)
        return image
