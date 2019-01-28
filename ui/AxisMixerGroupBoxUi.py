# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AxisMixerGroupBox.ui'
#
# Created: Mon Oct 27 18:56:58 2014
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

class Ui_AxisMixerGroupBox(object):
    def setupUi(self, AxisMixerGroupBox):
        AxisMixerGroupBox.setObjectName(_fromUtf8("AxisMixerGroupBox"))
        AxisMixerGroupBox.resize(343, 117)
        self.verticalLayout = QtGui.QVBoxLayout(AxisMixerGroupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelAxis1ComboTitle = QtGui.QLabel(AxisMixerGroupBox)
        self.labelAxis1ComboTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelAxis1ComboTitle.setObjectName(_fromUtf8("labelAxis1ComboTitle"))
        self.horizontalLayout.addWidget(self.labelAxis1ComboTitle)
        self.comboAxis1 = QtGui.QComboBox(AxisMixerGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboAxis1.sizePolicy().hasHeightForWidth())
        self.comboAxis1.setSizePolicy(sizePolicy)
        self.comboAxis1.setObjectName(_fromUtf8("comboAxis1"))
        self.horizontalLayout.addWidget(self.comboAxis1)
        self.labelAxis2ComboTitle = QtGui.QLabel(AxisMixerGroupBox)
        self.labelAxis2ComboTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelAxis2ComboTitle.setObjectName(_fromUtf8("labelAxis2ComboTitle"))
        self.horizontalLayout.addWidget(self.labelAxis2ComboTitle)
        self.comboAxis2 = QtGui.QComboBox(AxisMixerGroupBox)
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
        self.pbarAxis1Value = QtGui.QProgressBar(AxisMixerGroupBox)
        self.pbarAxis1Value.setMinimum(-1000)
        self.pbarAxis1Value.setMaximum(1000)
        self.pbarAxis1Value.setProperty("value", 0)
        self.pbarAxis1Value.setFormat(_fromUtf8(""))
        self.pbarAxis1Value.setObjectName(_fromUtf8("pbarAxis1Value"))
        self.gridLayout.addWidget(self.pbarAxis1Value, 0, 1, 1, 1)
        self.labelAxis1ValueTitle = QtGui.QLabel(AxisMixerGroupBox)
        self.labelAxis1ValueTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelAxis1ValueTitle.setObjectName(_fromUtf8("labelAxis1ValueTitle"))
        self.gridLayout.addWidget(self.labelAxis1ValueTitle, 0, 0, 1, 1)
        self.labelAxis2ValueTitle = QtGui.QLabel(AxisMixerGroupBox)
        self.labelAxis2ValueTitle.setMinimumSize(QtCore.QSize(80, 0))
        self.labelAxis2ValueTitle.setObjectName(_fromUtf8("labelAxis2ValueTitle"))
        self.gridLayout.addWidget(self.labelAxis2ValueTitle, 2, 0, 1, 1)
        self.pbarAxis2Value = QtGui.QProgressBar(AxisMixerGroupBox)
        self.pbarAxis2Value.setMinimum(-1000)
        self.pbarAxis2Value.setMaximum(1000)
        self.pbarAxis2Value.setProperty("value", 0)
        self.pbarAxis2Value.setFormat(_fromUtf8(""))
        self.pbarAxis2Value.setObjectName(_fromUtf8("pbarAxis2Value"))
        self.gridLayout.addWidget(self.pbarAxis2Value, 2, 1, 1, 1)
        self.labelAxis1Value = QtGui.QLabel(AxisMixerGroupBox)
        self.labelAxis1Value.setMinimumSize(QtCore.QSize(40, 0))
        self.labelAxis1Value.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAxis1Value.setObjectName(_fromUtf8("labelAxis1Value"))
        self.gridLayout.addWidget(self.labelAxis1Value, 0, 2, 1, 1)
        self.labelAxis2Value = QtGui.QLabel(AxisMixerGroupBox)
        self.labelAxis2Value.setMinimumSize(QtCore.QSize(40, 0))
        self.labelAxis2Value.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAxis2Value.setObjectName(_fromUtf8("labelAxis2Value"))
        self.gridLayout.addWidget(self.labelAxis2Value, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(AxisMixerGroupBox)
        QtCore.QMetaObject.connectSlotsByName(AxisMixerGroupBox)

    def retranslateUi(self, AxisMixerGroupBox):
        self.labelAxis1ComboTitle.setText(_translate("AxisMixerGroupBox", "Move axis:", None))
        self.labelAxis2ComboTitle.setText(_translate("AxisMixerGroupBox", "Turn axis:", None))
        self.labelAxis1ValueTitle.setText(_translate("AxisMixerGroupBox", "Left engine:", None))
        self.labelAxis2ValueTitle.setText(_translate("AxisMixerGroupBox", "Right engine:", None))
        self.labelAxis1Value.setText(_translate("AxisMixerGroupBox", "0", None))
        self.labelAxis2Value.setText(_translate("AxisMixerGroupBox", "0", None))

