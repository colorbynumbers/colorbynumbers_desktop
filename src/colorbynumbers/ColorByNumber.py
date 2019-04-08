# Created by Lionel Kornberger at 2019-04-01

import sys
from PySide2.QtWidgets import QApplication

from model.Canvas import Canvas
from view.MainWindow import MainWindow

# ToDo create GUI and Controller and Model

app = QApplication(sys.argv)
window = MainWindow()
window.show()

can = Canvas(64, 32)
print(can)

sys.exit(app.exec_())
