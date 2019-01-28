from PyQt4 import QtGui
from PyQt4 import QtCore

from AxisMixerGroupBoxUi import *


class AxisMixerGroupBox(QtGui.QGroupBox):
    def __init__(self, axisMixer, parent=None):
        super(AxisMixerGroupBox, self).__init__(parent)

        self.ui = Ui_AxisMixerGroupBox()
        self.ui.setupUi(self)

        self.axisMixer = axisMixer

        titles = self.axisMixer.getTitles()

        self.setTitle(titles['title'])

        self.ui.labelAxis1ComboTitle.setText(titles['axis1'] + " axis:")
        self.ui.labelAxis2ComboTitle.setText(titles['axis2'] + " axis:")
        self.ui.labelAxis1ValueTitle.setText(titles['value1'] + ":")
        self.ui.labelAxis2ValueTitle.setText(titles['value2'] + ":")

        self.getParamsFromMixer()

        self.connect(self, QtCore.SIGNAL('onAxisUpdate( float, float )'), self.updateAxisValue)
        self.connect(self.ui.comboAxis1, QtCore.SIGNAL('currentIndexChanged( int )'), self.onSelectAxis)
        self.connect(self.ui.comboAxis2, QtCore.SIGNAL('currentIndexChanged( int )'), self.onSelectAxis)

        self.axisMixer.EvAxisMove += self.onAxisMove

    def getParamsFromMixer(self):
        self.ui.comboAxis1.clear()
        self.ui.comboAxis2.clear()
        for axisId, axis in self.axisMixer.getAvailableAxes().iteritems():
            self.ui.comboAxis1.insertItem(axisId, axis.getName())
            self.ui.comboAxis2.insertItem(axisId, axis.getName())

        axis1Id, axis2Id = self.axisMixer.getAxes()

        if axis1Id is not None:
            self.ui.comboAxis1.setCurrentIndex(axis1Id)
        if axis2Id is not None:
            self.ui.comboAxis2.setCurrentIndex(axis2Id)

    def updateAxisValue(self, value1, value2):
        self.ui.pbarAxis1Value.setValue(int(value1 * 1000))
        self.ui.pbarAxis2Value.setValue(int(value2 * 1000))
        self.ui.labelAxis1Value.setText("{:.3}".format(value1))
        self.ui.labelAxis2Value.setText("{:.3}".format(value2))

    def onAxisMove(self, axis, value1, value2):
        self.emit(QtCore.SIGNAL('onAxisUpdate( float, float )'), value1, value2)

    def onSelectAxis(self, value):
        self.axisMixer.setAxes(self.ui.comboAxis1.currentIndex(), self.ui.comboAxis2.currentIndex())
