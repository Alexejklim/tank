from PyQt4 import QtGui
from PyQt4 import QtCore

from AxisMixerGroupBox import *
from ControlWidgetUi import *
from InputAxisGroupBox import *
from SwitchGroupBox import *
from BatteryBox import *

class ControlWidget(QtGui.QWidget):
    def __init__(self, controlClient, parent=None):
        super(ControlWidget, self).__init__(parent)
        self.ui = Ui_ControlWidget()
        self.ui.setupUi(self)

        self.controlClient = controlClient

        hasJoystick = False

        for joyId, joyName in self.controlClient.getAvailableJoystics().iteritems():
            self.ui.comboJoystick.insertItem(joyId, joyName)
            hasJoystick = True

        self.connect(self.ui.comboJoystick, QtCore.SIGNAL('currentIndexChanged( int )'), self.onSelectJoystick)
        self.connect(self.ui.btnSaveParams, QtCore.SIGNAL('clicked()'), self.onSaveParams)
        self.connect(self.ui.btnLoadParams, QtCore.SIGNAL('clicked()'), self.onLoadParams)

        if hasJoystick:
            self.ui.comboJoystick.setCurrentIndex(0)
            self.onSelectJoystick(0)

    def onSelectJoystick(self, joyId):
        self.controlClient.selectJoystick(joyId)
        self.updateControls()

    def updateControls(self):

        for i in reversed(range(self.ui.vlAxes.count())):
            item = self.ui.vlAxes.itemAt(i)
            self.ui.vlAxes.removeItem(item)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        for i in reversed(range(self.ui.vlMixers.count())):
            item = self.ui.vlMixers.itemAt(i)
            self.ui.vlMixers.removeItem(item)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        for axisId, axis in self.controlClient.getAxes().iteritems():
            axisWidget = InputAxisGroupBox(axis, self)
            self.ui.vlAxes.addWidget(axisWidget)

        self.ui.vlAxes.addStretch()

        for mixer in self.controlClient.getMixers().itervalues():
            mixerWidget = AxisMixerGroupBox(mixer, self)
            self.ui.vlMixers.addWidget(mixerWidget)

        for switch in self.controlClient.getSwitches().itervalues():
            switchWidget = SwitchGroupBox(switch, self)
            self.ui.vlMixers.addWidget(switchWidget)

        BatteryWidget = BatteryBox(self.controlClient.arduinoClient,self)
        self.ui.vlMixers.addWidget(BatteryWidget)

        self.ui.vlMixers.addStretch()

    def onSaveParams(self):
        self.controlClient.saveParams()

    def onLoadParams(self):
        self.controlClient.loadParams()
        self.updateControls()
