#!/usr/bin/python2

from  python_modules.command_utils import HTTPCommandHandler
from  python_modules.command_utils import UDPCommandHandler
from  python_modules.common_utils import ServiceLauncher
from  python_modules.server_utils import DispatchedBackgroundHTTPServer
from  python_modules.server_utils import DispatchedBackgroundUDPServer
from  python_modules.threading_utils import MultiThreadingDispatcher

from GpioController import *
from SoundController import *
from ServoController import *
from SwitchController import *
from VideoController import *
from ArduinoController import *

class TankServer:
    def __init__(self, config):
        self.logger = logging.getLogger("TankServer")

        httpThreadsNumber = int(config['http_threads_number'])
        self.httpDispatcher = MultiThreadingDispatcher("HttpDispatcher", httpThreadsNumber)
        udpThreadsNumber = int(config['udp_threads_number'])
        self.udpDispatcher = MultiThreadingDispatcher("UdpDispatcher", udpThreadsNumber)

        self.httpHandler = HTTPCommandHandler()
        self.udpHandler = UDPCommandHandler()

        self.httpHandler.setHandler('ping', self.pingHandler)
        self.httpHandler.setHandler('status', self.statusHandler)
        self.httpHandler.setHandler('reset', self.resetHandler)

        self.udpHandler.setHandler('ping', self.pingHandler)
        self.udpHandler.setHandler('status', self.statusHandler)
        self.udpHandler.setHandler('reset', self.resetHandler)

        self.http_port = int(config['http_port'])
        self.httpServer = DispatchedBackgroundHTTPServer(('', self.http_port),
                                                         self.httpHandler.getRequestHandlerClass(), self.httpDispatcher)
        self.httpServer.allow_reuse_address = True

        self.udp_port = int(config['udp_port'])
        self.udpServer = DispatchedBackgroundUDPServer(('', self.udp_port), self.udpHandler.getRequestHandlerClass(),
                                                       self.udpDispatcher)

        self.servoController = ServoController(config['ServoController'])
        self.servoCommandHandler = ServoCommandHandler(self.servoController)
        self.httpHandler.setHandler('servo', self.servoCommandHandler.handleCommand)
        self.udpHandler.setHandler('servo', self.servoCommandHandler.handleCommand)

        self.gpioController = GpioController(config['GpioController'])
        self.gpioCommandHandler = GpioCommandHandler(self.gpioController)
        self.httpHandler.setHandler('gpio', self.gpioCommandHandler.handleCommand)
        self.udpHandler.setHandler('gpio', self.gpioCommandHandler.handleCommand)

        self.arduinoController = ArduinoController(config['ArduinoController'])
        self.switchController = SwitchController(config['SwitchController'])
        self.switchCommandHandler = SwitchCommandHandler(self.switchController)
        self.httpHandler.setHandler('switch', self.switchCommandHandler.handleCommand)
        self.udpHandler.setHandler('switch', self.switchCommandHandler.handleCommand)

        self.videoController = VideoController(config['VideoController'])
        self.videoCommandHandler = VideoCommandHandler(self.videoController)
        self.httpHandler.setHandler('video', self.videoCommandHandler.handleCommand)

        self.soundController = SoundController(config['SoundController'])
        self.soundCommandHandler = SoundCommandHandler(self.soundController)
        self.httpHandler.setHandler('sound', self.soundCommandHandler.handleCommand)
        self.udpHandler.setHandler('sound', self.soundCommandHandler.handleCommand)

        self.config = config

    def start(self):
        self.logger.info("Starting")
        self.httpDispatcher.start()
        self.udpDispatcher.start()
        self.httpServer.startServer()
        self.udpServer.startServer()
        self.gpioController.start()
        self.servoController.add_all_gpios(self.gpioController.getPinNames(), self.gpioController.setPinValue,
                                           self.gpioController.getPinValue, 'gpio')
        self.servoController.start()
        self.arduinoController.start()

        self.switchController.addAll(self.gpioController.getPinNames(), self.gpioController.setPinValue,
                                     self.gpioController.getPinValue, 'gpio')

        self.switchController.addSwitch('gunPower', self.arduinoController.setGunPower,
                                        self.arduinoController.getGunPower, 'arduino')
        self.switchController.addSwitch('gunFire', self.arduinoController.setGunFire, self.arduinoController.getGunFire,
                                        'arduino')
        self.switchController.start()

        self.videoController.start()
        self.soundController.start()
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.videoController.stop()
        self.soundController.stop()

        self.switchController.stop()
        self.servoController.stop()
        self.gpioController.stop()
        self.arduinoController.stop()

        self.httpServer.stopServer()
        self.udpServer.stopServer()
        self.httpDispatcher.stop()
        self.udpDispatcher.stop()
        self.logger.info("Stopped")

    def pingHandler(self, cmd, args):
        return True

    def getStatus(self):
        status = {'http_port': self.http_port, 'udp_port': self.udp_port,
                  'ServoController': self.servoController.getStatus(),
                  'GpioController': self.gpioController.getStatus(),
                  'VideoController': self.videoController.getStatus(),
                  'SoundController': self.soundController.getStatus(),
                  'ArduinoController': self.arduinoController.getStatus(),
                  'SwitchController': self.switchController.getStatus()}

        return status

    def statusHandler(self, cmd, args):
        return self.getStatus()

    def tankHandler(self, cmd, args):
        action = args.get('act')

        if action == 'status':
            return {'tankStatus': self.getStatus()}
        elif action == 'reset':
            self.stop()
            self.start()
            return True
        else:
            raise NotImplementedError("Wrong action: {0}".format(action))

    def resetHandler(self, cmd, args):
        self.stop()
        self.start()
        return True


if __name__ == "__main__":
    class Launcher(ServiceLauncher):
        def createService(self, config):
            return TankServer(config['TankServer'])

        def addArgumentsToParser(self, parser):
            parser.add_argument("--port", type=int, help="Port to listen")


    Launcher().Run()
