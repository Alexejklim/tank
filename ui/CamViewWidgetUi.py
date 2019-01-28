# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CamViewWidget.ui'
#
# Created: Mon Oct 27 18:56:59 2014
#      by: PyQt4 UI code generator 4.11.2
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

class Ui_CamViewWidget(object):
    def setupUi(self, CamViewWidget):
        CamViewWidget.setObjectName(_fromUtf8("CamViewWidget"))
        CamViewWidget.resize(284, 63)
        self.verticalLayout = QtGui.QVBoxLayout(CamViewWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelImage = QtGui.QLabel(CamViewWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelImage.sizePolicy().hasHeightForWidth())
        self.labelImage.setSizePolicy(sizePolicy)
        self.labelImage.setFrameShape(QtGui.QFrame.Box)
        self.labelImage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelImage.setObjectName(_fromUtf8("labelImage"))
        self.verticalLayout.addWidget(self.labelImage)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboDevice = QtGui.QComboBox(CamViewWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboDevice.sizePolicy().hasHeightForWidth())
        self.comboDevice.setSizePolicy(sizePolicy)
        self.comboDevice.setObjectName(_fromUtf8("comboDevice"))
        self.horizontalLayout.addWidget(self.comboDevice)
        self.comboMode = QtGui.QComboBox(CamViewWidget)
        self.comboMode.setObjectName(_fromUtf8("comboMode"))
        self.horizontalLayout.addWidget(self.comboMode)
        self.spinFps = QtGui.QSpinBox(CamViewWidget)
        self.spinFps.setMinimum(1)
        self.spinFps.setMaximum(30)
        self.spinFps.setProperty("value", 10)
        self.spinFps.setObjectName(_fromUtf8("spinFps"))
        self.horizontalLayout.addWidget(self.spinFps)
        self.btnStartStop = QtGui.QPushButton(CamViewWidget)
        self.btnStartStop.setObjectName(_fromUtf8("btnStartStop"))
        self.horizontalLayout.addWidget(self.btnStartStop)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelStatus = QtGui.QLabel(CamViewWidget)
        self.labelStatus.setText(_fromUtf8(""))
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        self.verticalLayout.addWidget(self.labelStatus)

        self.retranslateUi(CamViewWidget)
        QtCore.QMetaObject.connectSlotsByName(CamViewWidget)

    def retranslateUi(self, CamViewWidget):
        self.btnStartStop.setText(_translate("CamViewWidget", "Start", None))

