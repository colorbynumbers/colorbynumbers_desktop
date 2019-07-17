# Created by Lionel Kornberger at 2019-04-07

from PySide2.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog, QMessageBox, QWidget, QGraphicsTextItem
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QRectF, Signal, Qt, QEvent, QThread, QObject
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

        self.computation_started = False

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
            if key == Qt.Key_Return and not self.computation_started:
                self.__start_computation()
            elif key == Qt.Key_Enter and not self.computation_started:
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
            self.__disable_ui(True)
            self.__set_computation_text()

            worker = ComputeCanvasWorker(self.ui.spinBoxNumberOfColors.value(),
                                         self.ui.comboBoxPrintSize.currentText(),
                                         self.ui.spinBoxMinSurfaceSize.value(),
                                         self.ui.checkBox.isChecked(), self.controller)  # no parent!
            self.controller.register_observer(worker)
            self.thread = QThread()
            worker.moveToThread(self.thread)
            worker.finished.connect(self.thread.quit)
            self.thread.started.connect(worker.run)
            self.thread.start()

    def __export(self):

        file_name = self.open_save_file_dialog() if self.controller.canvas else ""
        self.controller.export(self.ui.comboBoxPrintSize.currentText(), file_name=file_name)

    def display_image(self, img_data):
        self.__clear_scenes()
        self.__add_image_to_scene(self.scene_org, img_data[0])

        if img_data[1]:
            self.__add_image_to_scene(self.scene_reduced, img_data[1])
            self.__add_image_to_scene(self.scene_template, img_data[2])
            self.ui.tabWidget.setCurrentIndex(1)

    def __set_computation_text(self):
        self.scene_org = QGraphicsScene()
        self.scene_org.addText("It'll take a moment.")
        self.ui.graphicsViewOriginal.setScene(self.scene_org)
        self.ui.tabWidget.setCurrentIndex(0)
        self.computation_started = True
        self.resize_image()

    def __clear_scenes(self):
        self.scene_org = QGraphicsScene()
        self.scene_reduced = QGraphicsScene()
        self.scene_template = QGraphicsScene()
        self.ui.graphicsViewOriginal.setScene(self.scene_org)
        self.ui.graphicsViewReducedColors.setScene(self.scene_reduced)
        self.ui.graphicsViewTemplate.setScene(self.scene_template)

    def __disable_ui(self, boolean):
        self.ui.pushButtonStart.setDisabled(boolean)
        self.ui.pushButtonExport.setDisabled(boolean)
        self.ui.toolButtonOpenPhoto.setDisabled(boolean)
        self.ui.spinBoxNumberOfColors.setDisabled(boolean)
        self.ui.spinBoxMinSurfaceSize.setDisabled(boolean)
        self.ui.comboBoxPrintSize.setDisabled(boolean)
        self.ui.checkBox.setDisabled(boolean)
        self.ui.tabWidget.setDisabled(boolean)

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
            if self.computation_started:
                self.ui.graphicsViewOriginal.fitInView(QRectF(0, 0, self.scene_org.width(), self.scene_org.height()),
                                                       Qt.KeepAspectRatio)
            else:
                self.ui.graphicsViewOriginal.fitInView(QRectF(0, 0, self.controller.get_image_size()[0],
                                                              self.controller.get_image_size()[1]), Qt.KeepAspectRatio)
                self.ui.graphicsViewReducedColors.fitInView(QRectF(0, 0, self.controller.get_image_size()[0],
                                                                   self.controller.get_image_size()[1]),
                                                            Qt.KeepAspectRatio)
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

    def notify(self, update_data):
        self.computation_started = False
        self.__disable_ui(False)
        if isinstance(update_data, str):
            self.show_message(update_data)
        else:
            self.display_image(update_data)


class ComputeCanvasWorker(QObject, Observer):
    finished = Signal()
    images_computed = Signal(object)

    def __init__(self, n_colors, print_size, min_surface, is_aggressive, controller):
        QObject.__init__(self)
        self.n_colors = n_colors
        self.print_size = print_size
        self.min_surface = min_surface
        self.is_aggressive = is_aggressive
        self.controller = controller

    def run(self):
        self.controller.compute_canvas(n_colors=self.n_colors,
                                       min_surface=self.min_surface,
                                       is_aggressive=self.is_aggressive)
        self.finished.emit()

    def notify(self, update_data):
        self.images_computed.emit(update_data)
