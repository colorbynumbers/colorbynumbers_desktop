# Created by Lionel Kornberger at 2019-05-21
import img2pdf
from tempfile import NamedTemporaryFile
from PIL import Image

DIN_FORMAT = {
    "DIN A1": (594, 841),
    "DIN A2": (420, 594),
    "DIN A3": (297, 420),
    "DIN A4": (210, 297),
    "DIN A5": (148, 210)
}

ROWS_AND_COLUMNS = (5, 7)


def create_color_ref_images(colors_arr, din_format, template_image):
    from src.model.ImageManipulation import ImageManipulation, DIN_SIZE

    din_in_pixel = DIN_SIZE["DIN A4"]
    width, height = ImageManipulation.get_size_indices(template_image)
    width_for_color = din_in_pixel[width] / ROWS_AND_COLUMNS[width]
    height_for_color = din_in_pixel[height] / ROWS_AND_COLUMNS[height]

    is_landscape = ImageManipulation.is_landscape(template_image)

    img_colors = [Image.new('RGB', (din_in_pixel[width], din_in_pixel[height]), (255, 255, 255, 0))]

    point_1 = (0, 0)
    temp_color_image_index = 0
    for color_label, temp_color in enumerate(colors_arr):
        color = tuple(temp_color[0])

        point_1, point_2 = ImageManipulation.calculate_rectangle_points(point_1, width_for_color, height_for_color)
        img_colors[temp_color_image_index] = ImageManipulation.draw_rectangle_on_image(
            img_colors[temp_color_image_index], point_1, point_2, color)

        img_colors[temp_color_image_index] = ImageManipulation.draw_text_on_image(img_colors[temp_color_image_index],
                                                                                  create_color_mixture_string(
                                                                                      color_label, color),
                                                                                  (point_1[0] + width_for_color + 25,
                                                                                   point_1[1] + 25),
                                                                                  font_size=38)

        # Todo refactor and remove duplicate code
        if is_landscape:
            if (color_label + 1) % 3 == 0:
                point_1 = (0, point_1[1] + height_for_color)
            else:
                point_1 = (point_1[0] + 2 * width_for_color, point_1[1])
            if color_label != 0 and color_label % 14 == 0:
                img_colors.append(Image.new('RGB', (din_in_pixel[width], din_in_pixel[height]), (255, 255, 255, 0)))
                temp_color_image_index += 1
                point_1 = (0, 0)
        else:
            if color_label % 2 != 0:
                point_1 = (0, point_1[1] + height_for_color)
            else:
                point_1 = (point_1[0] + 2 * width_for_color, point_1[1])
            if color_label != 0 and color_label % 17 == 0:
                img_colors.append(Image.new('RGB', (din_in_pixel[width], din_in_pixel[height]), (255, 255, 255, 0)))
                temp_color_image_index += 1
                point_1 = (0, 0)

    return img_colors


def export(reduced_image, template_image, template_with_numbers_image,colors_arr, din_format, file_name):
    temp_file_reduced_image = NamedTemporaryFile(suffix='.png')  # this is a file object
    reduced_image.save(temp_file_reduced_image.name, format="png")  # save the content to temp

    temp_file_template_image = NamedTemporaryFile(suffix='.png')  # this is a file object
    template_image.save(temp_file_template_image.name, format="png")  # save the content to temp

    temp_file_template_With_numbers_image = NamedTemporaryFile(suffix='.png')  # this is a file object
    template_with_numbers_image.save(temp_file_template_With_numbers_image.name, format="png")  # save the content to temp

    colors_image = create_color_ref_images(colors_arr, din_format, template_image)
    temp_files_colors_image = []
    for image in colors_image:
        temp_file_colors_image = NamedTemporaryFile(suffix='.png')  # this is a file object
        image.save(temp_file_colors_image.name, format="png")  # save the content to temp
        temp_files_colors_image.append(temp_file_colors_image)

    din_input = get_dimensions(reduced_image, din_format)
    layout_fun = img2pdf.get_layout_fun(din_input)

    with open(file_name, "wb") as f:
        f.write(img2pdf.convert(temp_file_reduced_image.name, temp_file_template_image, temp_file_template_With_numbers_image,*temp_files_colors_image,
                                layout_fun=layout_fun))

    temp_file_reduced_image.close()
    temp_file_template_image.close()
    template_with_numbers_image.close()
    for temp_file in temp_files_colors_image:
        temp_file.close()


def get_dimensions(image, din_format):
    from model.ImageManipulation import ImageManipulation

    width, height = ImageManipulation.get_size_indices(image)
    return img2pdf.mm_to_pt(DIN_FORMAT[din_format][width]), img2pdf.mm_to_pt(DIN_FORMAT[din_format][height])


# https://stackoverflow.com/questions/14088375/how-can-i-convert-rgb-to-cmyk-and-vice-versa-in-python
def rgb_to_cmyk(r, g, b):
    cmyk_scale = 100
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / 255.
    m = 1 - g / 255.
    y = 1 - b / 255.

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c * cmyk_scale, m * cmyk_scale, y * cmyk_scale, k * cmyk_scale


def combined_percentages_of_cmyk(c, m, y, k):
    white = 0
    if sum([c, m, y, k]) == 0:
        return 0, 0, 0, 0, 100
    elif sum([c, m, y]) < 300:
        white = 100 - k
    percentage_sum = sum([c, m, y, k, white])
    cyan_percentage = (c / percentage_sum) * 100
    magenta_percentage = (m / percentage_sum) * 100
    yellow_percentage = (y / percentage_sum) * 100
    key_percentage = (k / percentage_sum) * 100
    white_percentage = (white / percentage_sum) * 100

    return cyan_percentage, magenta_percentage, yellow_percentage, key_percentage, white_percentage


def create_color_mixture_string(color_label, color):
    cyan, magenta, yellow, key = rgb_to_cmyk(color[0], color[1], color[2])
    cyan_percentage, magenta_percentage, yellow_percentage, key_percentage, white_percentage = combined_percentages_of_cmyk(
        int(cyan),
        int(magenta),
        int(yellow),
        int(key))

    return "Label Nr.: " + str(color_label) + "\n\n" \
           + "Cyan: " + "{0:.2f}".format(round(cyan_percentage, 2)) + " %\n" \
           + "Magenta: " + "{0:.2f}".format(round(magenta_percentage, 2)) + " %\n" \
           + "Yellow: " + "{0:.2f}".format(round(yellow_percentage, 2)) + " %\n" \
           + "Black: " + "{0:.2f}".format(round(key_percentage, 2)) + " %\n" \
           + "(White: " + "{0:.2f}".format(round(white_percentage, 2)) + " %)\n"
