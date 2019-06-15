# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\old_windows\Desktop\TANK\tank-master\tank-master\tank\ui\CamViewWidget.ui'
#
# Created: Thu May 09 00:25:28 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CamViewWidget(object):
    def setupUi(self, CamViewWidget):
        CamViewWidget.setObjectName("CamViewWidget")
        CamViewWidget.resize(284, 63)
        self.verticalLayout = QtGui.QVBoxLayout(CamViewWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelImage = QtGui.QLabel(CamViewWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelImage.sizePolicy().hasHeightForWidth())
        self.labelImage.setSizePolicy(sizePolicy)
        self.labelImage.setFrameShape(QtGui.QFrame.Box)
        self.labelImage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelImage.setObjectName("labelImage")
        self.verticalLayout.addWidget(self.labelImage)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboDevice = QtGui.QComboBox(CamViewWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboDevice.sizePolicy().hasHeightForWidth())
        self.comboDevice.setSizePolicy(sizePolicy)
        self.comboDevice.setObjectName("comboDevice")
        self.horizontalLayout.addWidget(self.comboDevice)
        self.comboMode = QtGui.QComboBox(CamViewWidget)
        self.comboMode.setObjectName("comboMode")
        self.horizontalLayout.addWidget(self.comboMode)
        self.spinFps = QtGui.QSpinBox(CamViewWidget)
        self.spinFps.setMinimum(1)
        self.spinFps.setMaximum(30)
        self.spinFps.setProperty("value", 10)
        self.spinFps.setObjectName("spinFps")
        self.horizontalLayout.addWidget(self.spinFps)
        self.btnStartStop = QtGui.QPushButton(CamViewWidget)
        self.btnStartStop.setObjectName("btnStartStop")
        self.horizontalLayout.addWidget(self.btnStartStop)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelStatus = QtGui.QLabel(CamViewWidget)
        self.labelStatus.setText("")
        self.labelStatus.setObjectName("labelStatus")
        self.verticalLayout.addWidget(self.labelStatus)

        self.retranslateUi(CamViewWidget)
        QtCore.QMetaObject.connectSlotsByName(CamViewWidget)

    def retranslateUi(self, CamViewWidget):
        self.btnStartStop.setText(QtGui.QApplication.translate("CamViewWidget", "Start", None, QtGui.QApplication.UnicodeUTF8))

