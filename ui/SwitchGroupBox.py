from PyQt4 import QtGui
from PyQt4 import QtCore

from SwitchGroupBoxUi import *


class SwitchGroupBox(QtGui.QGroupBox):
    def __init__(self, switch, parent=None):
        super(SwitchGroupBox, self).__init__(parent)

        self.ui = Ui_SwitchGroupBox()
        self.ui.setupUi(self)

        self.switch = switch

        self.setTitle(self.switch.getTitle())

        self.ui.checkToggle.setChecked(switch.getToggle())

        self.ui.comboButton.clear()
        for buttonId, button in self.switch.getAvailableButtons().iteritems():
            self.ui.comboButton.insertItem(buttonId, button.getName())

        buttonId = self.switch.getButton()

        if buttonId is not None:
            self.ui.comboButton.setCurrentIndex(buttonId)

        self.switch.EvStateChanged += self.onSwitchStateChanged

        self.connect(self.ui.buttonState, QtCore.SIGNAL('clicked()'), self.onStateClick)
        self.connect(self.ui.checkToggle, QtCore.SIGNAL('stateChanged( int )'), self.onToggleChanged)
        self.connect(self, QtCore.SIGNAL('onUpdateState( bool )'), self.onUpdateState)
        self.connect(self.ui.comboButton, QtCore.SIGNAL('currentIndexChanged( int )'), self.onSelectButton)

    def onStateClick(self):
        self.switch.setState(not self.switch.getState())

    def onUpdateState(self, state):
        if state:
            self.ui.buttonState.setText("ON")
        else:
            self.ui.buttonState.setText("OFF")

    def onSwitchStateChanged(self, switch, state):
        self.emit(QtCore.SIGNAL('onUpdateState( bool )'), state)

    def onToggleChanged(self, state):
        self.switch.setToggle(state);

    def onSelectButton(self, value):
        self.switch.setButton(self.ui.comboButton.currentIndex())
