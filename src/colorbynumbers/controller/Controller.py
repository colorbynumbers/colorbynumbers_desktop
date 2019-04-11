# Created by Lionel Kornberger at 2019-04-01
from model.ExtendedImage import ExtendedImage


class Controller:

    def __init__(self, ui, canvas):
        self.ui = ui
        self.canvas = canvas
        self.img = None

    def open_image(self, path):
        try:
            self.img = ExtendedImage(path)
            self.ui.display_image(self.img)
        except OSError as err:
            self.ui.show_message(str(err))
            return

    def get_image_size(self):
        if self.img:
            return self.img.size
        else:
            return 0, 0
