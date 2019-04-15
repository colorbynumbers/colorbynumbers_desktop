# Created by Lionel Kornberger at 2019-04-01
from model.ExtendedImage import ExtendedImage
from model.ExtendedImageManipulation import ExtendedImageManipulation


class Controller:

    def __init__(self, ui, canvas):
        self.ui = ui
        self.canvas = canvas
        self.img = None

    def open_image(self, path):
        try:
            from PIL import Image
            self.img = ExtendedImage(Image.open(path))
            self.ui.display_image(self.img)
        except OSError as err:
            self.ui.show_message(str(err))
            return

    def get_image_size(self):
        if self.img:
            return self.img.size
        else:
            return 0, 0

    def compute_canvas(self):
        self.img = ExtendedImageManipulation.reduce_colors(image=self.img, color_amount=8)
        self.img = ExtendedImageManipulation.refine_edge(image=self.img)
        self.ui.display_image(self.img)
