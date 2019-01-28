# -*- coding: utf-8 -*-

import logging
import httplib
import socket
import threading
import traceback
from CommonClient import CommonClient

__all__ = ['VideoClient']

# noinspection PyAttributeOutsideInit
class VideoClientSession:
    def __init__(self, name):
        self.name = "VideoClientSession[{0}]".format(name)
        self.logger = logging.getLogger(self.name)
        self.started = False

    def start(self, host, port, frameHandler):
        if self.started:
            raise RuntimeError("Already started")

        self.logger.debug("Starting")

        self.logger.debug("Binding UDP socket")
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.bind(("0.0.0.0", 0))

        (udpHost, udpPort) = udpSocket.getsockname()
        self.logger.debug("Socket bound to port {0}".format(udpPort))

        httpHost = "{0}:{1}".format(host, port)
        url = "/udp?port={0}".format(udpPort)

        self.logger.debug("Sending request to tinycamd {0}{1}".format(httpHost, url))

        conn = httplib.HTTPConnection(httpHost)
        conn.request("GET", url)
        resp = conn.getresponse()

        if resp.status != 200:
            udpSocket.close()
            conn.close()
            raise RuntimeError("Got HTTP error from tinycamd: {0} {1}".format(resp.status, resp.reason))

        udpSocket.settimeout(0.5)

        self.udpSocket = udpSocket
        self.httpConn = conn
        self.httpResp = resp
        self.handler = frameHandler

        self.logger.debug("Starting threads")

        self.httpThread = threading.Thread(target=self.httpThreadProc, name=self.name + ".Http")
        self.udpThread = threading.Thread(target=self.udpThreadProc, name=self.name + ".Udp")

        self.httpThread.daemon = True
        self.udpThread.daemon = True

        self.started = True
        self.httpThread.start()
        self.udpThread.start()

        self.logger.debug("Started")

    def stop(self):
        if not self.started:
            return

        self.logger.debug("Stopping")
        self.started = False

        self.httpThread.join()
        self.httpConn.close()
        self.httpConn = None
        self.httpResp = None
        self.httpThread = None
        self.logger.debug("HTTP stopped")

        self.udpThread.join()
        self.udpSocket.close()
        self.udpSocket = None
        self.udpThread = None
        self.logger.debug("UDP stopped")

        self.logger.debug("Stopped")

    def httpThreadProc(self):
        self.logger.debug("HTTP thread started")
        while self.started:
            try:
                self.httpResp.read(16)
            except Exception, ex:
                self.logger.error("Exception caught: {0}\n{1}".format(ex, traceback.format_exc()))

        self.logger.debug("HTTP thread stopped")

    @staticmethod
    def isFirstPacket(data):
        return data[0] == '\xFF' and data[1] == '\xD8'

    @staticmethod
    def isLastPacket(data):
        dataLen = len(data)

        if data[dataLen - 2] == '\xFF' and data[dataLen - 1] == '\xD9':
            return True

        if data[dataLen - 3] == '\xFF' and data[dataLen - 2] == '\xD9' and data[dataLen - 1] == '\xD9':
            return True

        return False

    def udpThreadProc(self):
        self.logger.debug("UDP thread started")

        frame = ""

        while self.started:
            try:
                data, addr = self.udpSocket.recvfrom(0xFFFF)

                dataLen = len(data)

                if dataLen < 2:
                    continue

                if self.isFirstPacket(data):
                    frame = data
                else:
                    frame = frame + data

                if self.isLastPacket(data):
                    self.handler(frame)
                    frame = ""

            except socket.timeout:
                pass
            except Exception, ex:
                self.logger.error("Exception caught: {0}\n{1}".format(ex, traceback.format_exc()))

        self.logger.debug("UDP thread stopped")


class VideoClient(CommonClient):
    def __init__(self, addr):
        CommonClient.__init__(self, addr, 'video')
        host, port = addr
        self.host = host
        self.logger = logging.getLogger("VideoClient")

        self.devices = {}
        self.captures = {}

    def refreshStatus(self):
        CommonClient.refreshStatus(self)
        self.devices = self.status['devices']

    def getDevices(self):
        return self.devices

    def startCapture(self, name, width, height, fps, frameHandler):
        if name not in self.devices:
            raise RuntimeError("Invalid name: {0}".format(name))

        if name in self.captures:
            raise RuntimeError("Capture already started at {0}".format(name))

        self.logger.debug("Starting capture at {0}".format(name))

        result = self.connector.requestAndCheck('video',
                                                {'act': 'startCapture', 'name': name, 'width': width, 'height': height,
                                                 'fps': fps})
        port = result['port']

        videoSession = VideoClientSession(name)

        try:
            self.logger.debug("Starting video session")
            videoSession.start(self.host, port, frameHandler)
        except Exception, e:
            self.logger.error(
                "Exception caught while starting video client session: {0}\n{1}".format(e, traceback.format_exc()))
            self.connector.requestAndCheck('video', {'act': 'stopCapture', 'name': name})
            raise e

        self.captures[name] = videoSession

    def stopCapture(self, name):
        if name not in self.captures:
            return

        self.logger.debug("Stopping capture at {0}".format(name))

        videoSession = self.captures.pop(name)
        videoSession.stop()
        self.connector.requestAndCheck('video', {'act': 'stopCapture', 'name': name})

        self.logger.debug("Capture stopped at {0}".format(name))

    def stopAllCaptures(self):
        self.logger.debug("Stopping all captures")
        for name in self.captures.keys():
            self.stopCapture(name)

    def stop(self):
        self.logger.debug("Stopping")
        self.stopAllCaptures()
        CommonClient.stop(self)
        self.logger.debug("Stopped")
