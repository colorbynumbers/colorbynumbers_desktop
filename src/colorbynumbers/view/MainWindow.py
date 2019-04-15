# Created by Lionel Kornberger at 2019-04-07

from PySide2.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog, QMessageBox
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QRectF, Signal, Qt
from Observer import Observer
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Observer):
    resized = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.controller = None

        # slots
        self.resized.connect(self.resize_image)

        self.ui.toolButtonOpenPhoto.clicked.connect(self.__select_image)
        self.ui.pushButtonStart.clicked.connect(self.__start_computation)

        # TODO impelement slots for other Buttons

    def set_controller(self, controller):
        self.controller = controller

    def __select_image(self):
        path = QFileDialog.getOpenFileName(self, "Select Image")[0]
        if path:
            self.controller.open_image(path)

    def __start_computation(self):
        self.controller.compute_canvas()

    def display_image(self, img):
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.resize_image()
        pixmap = self.__pil_to_pixmap(img)
        self.scene.addPixmap(pixmap)

    @staticmethod
    def __pil_to_pixmap(img):
        if img.mode == "RGB":
            pass
        elif img.mode == "L":
            img = img.convert("RGBA")
        data = img.convert("RGBA").tobytes("raw", "BGRA")
        qim = QImage(data, img.size[0], img.size[1], QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)
        return pixmap

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def resize_image(self):
        if self.controller:
            self.ui.graphicsView.fitInView(QRectF(0, 0, self.controller.get_image_size()[0],
                                                  self.controller.get_image_size()[1]), Qt.KeepAspectRatio)
        self.scene.update()

    @staticmethod
    def show_message(text):
        msgBox = QMessageBox()
        msgBox.setText(text)
        msgBox.exec_()

    def notify(self, update_data):
        if isinstance(update_data, str):
            self.show_message(update_data)
        else:
            self.display_image(update_data)
