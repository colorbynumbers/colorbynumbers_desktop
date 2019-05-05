# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui',
# licensing of 'mainwindow.ui' applies.
#
# Created: Sat May  4 19:21:33 2019
#      by: pyside2-uic  running on PySide2 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
from sys import platform

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(933, 658)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayoutLeft = QtWidgets.QVBoxLayout()
        if platform == "darwin":
            self.verticalLayoutLeft.setSpacing(6)
        else:
            self.verticalLayoutLeft.setSpacing(8)
        self.verticalLayoutLeft.setObjectName("verticalLayoutLeft")
        self.labelOpenPhoto = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelOpenPhoto.sizePolicy().hasHeightForWidth())
        self.labelOpenPhoto.setSizePolicy(sizePolicy)
        self.labelOpenPhoto.setMinimumSize(QtCore.QSize(0, 22))
        self.labelOpenPhoto.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelOpenPhoto.setObjectName("labelOpenPhoto")
        self.verticalLayoutLeft.addWidget(self.labelOpenPhoto)
        self.labelNumberOfColors = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelNumberOfColors.sizePolicy().hasHeightForWidth())
        self.labelNumberOfColors.setSizePolicy(sizePolicy)
        self.labelNumberOfColors.setMinimumSize(QtCore.QSize(0, 26))
        self.labelNumberOfColors.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelNumberOfColors.setObjectName("labelNumberOfColors")
        self.verticalLayoutLeft.addWidget(self.labelNumberOfColors)
        self.labelPrintSize = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPrintSize.sizePolicy().hasHeightForWidth())
        self.labelPrintSize.setSizePolicy(sizePolicy)
        self.labelPrintSize.setMinimumSize(QtCore.QSize(0, 26))
        self.labelPrintSize.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelPrintSize.setObjectName("labelPrintSize")
        self.verticalLayoutLeft.addWidget(self.labelPrintSize)
        self.labelMinSurfaceSize = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMinSurfaceSize.sizePolicy().hasHeightForWidth())
        self.labelMinSurfaceSize.setSizePolicy(sizePolicy)
        self.labelMinSurfaceSize.setMinimumSize(QtCore.QSize(0, 24))
        self.labelMinSurfaceSize.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelMinSurfaceSize.setObjectName("labelMinSurfaceSize")
        self.verticalLayoutLeft.addWidget(self.labelMinSurfaceSize)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutLeft.addItem(spacerItem)
        self.pushButtonStart = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.verticalLayoutLeft.addWidget(self.pushButtonStart)
        self.horizontalLayout.addLayout(self.verticalLayoutLeft)
        self.verticalLayoutRight = QtWidgets.QVBoxLayout()
        self.verticalLayoutRight.setSpacing(8)
        self.verticalLayoutRight.setObjectName("verticalLayoutRight")
        self.toolButtonOpenPhoto = QtWidgets.QToolButton(self.centralwidget)
        self.toolButtonOpenPhoto.setMinimumSize(QtCore.QSize(0, 22))
        self.toolButtonOpenPhoto.setMaximumSize(QtCore.QSize(16777215, 22))
        self.toolButtonOpenPhoto.setObjectName("toolButtonOpenPhoto")
        self.verticalLayoutRight.addWidget(self.toolButtonOpenPhoto)
        self.spinBoxNumberOfColors = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBoxNumberOfColors.setMinimumSize(QtCore.QSize(0, 26))
        self.spinBoxNumberOfColors.setMaximumSize(QtCore.QSize(16777215, 26))
        self.spinBoxNumberOfColors.setMinimum(1)
        self.spinBoxNumberOfColors.setMaximum(100)
        self.spinBoxNumberOfColors.setProperty("value", 21)
        self.spinBoxNumberOfColors.setObjectName("spinBoxNumberOfColors")
        self.verticalLayoutRight.addWidget(self.spinBoxNumberOfColors)
        self.comboBoxPrintSize = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxPrintSize.sizePolicy().hasHeightForWidth())
        self.comboBoxPrintSize.setSizePolicy(sizePolicy)
        self.comboBoxPrintSize.setMinimumSize(QtCore.QSize(0, 26))
        self.comboBoxPrintSize.setMaximumSize(QtCore.QSize(16777215, 26))
        self.comboBoxPrintSize.setObjectName("comboBoxPrintSize")
        self.comboBoxPrintSize.addItem("")
        self.comboBoxPrintSize.addItem("")
        self.comboBoxPrintSize.addItem("")
        self.comboBoxPrintSize.addItem("")
        self.comboBoxPrintSize.addItem("")
        self.verticalLayoutRight.addWidget(self.comboBoxPrintSize)
        self.spinBoxMinSurfaceSize = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxMinSurfaceSize.sizePolicy().hasHeightForWidth())
        self.spinBoxMinSurfaceSize.setSizePolicy(sizePolicy)
        self.spinBoxMinSurfaceSize.setMinimumSize(QtCore.QSize(0, 24))
        self.spinBoxMinSurfaceSize.setMaximumSize(QtCore.QSize(16777215, 24))
        self.spinBoxMinSurfaceSize.setMinimum(1)
        self.spinBoxMinSurfaceSize.setMaximum(100)
        self.spinBoxMinSurfaceSize.setProperty("value", 21)
        self.spinBoxMinSurfaceSize.setObjectName("spinBoxMinSurfaceSize")
        self.verticalLayoutRight.addWidget(self.spinBoxMinSurfaceSize)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutRight.addItem(spacerItem1)
        self.pushButtonExport = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonExport.setObjectName("pushButtonExport")
        self.verticalLayoutRight.addWidget(self.pushButtonExport)
        self.horizontalLayout.addLayout(self.verticalLayoutRight)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabOriginal = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabOriginal.sizePolicy().hasHeightForWidth())
        self.tabOriginal.setSizePolicy(sizePolicy)
        self.tabOriginal.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabOriginal.setObjectName("tabOriginal")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabOriginal)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsViewOriginal = QtWidgets.QGraphicsView(self.tabOriginal)
        self.graphicsViewOriginal.setObjectName("graphicsViewOriginal")
        self.verticalLayout.addWidget(self.graphicsViewOriginal)
        self.tabWidget.addTab(self.tabOriginal, "")
        self.tabReducedColors = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabReducedColors.sizePolicy().hasHeightForWidth())
        self.tabReducedColors.setSizePolicy(sizePolicy)
        self.tabReducedColors.setObjectName("tabReducedColors")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabReducedColors)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.graphicsViewReducedColors = QtWidgets.QGraphicsView(self.tabReducedColors)
        self.graphicsViewReducedColors.setObjectName("graphicsViewReducedColors")
        self.verticalLayout_2.addWidget(self.graphicsViewReducedColors)
        self.tabWidget.addTab(self.tabReducedColors, "")
        self.tabTemplate = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabTemplate.sizePolicy().hasHeightForWidth())
        self.tabTemplate.setSizePolicy(sizePolicy)
        self.tabTemplate.setObjectName("tabTemplate")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabTemplate)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.graphicsViewTemplate = QtWidgets.QGraphicsView(self.tabTemplate)
        self.graphicsViewTemplate.setObjectName("graphicsViewTemplate")
        self.verticalLayout_3.addWidget(self.graphicsViewTemplate)
        self.tabWidget.addTab(self.tabTemplate, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Color Photo By Number", None, -1))
        self.labelOpenPhoto.setText(QtWidgets.QApplication.translate("MainWindow", "open photo", None, -1))
        self.labelNumberOfColors.setText(QtWidgets.QApplication.translate("MainWindow", "number of colors", None, -1))
        self.labelPrintSize.setText(QtWidgets.QApplication.translate("MainWindow", "print size", None, -1))
        self.labelMinSurfaceSize.setText(QtWidgets.QApplication.translate("MainWindow", "min. surface size", None, -1))
        self.pushButtonStart.setText(QtWidgets.QApplication.translate("MainWindow", "start", None, -1))
        self.toolButtonOpenPhoto.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.comboBoxPrintSize.setItemText(0, QtWidgets.QApplication.translate("MainWindow", "DIN A1", None, -1))
        self.comboBoxPrintSize.setItemText(1, QtWidgets.QApplication.translate("MainWindow", "DIN A2", None, -1))
        self.comboBoxPrintSize.setItemText(2, QtWidgets.QApplication.translate("MainWindow", "DIN A3", None, -1))
        self.comboBoxPrintSize.setItemText(3, QtWidgets.QApplication.translate("MainWindow", "DIN A4", None, -1))
        self.comboBoxPrintSize.setItemText(4, QtWidgets.QApplication.translate("MainWindow", "DIN A5", None, -1))
        self.comboBoxPrintSize.setCurrentText(QtWidgets.QApplication.translate("MainWindow", "DIN A4", None, -1))
        self.pushButtonExport.setText(QtWidgets.QApplication.translate("MainWindow", "export ...", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOriginal), QtWidgets.QApplication.translate("MainWindow", "Original", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabReducedColors), QtWidgets.QApplication.translate("MainWindow", "Reduced Colors", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTemplate), QtWidgets.QApplication.translate("MainWindow", "Template", None, -1))
        # self.spinBoxNumberOfColors.setKeyboardTracking(False)
        # self.spinBoxMinSurfaceSize.setKeyboardTracking(False)
