# Created by Lionel Kornberger at 2019-05-21
import img2pdf
from tempfile import NamedTemporaryFile

DIN_FORMAT = {
    "DIN A1": (594, 841),
    "DIN A2": (420, 594),
    "DIN A3": (297, 420),
    "DIN A4": (210, 297),
    "DIN A5": (148, 210)
}


def export(image, din_format, file_name):
    temp = NamedTemporaryFile(suffix='.png')  # this is a file object
    image.save(temp.name, format="png")  # save the content to temp

    din_input = get_dimensions(image, din_format)
    layout_fun = img2pdf.get_layout_fun(din_input)

    with open(file_name, "wb") as f:
        f.write(img2pdf.convert(temp.name, layout_fun=layout_fun))

    temp.close()


def get_dimensions(image, din_format):
    from model.ImageManipulation import ImageManipulation

    width, height = ImageManipulation.get_size_indicies(image)
    return img2pdf.mm_to_pt(DIN_FORMAT[din_format][width]), img2pdf.mm_to_pt(DIN_FORMAT[din_format][height])
