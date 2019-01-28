import logging

from python_modules.common_utils import MulticastDelegate


class Switch:
    def __init__(self, controlClient, config):
        self.logger = logging.getLogger("Switch")

        self.switchState = False
        self.controlClient = controlClient
        self.button = None
        self.title = config['title']
        self.name = config['name']

        self.EvStateChanged = MulticastDelegate()

    def getTitle(self):
        return self.title

    def getName(self):
        return self.name

    def getState(self):
        return self.switchState

    def setState(self, state):
        self.switchState = state
        self.EvStateChanged(self, self.switchState)

    def onUpdateState(self, button, state):
        self.switchState = state
        self.EvStateChanged(self, self.switchState)

    def setButton(self, buttonId):
        if self.button is not None:
            self.button.EvStateChange -= self.onUpdateState

        self.button = None

        buttons = self.controlClient.getButtons()

        if buttonId is not None and buttons.has_key(buttonId):
            self.button = buttons[buttonId]
            self.button.EvStateChange += self.onUpdateState

    def getButton(self):
        buttonId = None
        if self.button is not None:
            buttonId = self.button.getId()
        return buttonId

    def setButtonDict(self, params):
        if params.has_key('button'):
            self.setButton(int(params['button']))

    def getButtonDict(self):
        buttonId = self.getButton()
        result = {}

        if buttonId is not None:
            result['button'] = buttonId

        return result

    def setToggle(self, toggle):
        if self.button is not None:
            self.button.setParams(toggle)

    def getToggle(self):
        toggle = False

        if self.button is not None:
            (toggle) = self.button.getParams()

        return toggle

    def getAvailableButtons(self):
        return self.controlClient.getButtons()
