# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created: Tue Nov 28 16:01:38 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(658, 429)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.widgetLayout = QtGui.QHBoxLayout(self.frame_2)
        self.widgetLayout.setMargin(0)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.pushButton_2 = QtGui.QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.widgetLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtGui.QPushButton(self.frame_2)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.widgetLayout.addWidget(self.pushButton_3)
        self.pushButton = QtGui.QPushButton(self.frame_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.widgetLayout.addWidget(self.pushButton)
        self.tempBox = QtGui.QDoubleSpinBox(self.frame_2)
        self.tempBox.setDecimals(3)
        self.tempBox.setMinimum(0.001)
        self.tempBox.setMaximum(15.0)
        self.tempBox.setSingleStep(0.2)
        self.tempBox.setObjectName(_fromUtf8("tempBox"))
        self.widgetLayout.addWidget(self.tempBox)
        self.checkBox = QtGui.QCheckBox(self.frame_2)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.widgetLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtGui.QCheckBox(self.frame_2)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.widgetLayout.addWidget(self.checkBox_2)
        self.checkBox_3 = QtGui.QCheckBox(self.frame_2)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.widgetLayout.addWidget(self.checkBox_3)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame_3 = QtGui.QFrame(self.frame)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.plotLayout = QtGui.QVBoxLayout(self.frame_3)
        self.plotLayout.setSpacing(0)
        self.plotLayout.setMargin(0)
        self.plotLayout.setObjectName(_fromUtf8("plotLayout"))
        self.horizontalLayout.addWidget(self.frame_3)
        self.verticalSlider = QtGui.QSlider(self.frame)
        self.verticalSlider.setProperty("value", 50)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.horizontalLayout.addWidget(self.verticalSlider)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.play)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.pause)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.force)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), MainWindow.hideUp)
        QtCore.QObject.connect(self.checkBox_2, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), MainWindow.hideDown)
        QtCore.QObject.connect(self.checkBox_3, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), MainWindow.slicing)
        QtCore.QObject.connect(self.verticalSlider, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), MainWindow.setSlicing)
        QtCore.QObject.connect(self.tempBox, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), MainWindow.setT)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_2.setText(_translate("MainWindow", "START", None))
        self.pushButton_3.setText(_translate("MainWindow", "PAUSE", None))
        self.pushButton.setText(_translate("MainWindow", "thermalize(force)", None))
        self.tempBox.setSuffix(_translate("MainWindow", " K", None))
        self.checkBox.setText(_translate("MainWindow", "Hide Up", None))
        self.checkBox_2.setText(_translate("MainWindow", "Hide Down", None))
        self.checkBox_3.setText(_translate("MainWindow", "slice", None))

