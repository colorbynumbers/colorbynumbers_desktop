# Created by Lionel Kornberger at 2019-04-07

from PySide2.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog, QMessageBox, QWidget
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QRectF, Signal, Qt, QEvent
from Observer import Observer
from view.ui_mainwindow import Ui_MainWindow
from Config import get_config


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
        self.ui.tabWidget.currentChanged.connect(self.resize_image)

        self.ui.toolButtonOpenPhoto.clicked.connect(self.__select_image)
        self.ui.pushButtonStart.clicked.connect(self.__start_computation)

        self.ui.pushButtonExport.clicked.connect(self.__export)

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
        file_dialog = QFileDialog()
        MainWindow.__set_file_dialog_options(file_dialog, get_config().getboolean('UI', 'NO_NATIVE_DIALOG'))

        path = file_dialog.getOpenFileName(
            self, 'Open File', " ../../",
            'Images (*.png *.svg *.jpg *.jpeg)',
            '')[0]
        if path:
            self.controller.open_image(path)
            self.ui.tabWidget.setCurrentIndex(0)
            self.resize_image()

    @staticmethod
    def __set_file_dialog_options(file_dialog, is_not_native_dialog):
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, is_not_native_dialog)

    def __start_computation(self):
        if self.controller:
            self.controller.compute_canvas(n_colors=self.ui.spinBoxNumberOfColors.value(),
                                           print_size=self.ui.comboBoxPrintSize.currentText(),
                                           min_surface=self.ui.spinBoxMinSurfaceSize.value(),
                                           is_aggressive=self.ui.checkBox.isChecked())
            self.controller.compute_template(min_surface=self.ui.spinBoxMinSurfaceSize.value())

    def __export(self):
        file_name = self.open_save_file_dialog() if self.controller.canvas else ""
        self.controller.export(self.ui.comboBoxPrintSize.currentText(), file_name=file_name)

    def display_image(self, img_data):
        self.__clear_scenes()
        self.__add_image_to_scene(self.scene_org, img_data[0])

    def display_reduced(self, img_data):
        if img_data[1]:
            self.__add_image_to_scene(self.scene_reduced, img_data[1])
            self.ui.tabWidget.setCurrentIndex(1)

    def display_template(self, img_data):
        self.__add_image_to_scene(self.scene_template, img_data[1])
        self.ui.tabWidget.setCurrentIndex(2)

    def __clear_scenes(self):
        self.scene_org = QGraphicsScene()
        self.scene_reduced = QGraphicsScene()
        self.scene_template = QGraphicsScene()
        self.ui.graphicsViewOriginal.setScene(self.scene_org)
        self.ui.graphicsViewReducedColors.setScene(self.scene_reduced)
        self.ui.graphicsViewTemplate.setScene(self.scene_template)

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
            self.ui.graphicsViewReducedColors.fitInView(QRectF(0, 0, self.controller.get_image_size()[0],
                                                               self.controller.get_image_size()[1]), Qt.KeepAspectRatio)
            self.ui.graphicsViewTemplate.fitInView(QRectF(0, 0, self.controller.get_image_size()[0],
                                                          self.controller.get_image_size()[1]), Qt.KeepAspectRatio)

    def open_save_file_dialog(self):
        file_dialog = QFileDialog()
        file_name = file_dialog.getSaveFileName(self, 'Save as PDF', " ../../",
                                                'PDF (*.pdf)',
                                                '')[0]
        return file_name

    @staticmethod
    def show_message(text):
        msgBox = QMessageBox()
        msgBox.setText(text)
        msgBox.exec_()

    def notify(self, update_data, tag):
        if isinstance(update_data, str):
            self.show_message(update_data)
        elif tag is "image":
            self.display_image(update_data)
        elif tag is "reduced":
            self.display_reduced(update_data)
        elif tag is "template":
            self.display_template(update_data)
