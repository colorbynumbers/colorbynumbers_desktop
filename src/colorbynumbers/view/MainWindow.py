# Created by Lionel Kornberger at 2019-04-07

from PySide2.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog, QMessageBox, QWidget
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QRectF, Signal, Qt, QEvent
from Observer import Observer
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Observer):
    resized = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scene_org = QGraphicsScene()
        self.scene_reduced = QGraphicsScene()
        self.scene_template = QGraphicsScene()
        self.ui.graphicsViewOriginal.setScene(self.scene_org)

        self.controller = None

        # slots
        self.resized.connect(self.resize_image)

        self.ui.toolButtonOpenPhoto.clicked.connect(self.__select_image)
        self.ui.pushButtonStart.clicked.connect(self.__start_computation)

        self.installEventFilter(self)

    def eventFilter(self, widget, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Return:
                self.__start_computation()
            elif key == Qt.Key_Enter:
                self.__start_computation()
            return True
        return QWidget.eventFilter(self, widget, event)

    def set_controller(self, controller):
        self.controller = controller

    def __select_image(self):
        path = QFileDialog.getOpenFileName(self, "Select Image")[0]
        if path:
            self.controller.open_image(path)
            self.ui.tabWidget.setCurrentIndex(0)

    def __start_computation(self):
        if self.controller:
            self.controller.compute_canvas(n_colors=self.ui.spinBoxNumberOfColors.value(),
                                           print_size=self.ui.comboBoxPrintSize.currentText(),
                                           min_surface=self.ui.spinBoxMinSurfaceSize.value()
                                           )

    def display_image(self, img_data):
        self.ui.graphicsViewOriginal.setScene(self.scene_org)
        self.__add_image_to_scene(self.scene_org, img_data[0])
        self.resize_image()

        if img_data[1] and img_data[2]:
            self.ui.graphicsViewReducedColors.setScene(self.scene_reduced)
            self.__add_image_to_scene(self.scene_reduced, img_data[1])
            self.resize_image()

            self.ui.tabWidget.setCurrentIndex(1)

    def __add_image_to_scene(self, scene, image):
        pixmap = self.__pil_to_pixmap(image)
        scene.addPixmap(pixmap)

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
            self.ui.graphicsViewOriginal.fitInView(QRectF(0, 0, self.controller.get_image_size()[0],
                                                          self.controller.get_image_size()[1]), Qt.KeepAspectRatio)
        self.scene_org.update()
        self.scene_reduced.update()
        self.scene_template.update()

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
