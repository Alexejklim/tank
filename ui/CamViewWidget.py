from PyQt4 import QtGui
from PyQt4 import QtCore

import time
import re

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, GstVideo
GObject.threads_init()
Gst.init(None)

class CamViewWidget(QtGui.QWidget):

    """Form for Streaming a CamViewWidget"""
    def __init__(self, videoClient, parent = None):
        super(CamViewWidget, self).__init__(parent)
        self.videoClient = videoClient
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("CamViewWidget Streaming")

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.addStretch(1)

        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setLayout(self.verticalLayout)

        self.btnStartStop = QtGui.QPushButton(self)
        self.btnStartStop.setObjectName("btnStartStop")
        self.horizontalLayout.addWidget(self.btnStartStop)

        self.comboDevice = QtGui.QComboBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboDevice.sizePolicy().hasHeightForWidth())
        self.comboDevice.setSizePolicy(sizePolicy)
        self.comboDevice.setObjectName("comboDevice")
        self.horizontalLayout.addWidget(self.comboDevice)

        self.comboMode = QtGui.QComboBox(self)
        self.comboMode.setObjectName("comboMode")
        self.horizontalLayout.addWidget(self.comboMode)


        self.spinFps = QtGui.QSpinBox(self)
        self.spinFps.setMinimum(1)
        self.spinFps.setMaximum(30)
        self.spinFps.setProperty("value", 15)
        self.spinFps.setObjectName("spinFps")
        self.horizontalLayout.addWidget(self.spinFps)

        self.bitrate = QtGui.QSpinBox(self)
        self.bitrate.setMinimum(100000)
        self.bitrate.setMaximum(10000000)
        self.bitrate.setProperty("value", 1000000)
        self.bitrate.setObjectName("bitrate")
        self.horizontalLayout.addWidget(self.bitrate)

        self.labelStatus = QtGui.QLabel(self)
        self.labelStatus.setText("")
        self.labelStatus.setObjectName("labelStatus")
        self.verticalLayout.addWidget(self.labelStatus)


        self.horizontalLayout.addStretch(1)
        self.connect(self.comboDevice, QtCore.SIGNAL('currentIndexChanged(int)'), self.deviceChanged)
        self.connect(self.btnStartStop, QtCore.SIGNAL('clicked()'), self.startStop)
        self.refreshDevices()
        self.started = False

        self.comboMode.addItem('640x480')
        self.comboMode.addItem('1280x960')
        self.comboMode.addItem('320x240')

    def refreshDevices(self):
        self.videoClient.refreshStatus()
        self.comboDevice.clear()
        self.devices = []

        for (name, device) in self.videoClient.getDevices().iteritems():
            self.devices.append(device)
            self.comboDevice.addItem(name)

    def deviceChanged(self, index):
        self.deviceName = str(self.comboDevice.itemText(index))
        self.device = self.devices[index]

    def startStop(self):
        if self.started:
            self.stop()
        else:
            self.start()

    def start(self):
        if self.started:
            return

        name = self.deviceName
        mode = re.split(r'x', str(self.comboMode.currentText()))
        width = mode[0]
        height = mode[1]
        fps = self.spinFps.value()
        bitrate = self.bitrate.value()
        host = self.videoClient.host
        self.port = self.videoClient.startCapture(name, width, height, bitrate, fps, host)
        self.started = True
        self.comboMode.setDisabled(self.started)
        self.comboDevice.setDisabled(self.started)
        self.spinFps.setDisabled(self.started)
        self.btnStartStop.setText("Stop")
        self.startPrev()
        self.tick = time.time()

    def stop(self):
        if not self.started:
            return

        name = self.deviceName
        self.videoClient.stopCapture(name)
        self.started = False
        self.comboMode.setDisabled(self.started)
        self.comboDevice.setDisabled(self.started)
        self.spinFps.setDisabled(self.started)
        self.btnStartStop.setText("Start")

    def closeEvent(self, event):
        self.stop()
        QtGui.QWidget.closeEvent(self, event)

    def setupGst(self):
        self.CamViewWidgetPipe = Gst.Pipeline()
        # Create Gst Elements
        self.udpsrc = Gst.ElementFactory.make('udpsrc', None)
        self.capsFilter = Gst.ElementFactory.make('capsfilter', None)
        self.rtph264depay = Gst.ElementFactory.make('rtph264depay', None)
        self.avdec_h264 = Gst.ElementFactory.make('avdec_h264', None)
        self.videoconvert = Gst.ElementFactory.make('videoconvert', None)
        self.autovideosink = Gst.ElementFactory.make('autovideosink', None)
        self.udpsrc.set_property('port', self.port)
        cameraCaps = Gst.Caps.from_string(
            'application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264')
        self.capsFilter.set_property('caps', cameraCaps)
        self.autovideosink.set_property('sync', False)

        self.CamViewWidgetPipe.add(self.udpsrc)
        self.CamViewWidgetPipe.add(self.capsFilter)
        self.CamViewWidgetPipe.add(self.rtph264depay)
        self.CamViewWidgetPipe.add(self.avdec_h264)
        self.CamViewWidgetPipe.add(self.videoconvert)
        self.CamViewWidgetPipe.add(self.autovideosink)

        self.udpsrc.link(self.capsFilter)
        self.capsFilter.link(self.rtph264depay)
        self.rtph264depay.link(self.avdec_h264)
        self.avdec_h264.link(self.videoconvert)
        self.videoconvert.link(self.autovideosink)

        bus =  self.CamViewWidgetPipe.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message)

    def on_sync_message(self, bus, message):
        if message.get_structure().get_name() == 'prepare-window-handle':
            message.src.set_property('force-aspect-ratio', True)
            message.src.set_window_handle(self.winId().__int__())

    def startPrev(self):
        self.setupGst()
        self.CamViewWidgetPipe.set_state(Gst.State.PLAYING)
