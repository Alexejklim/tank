import logging

from python_modules.sound_utils import UdpPlayer
from python_modules.sound_utils import UdpRecorder


class SoundController:
    def __init__(self, config):
        self.logger = logging.getLogger("SoundController")
        self.periodSize = config['periodSize']

        self.udpPlayer = None
        self.udpRecorder = None

    def start(self):
        self.logger.info("Starting")
        pass
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.stopReceiveSound()
        self.stopSendSound()
        self.logger.info("Stopped")

    def startReceiveSound(self, host="0.0.0.0", port=0, sampleRate=8000):
        if self.udpPlayer is not None:
            raise RuntimeError("Sound receiver already started")

        self.logger.info("Starting receive")

        self.udpPlayer = UdpPlayer()
        self.udpPlayer.start(host, port, sampleRate, self.periodSize)

        self.logger.info("Receive started")

        return self.udpPlayer.getListenAddr()

    def stopReceiveSound(self):
        if self.udpPlayer is None:
            return

        self.logger.info("Stopping receive")
        self.udpPlayer.stop()
        self.udpPlayer = None
        self.logger.info("Receive stopped")

    def startSendSound(self, host, port, sampleRate=8000):
        if self.udpRecorder is not None:
            raise RuntimeError("Sound sender already started")

        self.logger.info("Starting send")
        self.udpRecorder = UdpRecorder()
        self.udpRecorder.start(host, port, sampleRate, self.periodSize)
        self.logger.info("Send started")

        return True

    def stopSendSound(self):
        if self.udpRecorder is None:
            return

        self.logger.info("Stopping send")
        self.udpRecorder.stop()
        self.udpRecorder = None
        self.logger.info("Send stopped")

    def getStatus(self):
        recvStatus = {'started': False}
        if self.udpPlayer is not None:
            recvStatus = self.udpPlayer.status()

        sendStatus = {'started': False}
        if self.udpRecorder is not None:
            sendStatus = self.udpRecorder.status()

        return {'period': self.periodSize, 'receiver': recvStatus, 'sender': sendStatus}


class SoundCommandHandler:
    def __init__(self, soundController):
        self.soundController = soundController

    def handleCommand(self, cmd, args):
        if cmd != 'sound':
            raise NotImplementedError("Wrong command: {0}".format(cmd))

        action = args.get('act')

        if action == 'startReceiver':
            sampleRate = int(args.get('rate', 8000))

            port = int(args.get('port', 0))
            host = args.get('host', "0.0.0.0")

            host, port = self.soundController.startReceiveSound(host, port, sampleRate)
            return {'host': host, 'port': port}

        if action == 'stopReceiver':
            self.soundController.stopReceiveSound()
            return True

        if action == 'startSender':
            sampleRate = int(args.get('rate', 8000))
            remoteAddr = args.get('_remoteAddr')

            host = None
            if remoteAddr is not None:
                host, port = remoteAddr

            host = args.get('host', host)
            port = int(args.get('port'))

            if port is None or host is None:
                raise RuntimeError("Host or port is not specified")

            self.soundController.startSendSound(host, port, sampleRate)
            return True

        if action == 'stopSender':
            self.soundController.stopSendSound()
            return True

        elif action == 'status':
            return {'soundStatus': self.soundController.getStatus()}

        elif action == 'start':
            self.soundController.start()
            return True
        elif action == 'stop':
            self.soundController.stop()
            return True

        else:
            raise NotImplementedError("Wrong action: {0}".format(action))
