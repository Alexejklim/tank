import logging
import os
import subprocess
import time


class ServoController:
    def __init__(self, config):
        self.logger = logging.getLogger("ServoController")
        
        self.servodPath = config['servodPath']
        self.ctrlFile = config['ctrlFile']

        self.minValue = config['minValue']
        self.maxValue = config['maxValue']

        self.servos = config['Servos']
        self.servod = None
        self.gpios = {}

        self.config = config;


    def start(self):
        if self.servod is not None:
            raise RuntimeError("Servo controller already started")

        self.logger.info("Starting")
                        
        pins = []
        n = 0
        for name in self.servos.iterkeys():
            servo = self.servos[name]
            if servo['type'] != 'gpio':
                pins.append(str(servo['pin']))
                servo['index'] = n
                n = n + 1
                self.servos[name] = servo
            
        pinList = ','.join(pins)
            
        args = [self.servodPath, '-f','--min={0}'.format(self.minValue), '--max={0}'.format(self.maxValue), '--p1pins={0}'.format(pinList)]
        
        self.logger.info("Starting servoblaster with args: {0}".format(args))
        self.servod = subprocess.Popen(args)
        self.logger.info("servoblaster started")

        time.sleep(3)

        self.logger.info("Setting initial values")
        for name in self.servos.iterkeys():
            servo = self.servos[name]
            if servo['type'] != 'gpio':
                self.setExactServoPosition(name)
                time.sleep(0.5)

        self.logger.info("Started")
        
    def stop(self):
        if self.servod is None:
            return

        self.logger.info("Stopping")
        self.servod.terminate()
        self.servod.wait()
        self.servod = None
        self.clear_gpios()
        self.logger.info("Stopped")
    
    def getServoPosition(self, name):
        if name not in self.servos:
            raise IndexError("Wrong servo name: {0}".format(name))
        
        return self.servos[name]['value']
        
    def getStatus(self):
        servoStatus = {}
        
        for name in self.servos.iterkeys():
            servoStatus[name] = self.servos[name].copy()
        
        return servoStatus

    def setExactServoPosition(self, name):
        if name not in self.servos:
            raise IndexError("Wrong servo name: {0}".format(name))

        servo = self.servos[name]

        with open(self.ctrlFile, "w") as f:
            f.write("{0}={1}\n".format(servo['index'], servo['value']))

    def setShiftServoPosition(self, name, sign):
        if name not in self.servos:
            raise IndexError("Wrong servo name: {0}".format(name))

        servo = self.servos[name]

        with open(self.ctrlFile, "w") as f:
            if sign != "":
                f.write("{0}={1}{2}\n".format(servo['index'], sign, servo['trim']))

    def setGPIOServoPosition(self, name, sign):
        if name not in self.servos:
            raise IndexError("Wrong servo name: {0}".format(name))

        servo = self.servos[name]

        if sign is "-":
            self.set_gpio_value(servo['pinnames']['run'], 0)
            self.set_gpio_value(servo['pinnames']['back'], 1)
        elif sign is "+":
            self.set_gpio_value(servo['pinnames']['run'], 1)
            self.set_gpio_value(servo['pinnames']['back'], 0)
        elif sign is "":
            self.set_gpio_value(servo['pinnames']['run'], 0)
            self.set_gpio_value(servo['pinnames']['back'], 0)
        else:
            raise ValueError("sign {0} not supports".format(sign))

    def setServoPosition(self, name, value):
        if name not in self.servos:
            raise IndexError("Wrong servo name: {0}".format(name))

        servo = self.servos[name]

        if value < -0.001:
            sign = "-"
        elif value > 0.001:
            sign = "+"
        else:
            sign = ""

        if servo['type'] == 'set':
            self.setExactServoPosition(name)

        elif servo['type'] == 'move':
            self.setShiftServoPosition(name,sign)

        elif servo['type'] == 'gpio':
            self.setGPIOServoPosition(name, sign)
        else:
            raise ValueError("servo-type {0} not supports".format(servo['type']))


    def setMany(self, positions):
        for name, value in positions.iteritems():
            self.setServoPosition(name, value)

    def add_all_gpios(self, names, setFunction, getFunction, type=None):
        for name in names:
            self.add_gpio(name, setFunction, getFunction, type)

    def add_gpio(self, name, setFunction, getFunction, type=None):
        if name in self.gpios:
            raise RuntimeError("gpio {0} already exists".format(name))

        self.gpios[name] = {'set': setFunction, 'get': getFunction, 'type': type}

    def set_gpio_value(self, name, value):
        if name not in self.gpios:
            raise RuntimeError("Wrong gpio name: {0}".format(name))

        gpio = self.gpios.get(name)
        gpio['set'](name, value)

    def get_gpio_value(self, name):
        if name not in self.gpios:
            raise RuntimeError("Wrong switch name: {0}".format(name))

        gpio = self.gpios.get(name)
        value = gpio['get'](name)

        return value

    def clear_gpios(self):
        self.logger.info("Clearing gpios")
        self.gpios.clear()

        
class ServoCommandHandler:
    def __init__(self, servoController):
        self.servoController = servoController

    def handleCommand(self, cmd, args):
        if cmd != 'servo':
            raise NotImplementedError("Wrong command: {0}".format(cmd))
        
        action = args.get('act')

        if action == 'set':
            name = args.get('name')
            value = round(float(args.get('value')))
            self.servoController.setServoPosition(name, value)
            
            if args.get('_protocol', '') == 'udp':
                return { '_noAnswer': True }
            
            return True

        elif action == 'setmany':
            values = args.get('values')
            
            servodict = {}

            for item in values.split(','):
                name, value = item.split(':', 1)
                servodict[name] = round(float(value))
                
            self.servoController.setMany(servodict)

            if args.get('_protocol', '') == 'udp':
                return { '_noAnswer': True }
            
            return True
            
            
        elif action == 'get':
            name = args.get('name')
            value = self.servoController.getServoPosition(name)
            return { 'servoName': name, 'servoValue': value }

        elif action == 'status':
            return { 'servoStatus': self.servoController.getStatus() }

        elif action == 'start':
            self.servoController.start()
            return True
        elif action == 'stop':
            self.servoController.stop()
            return True

        else:
            raise NotImplementedError("Wrong action: {0}".format(action))
        