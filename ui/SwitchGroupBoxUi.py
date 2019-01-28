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

class Ui_SwitchGroupBox(object):
    def setupUi(self, SwitchGroupBox):
        SwitchGroupBox.setObjectName(_fromUtf8("SwitchGroupBox"))
        SwitchGroupBox.resize(392, 67)
        self.horizontalLayout = QtGui.QHBoxLayout(SwitchGroupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkToggle = QtGui.QCheckBox(SwitchGroupBox)
        self.checkToggle.setObjectName(_fromUtf8("checkToggle"))
        self.horizontalLayout.addWidget(self.checkToggle)
        self.labelButton = QtGui.QLabel(SwitchGroupBox)
        self.labelButton.setObjectName(_fromUtf8("labelButton"))
        self.horizontalLayout.addWidget(self.labelButton)
        self.comboButton = QtGui.QComboBox(SwitchGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboButton.sizePolicy().hasHeightForWidth())
        self.comboButton.setSizePolicy(sizePolicy)
        self.comboButton.setObjectName(_fromUtf8("comboButton"))
        self.horizontalLayout.addWidget(self.comboButton)
        self.label = QtGui.QLabel(SwitchGroupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.buttonState = QtGui.QPushButton(SwitchGroupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.buttonState.setFont(font)
        self.buttonState.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonState.setCheckable(False)
        self.buttonState.setChecked(False)
        self.buttonState.setFlat(True)
        self.buttonState.setObjectName(_fromUtf8("buttonState"))
        self.horizontalLayout.addWidget(self.buttonState)

        self.retranslateUi(SwitchGroupBox)
        QtCore.QMetaObject.connectSlotsByName(SwitchGroupBox)

    def retranslateUi(self, SwitchGroupBox):
        self.checkToggle.setText(_translate("SwitchGroupBox", "Toggle", None))
        self.labelButton.setText(_translate("SwitchGroupBox", "Button:", None))
        self.label.setText(_translate("SwitchGroupBox", "State:", None))
        self.buttonState.setText(_translate("SwitchGroupBox", "OFF", None))

