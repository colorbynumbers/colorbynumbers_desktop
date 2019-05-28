# Created by Lionel Kornberger at 2019-04-01
from model.ExtendedImage import ExtendedImage
from model.ExtendedImageManipulation import ExtendedImageManipulation
from Observable import Observable


class Controller(Observable):

    def __init__(self, ui, canvas):
        super(Controller, self).__init__()

        self.ui = ui
        self.canvas = canvas
        self.img = None
        self.img_reduced = None

        self.register_observer(self.ui)

    def open_image(self, path):
        try:
            from PIL import Image
            self.img = ExtendedImage(Image.open(path))
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
            self.img_reduced = ExtendedImageManipulation.reduce_colors(image=self.img, n_colors=n_colors)
            self.img_reduced = ExtendedImageManipulation.refine_edge(image=self.img_reduced,
                                                                     is_aggressive=is_aggressive)
            self.notify_observers((self.img, self.img_reduced, self.canvas), tag="reduced")
        else:
            self.notify_observers("No Photo opened!\nPlease open a photo first.", tag="message")

    def compute_reduced(self):
        pass

    def compute_template(self, min_surface):
        img_detected = ExtendedImageManipulation.detect_edges(self.img_reduced, min_surface)
        self.notify_observers((self.img, img_detected, self.canvas), tag="template")
