from CommonClient import *
import logging

from python_modules.sound_utils import UdpPlayer
from python_modules.sound_utils import UdpRecorder


class SoundClient(CommonClient):
    def __init__(self, addr):
        CommonClient.__init__(self, addr, 'sound')
        host, port = addr
        self.host = host
        self.logger = logging.getLogger("SoundClient")
        self.udpPlayer = None
        self.udpRecorder = None
        
    def refreshStatus(self):
        CommonClient.refreshStatus(self)
        self.periodSize = self.status['period']
        
    def startReceive(self, sampleRate):
        if self.udpPlayer is not None:
            raise RuntimeError("Sound receiver already started")

        self.logger.debug("Starting receive")
        
        self.udpPlayer = UdpPlayer()
        self.udpPlayer.start("0.0.0.0", 0, sampleRate, self.periodSize)
        
        host, port = self.udpPlayer.getListenAddr()
        
        self.connector.requestAndCheck('sound', {'act': 'startSender', 'port': port, 'rate': sampleRate})
        self.logger.debug("Receive started")

    def stopReceive(self):
        if self.udpPlayer is None:
            return

        self.logger.debug("Stopping receive")
        self.udpPlayer.stop()
        self.udpPlayer = None
        self.connector.request('sound', {'act': 'stopSender'})
        self.logger.debug("Receive stopped")

    def getReceiveStatus(self):
        if self.udpPlayer is None:
            return None
        
        return self.udpPlayer.status()
    
    def startSend(self, sampleRate):
        if self.udpRecorder is not None:
            raise RuntimeError("Sound sender already started")
        
        self.logger.debug("Starting send")
        result = self.connector.requestAndCheck('sound', {'act': 'startReceiver', 'rate': sampleRate})
        
        port = result['port']
        
        self.udpRecorder = UdpRecorder()
        self.udpRecorder.start(self.host, port, sampleRate, self.periodSize)
        self.logger.debug("Send started")
        
    def stopSend(self):
        if self.udpRecorder is None:
            return

        self.logger.debug("Stopping send")
        self.udpRecorder.stop()
        self.udpRecorder = None
        self.connector.request('sound', {'act': 'stopReceiver'})
        self.logger.debug("Send stopped")

    def getSendStatus(self):
        if self.udpRecorder is None:
            return None
        
        return self.udpRecorder.status()

    def start(self):
        self.logger.debug("Starting")
        CommonClient.start(self)
        self.logger.debug("Started")
    
    def stop(self):
        self.logger.debug("Stopping")
        self.stopReceive()
        self.stopSend()
        CommonClient.stop(self)
        self.logger.debug("Stopped")
    