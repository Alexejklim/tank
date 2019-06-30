from PyQt4 import QtGui
from PyQt4 import QtCore


from BatteryBoxUi import *


class BatteryBox(QtGui.QGroupBox):
    def __init__(self,arduinoClient, parent=None):
        super(BatteryBox, self).__init__(parent)
        self.ui = Ui_BatteryBox()
        self.ui.setupUi(self)
        self.arduinoClient = arduinoClient
        self.connect(self, QtCore.SIGNAL('onAxisUpdate'), self.updateBatteryValue)
        self.battery = arduinoClient.battery
        self.arduinoClient.EvBatteryMove += self.onBatteryMove


    def updateBatteryValue(self):
        self.ui.pbarBattery.setValue(self.battery['charge'])
        self.ui.labelBattery.setText(str(self.battery['charge']))
        self.ui.labelVoltage.setText("{:.3}".format(self.battery['voltage']))
        self.ui.labelCurrent.setText("{:.3}".format(self.battery['current']))

    def onBatteryMove(self):
        self.emit(QtCore.SIGNAL(('onAxisUpdate')))


