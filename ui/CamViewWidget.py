from PyQt4 import QtGui
from PyQt4 import QtCore

import time

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, GstVideo
GObject.threads_init()
Gst.init(None)


class CamViewWidget(QtGui.QWidget):

    """Form for Streaming a CamViewWidget"""
    def __init__(self, parent = None):
        super(CamViewWidget, self).__init__(parent)
        self.display = QtGui.QWidget()
        self.windowId = self.display.winId()
        self.setGeometry(300,300,640,480)
        self.setWindowTitle("CamViewWidget Streaming")

        self.port = 5000

    def setUpGst(self):

        self.CamViewWidgetPipe = Gst.Pipeline()

        # Create Gst Elements
        self.udpsrc = Gst.ElementFactory.make('udpsrc', None)
        self.capsFilter = Gst.ElementFactory.make('capsfilter', None)
        self.rtph264depay = Gst.ElementFactory.make('rtph264depay', None)
        self.avdec_h264 = Gst.ElementFactory.make('avdec_h264', None)
        self.videoconvert = Gst.ElementFactory.make('videoconvert', None)
        self.autovideosink = Gst.ElementFactory.make('autovideosink', None)

        self.udpsrc.set_property('port', self.port)
        cameraCaps = Gst.Caps.from_string('application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264')
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
        self.CamViewWidgetPipe.set_state(Gst.State.PLAYING)
