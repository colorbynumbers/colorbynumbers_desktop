# Created by Lionel Kornberger at 2019-04-01
from model.ExtendedImage import ExtendedImage
from model.ExtendedImageManipulation import ExtendedImageManipulation
from Observable import Observable


class Controller(Observable):

    def __init__(self, ui, canvas):
        super(Controller,self).__init__()

        self.ui = ui
        self.canvas = canvas
        self.img = None

        self.register_observer(self.ui)

    def open_image(self, path):
        try:
            from PIL import Image
            self.img = ExtendedImage(Image.open(path))
            self.notify_observers(self.img)
        except OSError as err:
            self.notify_observers(str(err))
            return

    def get_image_size(self):
        if self.img:
            return self.img.size
        else:
            return 0, 0

    def compute_canvas(self):
        self.img = ExtendedImageManipulation.reduce_colors(image=self.img, color_amount=8)
        self.img = ExtendedImageManipulation.refine_edge(image=self.img)
        self.notify_observers(self.img)
