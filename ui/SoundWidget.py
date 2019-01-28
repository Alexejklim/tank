import time
import threading
from PyQt4 import QtGui
from PyQt4 import QtCore

from SoundWidgetUi import *


class SoundWidget(QtGui.QWidget):
    def __init__(self, soundClient, parent=None):
        super(SoundWidget, self).__init__(parent)
        self.ui = Ui_SoundWidget()
        self.ui.setupUi(self)

        self.soundClient = soundClient

        self.connect(self, QtCore.SIGNAL('onUpdateStatistics()'), self.onUpdateStatistics)

        self.connect(self.ui.btnSendStartStop, QtCore.SIGNAL('clicked()'), self.sendStartStop)
        self.connect(self.ui.btnReceiveStartStop, QtCore.SIGNAL('clicked()'), self.receiveStartStop)

        for rate in [8000, 11025, 16000, 22050, 32000, 44100, 48000]:
            self.ui.comboSendRate.addItem(str(rate))
            self.ui.comboReceiveRate.addItem(str(rate))

        self.thread = None

    def isSendStarted(self):
        return self.soundClient.getSendStatus() is not None

    def isReceiveStarted(self):
        return self.soundClient.getReceiveStatus() is not None

    def sendStartStop(self):
        if self.isSendStarted():
            self.stopSend()
        else:
            self.startSend()

    def receiveStartStop(self):
        if self.isReceiveStarted():
            self.stopReceive()
        else:
            self.startReceive()

    def checkThread(self):
        if self.thread is None and (self.isSendStarted() or self.isReceiveStarted()):
            self.stopThread = False
            self.thread = threading.Thread(target=self.threadProc, name="SoundStatisticsThread")
            self.thread.daemon = True
            self.thread.start()

        if self.thread is not None and not self.isSendStarted() and not self.isReceiveStarted():
            self.stopThread = True
            self.thread.join()
            self.thread = None

    def stopSend(self):
        self.soundClient.stopSend()
        self.checkThread()
        self.ui.btnSendStartStop.setText("Start")
        self.ui.labelSendStatus.setText("")

    def stopReceive(self):
        self.soundClient.stopReceive()
        self.checkThread()
        self.ui.btnReceiveStartStop.setText("Start")
        self.ui.labelReceiveStatus.setText("")

    def startSend(self):
        rate = int(self.ui.comboSendRate.currentText())
        self.soundClient.startSend(rate)
        self.checkThread()
        self.ui.btnSendStartStop.setText("Stop")

    def startReceive(self):
        rate = int(self.ui.comboReceiveRate.currentText())
        self.soundClient.startReceive(rate)
        self.checkThread()
        self.ui.btnReceiveStartStop.setText("Stop")

    def closeEvent(self, event):
        self.stopSend()
        self.stopReceive()
        QtGui.QWidget.closeEvent(self, event)

    def onUpdateStatistics(self):
        sendStat = self.soundClient.getSendStatus()
        recvStat = self.soundClient.getReceiveStatus()

        sendText = ""
        recvText = ""

        if sendStat is not None:
            for name, value in sendStat.iteritems():
                sendText += "{0}: {1}\n".format(name, value)

        if recvStat is not None:
            for name, value in recvStat.iteritems():
                recvText += "{0}: {1}\n".format(name, value)

        self.ui.labelSendStatus.setText(sendText)
        self.ui.labelReceiveStatus.setText(recvText)

    def threadProc(self):
        while not self.stopThread:
            self.emit(QtCore.SIGNAL('onUpdateStatistics()'))
            time.sleep(0.5)
