# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ControlWidget.ui'
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

class Ui_ControlWidget(object):
    def setupUi(self, ControlWidget):
        ControlWidget.setObjectName(_fromUtf8("BatteryState"))
        ControlWidget.resize(433, 307)
        self.verticalLayout = QtGui.QVBoxLayout(ControlWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.comboJoystick = QtGui.QComboBox(ControlWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboJoystick.sizePolicy().hasHeightForWidth())
        self.comboJoystick.setSizePolicy(sizePolicy)
        self.comboJoystick.setObjectName(_fromUtf8("comboJoystick"))
        self.horizontalLayout_2.addWidget(self.comboJoystick)
        self.btnSaveParams = QtGui.QPushButton(ControlWidget)
        self.btnSaveParams.setObjectName(_fromUtf8("btnSaveParams"))
        self.horizontalLayout_2.addWidget(self.btnSaveParams)
        self.btnLoadParams = QtGui.QPushButton(ControlWidget)
        self.btnLoadParams.setObjectName(_fromUtf8("btnLoadParams"))
        self.horizontalLayout_2.addWidget(self.btnLoadParams)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.vlAxes = QtGui.QVBoxLayout()
        self.vlAxes.setObjectName(_fromUtf8("vlAxes"))
        self.horizontalLayout.addLayout(self.vlAxes)
        self.vlMixers = QtGui.QVBoxLayout()
        self.vlMixers.setObjectName(_fromUtf8("vlMixers"))
        self.horizontalLayout.addLayout(self.vlMixers)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ControlWidget)
        QtCore.QMetaObject.connectSlotsByName(ControlWidget)

    def retranslateUi(self, ControlWidget):
        self.btnSaveParams.setText(_translate("ControlWidget", "Save params", None))
        self.btnLoadParams.setText(_translate("ControlWidget", "Load params", None))

