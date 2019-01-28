# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TwoAxesGroupBox.ui'
#
# Created: Mon Oct 27 18:57:00 2014
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

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        GroupBox.setObjectName(_fromUtf8("GroupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(GroupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelAxis1ComboTitle = QtGui.QLabel(GroupBox)
        self.labelAxis1ComboTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelAxis1ComboTitle.setObjectName(_fromUtf8("labelAxis1ComboTitle"))
        self.horizontalLayout.addWidget(self.labelAxis1ComboTitle)
        self.comboAxis1 = QtGui.QComboBox(GroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboAxis1.sizePolicy().hasHeightForWidth())
        self.comboAxis1.setSizePolicy(sizePolicy)
        self.comboAxis1.setObjectName(_fromUtf8("comboAxis1"))
        self.horizontalLayout.addWidget(self.comboAxis1)
        self.labelAxis2ComboTitle = QtGui.QLabel(GroupBox)
        self.labelAxis2ComboTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelAxis2ComboTitle.setObjectName(_fromUtf8("labelAxis2ComboTitle"))
        self.horizontalLayout.addWidget(self.labelAxis2ComboTitle)
        self.comboAxis2 = QtGui.QComboBox(GroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboAxis2.sizePolicy().hasHeightForWidth())
        self.comboAxis2.setSizePolicy(sizePolicy)
        self.comboAxis2.setObjectName(_fromUtf8("comboAxis2"))
        self.horizontalLayout.addWidget(self.comboAxis2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pbarLeftEngine = QtGui.QProgressBar(GroupBox)
        self.pbarLeftEngine.setMinimum(-1000)
        self.pbarLeftEngine.setMaximum(1000)
        self.pbarLeftEngine.setProperty("value", 0)
        self.pbarLeftEngine.setFormat(_fromUtf8(""))
        self.pbarLeftEngine.setObjectName(_fromUtf8("pbarLeftEngine"))
        self.gridLayout.addWidget(self.pbarLeftEngine, 0, 1, 1, 1)
        self.labelAxis1ValueTitle = QtGui.QLabel(GroupBox)
        self.labelAxis1ValueTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelAxis1ValueTitle.setObjectName(_fromUtf8("labelAxis1ValueTitle"))
        self.gridLayout.addWidget(self.labelAxis1ValueTitle, 0, 0, 1, 1)
        self.labelAxis2ValueTitle = QtGui.QLabel(GroupBox)
        self.labelAxis2ValueTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelAxis2ValueTitle.setObjectName(_fromUtf8("labelAxis2ValueTitle"))
        self.gridLayout.addWidget(self.labelAxis2ValueTitle, 2, 0, 1, 1)
        self.progressBar_2 = QtGui.QProgressBar(GroupBox)
        self.progressBar_2.setMinimum(-1000)
        self.progressBar_2.setMaximum(1000)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setFormat(_fromUtf8(""))
        self.progressBar_2.setObjectName(_fromUtf8("progressBar_2"))
        self.gridLayout.addWidget(self.progressBar_2, 2, 1, 1, 1)
        self.labelAxis1Value = QtGui.QLabel(GroupBox)
        self.labelAxis1Value.setMinimumSize(QtCore.QSize(40, 0))
        self.labelAxis1Value.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAxis1Value.setObjectName(_fromUtf8("labelAxis1Value"))
        self.gridLayout.addWidget(self.labelAxis1Value, 0, 2, 1, 1)
        self.labeAxis2Value = QtGui.QLabel(GroupBox)
        self.labeAxis2Value.setMinimumSize(QtCore.QSize(40, 0))
        self.labeAxis2Value.setAlignment(QtCore.Qt.AlignCenter)
        self.labeAxis2Value.setObjectName(_fromUtf8("labeAxis2Value"))
        self.gridLayout.addWidget(self.labeAxis2Value, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(GroupBox)
        QtCore.QMetaObject.connectSlotsByName(GroupBox)

    def retranslateUi(self, GroupBox):
        self.labelAxis1ComboTitle.setText(_translate("GroupBox", "Move axis:", None))
        self.labelAxis2ComboTitle.setText(_translate("GroupBox", "Turn axis:", None))
        self.labelAxis1ValueTitle.setText(_translate("GroupBox", "Left engine:", None))
        self.labelAxis2ValueTitle.setText(_translate("GroupBox", "Right engine:", None))
        self.labelAxis1Value.setText(_translate("GroupBox", "0", None))
        self.labeAxis2Value.setText(_translate("GroupBox", "0", None))

