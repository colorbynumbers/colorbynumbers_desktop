# Created by Lionel Kornberger at 2019-04-07

from PySide2.QtWidgets import QMainWindow
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

