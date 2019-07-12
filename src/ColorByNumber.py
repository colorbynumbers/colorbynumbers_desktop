# Created by Lionel Kornberger at 2019-04-01

import sys
from PySide2.QtWidgets import QApplication

from view.MainWindow import MainWindow
from controller.Controller import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

    controller = Controller(ui)

    ui.set_controller(controller)

    sys.exit(app.exec_())
