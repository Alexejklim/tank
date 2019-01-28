# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SoundWidget.ui'
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

class Ui_SoundWidget(object):
    def setupUi(self, SoundWidget):
        SoundWidget.setObjectName(_fromUtf8("SoundWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(SoundWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(SoundWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboSendRate = QtGui.QComboBox(self.groupBox)
        self.comboSendRate.setObjectName(_fromUtf8("comboSendRate"))
        self.verticalLayout.addWidget(self.comboSendRate)
        self.btnSendStartStop = QtGui.QPushButton(self.groupBox)
        self.btnSendStartStop.setObjectName(_fromUtf8("btnSendStartStop"))
        self.verticalLayout.addWidget(self.btnSendStartStop)
        self.labelSendStatus = QtGui.QLabel(self.groupBox)
        self.labelSendStatus.setMinimumSize(QtCore.QSize(200, 200))
        self.labelSendStatus.setText(_fromUtf8(""))
        self.labelSendStatus.setObjectName(_fromUtf8("labelSendStatus"))
        self.verticalLayout.addWidget(self.labelSendStatus)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(SoundWidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.comboReceiveRate = QtGui.QComboBox(self.groupBox_2)
        self.comboReceiveRate.setObjectName(_fromUtf8("comboReceiveRate"))
        self.verticalLayout_2.addWidget(self.comboReceiveRate)
        self.btnReceiveStartStop = QtGui.QPushButton(self.groupBox_2)
        self.btnReceiveStartStop.setObjectName(_fromUtf8("btnReceiveStartStop"))
        self.verticalLayout_2.addWidget(self.btnReceiveStartStop)
        self.labelReceiveStatus = QtGui.QLabel(self.groupBox_2)
        self.labelReceiveStatus.setMinimumSize(QtCore.QSize(200, 200))
        self.labelReceiveStatus.setText(_fromUtf8(""))
        self.labelReceiveStatus.setObjectName(_fromUtf8("labelReceiveStatus"))
        self.verticalLayout_2.addWidget(self.labelReceiveStatus)
        self.horizontalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(SoundWidget)
        QtCore.QMetaObject.connectSlotsByName(SoundWidget)

    def retranslateUi(self, SoundWidget):
        SoundWidget.setWindowTitle(_translate("SoundWidget", "Form", None))
        self.groupBox.setTitle(_translate("SoundWidget", "Send sound", None))
        self.btnSendStartStop.setText(_translate("SoundWidget", "Start", None))
        self.groupBox_2.setTitle(_translate("SoundWidget", "Receive sound", None))
        self.btnReceiveStartStop.setText(_translate("SoundWidget", "Start", None))

