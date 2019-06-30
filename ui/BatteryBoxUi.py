# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SwitchGroupBox.ui'
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

class Ui_BatteryBox(object):
    def setupUi(self, BatteryBox):
        BatteryBox.setObjectName(_fromUtf8("BatteryBox"))
        BatteryBox.resize(392, 67)
        self.verticalLayout = QtGui.QVBoxLayout(BatteryBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pbarBattery = QtGui.QProgressBar(BatteryBox)
        self.pbarBattery.setMinimum(0)
        self.pbarBattery.setMaximum(100)
        self.pbarBattery.setProperty("value", 0)
        self.pbarBattery.setFormat(_fromUtf8(""))
        self.pbarBattery.setObjectName(_fromUtf8("pbarBattery"))
        self.gridLayout.addWidget(self.pbarBattery, 0, 1, 1, 1)

        self.labelBatteryTitle = QtGui.QLabel(BatteryBox)
        self.labelBatteryTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelBatteryTitle.setObjectName(_fromUtf8("labelBatteryTitle"))
        self.gridLayout.addWidget(self.labelBatteryTitle, 0, 0, 1, 1)
        self.labelBattery = QtGui.QLabel(BatteryBox)
        self.labelBattery.setMinimumSize(QtCore.QSize(40, 0))
        self.labelBattery.setAlignment(QtCore.Qt.AlignCenter)
        self.labelBattery.setObjectName(_fromUtf8("labelBattery"))
        self.gridLayout.addWidget(self.labelBattery, 0, 2, 1, 1)

        self.labelVoltageTitle = QtGui.QLabel(BatteryBox)
        self.labelVoltageTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelVoltageTitle.setObjectName(_fromUtf8("labelVoltageTitle"))
        self.gridLayout.addWidget(self.labelVoltageTitle, 1, 0, 1, 1)
        self.labelVoltage = QtGui.QLabel(BatteryBox)
        self.labelVoltage.setMinimumSize(QtCore.QSize(40, 0))
        self.labelVoltage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelVoltage.setObjectName(_fromUtf8("labelVoltage"))
        self.gridLayout.addWidget(self.labelVoltage, 1, 2, 1, 1)

        self.labelCurrentTitle = QtGui.QLabel(BatteryBox)
        self.labelCurrentTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelCurrentTitle.setObjectName(_fromUtf8("labelVoltageTitle"))
        self.gridLayout.addWidget(self.labelCurrentTitle, 2, 0, 1, 1)
        self.labelCurrent = QtGui.QLabel(BatteryBox)
        self.labelCurrent.setMinimumSize(QtCore.QSize(40, 0))
        self.labelCurrent.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCurrent.setObjectName(_fromUtf8("labelVoltage"))
        self.gridLayout.addWidget(self.labelCurrent, 2, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        self.retranslateUi(BatteryBox)
        QtCore.QMetaObject.connectSlotsByName(BatteryBox)

    def retranslateUi(self, BatteryBox):
        self.labelBatteryTitle.setText(_translate("BatteryBox", "Battery:", None))
        self.labelVoltageTitle.setText(_translate("BatteryBox", "Voltage:", None))
        self.labelCurrentTitle.setText(_translate("BatteryBox", "Current:", None))
        self.labelBattery.setText(_translate("Battery", "0", None))
        self.labelVoltage.setText(_translate("Voltage", "0", None))
        self.labelCurrent.setText(_translate("Current", "0", None))