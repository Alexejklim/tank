import logging

from python_modules.common_utils import MulticastDelegate


class AxisMixer:
    def __init__(self, controlClient, config):
        self.logger = logging.getLogger("AxisMixer")

        self.a1 = float(config['Coeff']['a1'])
        self.a2 = float(config['Coeff']['a2'])

        self.b1 = float(config['Coeff']['b1'])
        self.b2 = float(config['Coeff']['b2'])

        self.titles = config['Titles']
        self.servos = config['Servos']

        self.value1 = 0
        self.value2 = 0

        self.axis1 = None
        self.axis2 = None

        self.controlClient = controlClient

        self.EvAxisMove = MulticastDelegate()

    def getTitles(self):
        return self.titles

    def getServoDict(self):
        return {self.servos['value1']: self.value1, self.servos['value2']: self.value2}

    def getValues(self):
        return self.value1, self.value2

    def onUpdateAxis(self, *args):
        self.value1, self.value2 = self.convert(self.axis1.getValue(), self.axis2.getValue())
        self.EvAxisMove(self, self.value1, self.value2)

    def getAvailableAxes(self):
        return self.controlClient.getAxes()

    def setAxes(self, axis1Id, axis2Id):
        if self.axis1 is not None:
            self.axis1.EvAxisMove -= self.onUpdateAxis

        if self.axis2 is not None:
            self.axis2.EvAxisMove -= self.onUpdateAxis

        axes = self.controlClient.getAxes()

        if axis1Id is not None:
            self.axis1 = axes[axis1Id]
            self.axis1.EvAxisMove += self.onUpdateAxis

        if axis2Id is not None:
            self.axis2 = axes[axis2Id]
            self.axis2.EvAxisMove += self.onUpdateAxis

    def getAxes(self):
        axis1Id = None
        axis2Id = None

        if self.axis1 is not None:
            axis1Id = self.axis1.getId()
        if self.axis2 is not None:
            axis2Id = self.axis2.getId()

        return axis1Id, axis2Id

    def setAxesDict(self, params):
        if params.has_key('axis1') and params.has_key('axis2'):
            self.setAxes(int(params['axis1']), int(params['axis2']))

    def getAxesDict(self):
        axis1Id, axis2Id = self.getAxes()
        result = {}

        if axis1Id is not None:
            result['axis1'] = axis1Id
        if axis2Id is not None:
            result['axis2'] = axis2Id
        return result

    def convert(self, value1, value2):
        result1 = self.a1 * value1 + self.a2 * value2
        result2 = self.b1 * value1 + self.b2 * value2

        if result1 > 1.0:
            result1 = 1.0
        elif result1 < -1.0:
            result1 = -1.0

        if result2 > 1.0:
            result2 = 1.0
        elif result2 < -1.0:
            result2 = -1.0

        return result1, result2
