# Created by Lionel Kornberger at 2019-04-01

import sys
from PySide2.QtWidgets import QApplication

from view.MainWindow import MainWindow
from controller.Controller import Controller
from model.Canvas import Canvas

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

    canvas = Canvas(0, 0)
    controller = Controller(ui, canvas)

    ui.set_controller(controller)

    sys.exit(app.exec_())
