# Created by Lionel Kornberger at 2019-04-01
from model.ImageManipulation import ImageManipulation
from model.Export import export
from Observable import Observable


class Controller(Observable):

    def __init__(self, ui, canvas):
        super(Controller, self).__init__()

        self.ui = ui
        self.canvas = None
        self.img = None
        self.img_reduced = None

        self.register_observer(self.ui)

    def open_image(self, path):
        try:
            from PIL import Image
            self.img = Image.open(path)
            self.img = ImageManipulation.convert_gray_to_rgb(self.img)
            self.img_reduced = None
            self.notify_observers((self.img, self.img_reduced, self.canvas), tag="image")
        except OSError as err:
            self.notify_observers(str(err), tag="message")
            return

    def get_image_size(self):
        if self.img:
            return self.img.size
        else:
            return 0, 0

    def compute_canvas(self, n_colors, print_size, min_surface, is_aggressive=False):
        if self.img:
            self.img_reduced = ImageManipulation.reduce_colors(image=self.img, n_colors=n_colors)
            self.img_reduced = ImageManipulation.refine_edge(image=self.img_reduced,
                                                             is_aggressive=is_aggressive)
            self.notify_observers((self.img, self.img_reduced, self.canvas), tag="reduced")
        else:
            self.notify_observers("No Photo opened!\nPlease open a photo first.", tag="message")

    def export(self, din_format, file_name=""):
        if self.canvas:
            export(self.img, din_format, file_name)
        else:
            self.notify_observers(str("No Template generated!\nPlease start computation of template first."))
