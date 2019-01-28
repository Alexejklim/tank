from PyQt4 import QtGui
from PyQt4 import QtCore

from InputAxisGroupBoxUi import *


class InputAxisGroupBox(QtGui.QGroupBox):
    def __init__(self, axis, parent=None):
        super(InputAxisGroupBox, self).__init__(parent)

        self.ui = Ui_InputAxisGroupBox()
        self.ui.setupUi(self)

        self.axis = axis

        self.connect(self.ui.sliderTrim, QtCore.SIGNAL('valueChanged( int )'), self.onTrimChanged)
        self.connect(self.ui.sliderGamma, QtCore.SIGNAL('valueChanged( int )'), self.onGammaChanged)
        self.connect(self.ui.checkInvert, QtCore.SIGNAL('stateChanged( int )'), self.onInvertChanged)

        self.connect(self, QtCore.SIGNAL('onAxisUpdate( float, float )'), self.updateAxisValue)

        self.getParamsFromAxis()

        self.axis.EvAxisMove += self.onAxisMove

    def getParamsFromAxis(self):
        self.setTitle(self.axis.getName())

        gamma, trim, invert = self.axis.getParams()

        self.ui.sliderTrim.setValue(self.trimToUi(trim))
        self.ui.sliderGamma.setValue(self.gammaToUi(gamma))

        self.ui.labelTrim.setText("{:.3}".format(trim))
        self.ui.labelGamma.setText("{:.3}".format(gamma))

        self.ui.checkInvert.setChecked(invert)

    def setParamsToAxis(self):
        gamma = self.gammaFromUi(self.ui.sliderGamma.value())
        trim = self.trimFromUi(self.ui.sliderTrim.value())
        invert = self.ui.checkInvert.checkState() == QtCore.Qt.Checked

        self.axis.setParams(gamma, trim, invert)

    def gammaFromUi(self, value):
        value = float(value) / 10.0

        if value < 0:
            value = -1.0 / (value - 1.0)
        else:
            value = value + 1.0

        return value

    def gammaToUi(self, value):
        if value < 1.0:
            value = -1.0 / value
        else:
            value = value - 1.0

        return int(value * 10.0)

    def trimFromUi(self, value):
        return float(value) / 1000.0

    def trimToUi(self, value):
        return int(value * 1000)

    def onTrimChanged(self, value):
        trim = self.trimFromUi(value)
        self.ui.labelTrim.setText("{:.3}".format(trim))
        self.setParamsToAxis()

    def onGammaChanged(self, value):
        gamma = self.gammaFromUi(value)
        self.ui.labelGamma.setText("{:.3}".format(gamma))
        self.setParamsToAxis()

    def onInvertChanged(self, state):
        self.setParamsToAxis()

    def updateAxisValue(self, newValue, newInputValue):
        self.ui.pbarInValue.setValue(int(newInputValue * 1000))
        self.ui.pbarOutValue.setValue(int(newValue * 1000))
        self.ui.labelInput.setText("{:.3}".format(newInputValue))
        self.ui.labelOutput.setText("{:.3}".format(newValue))

    def onAxisMove(self, axis, newValue, newInputValue):
        self.emit(QtCore.SIGNAL(('onAxisUpdate( float, float )')), newValue, newInputValue)
