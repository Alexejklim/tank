# -*- coding: utf-8 -*-

import argparse
import json
import logging
import logging.config
import os
import sys
import traceback

import six

class DummyUtil:
    def __init__(self, config):
        pass

    def run(self):
        pass


class UtilLauncher:
    def __init__(self):
        self.path = os.path.realpath(sys.argv[0])
        self.directory = os.path.dirname(self.path)
        self.logger = None
        pass

    def getDefaultConfigPath(self):
        return self.directory + "/config.conf"

    def getConfigOverrideSection(self, config):
        return config

    def addArgumentsToParser(self, parser):
        pass

    def createUtil(self, config):
        return DummyUtil(config)

    def Run(self, changeDir = False):
        if changeDir:
            os.chdir(self.directory)

        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--config", default=self.getDefaultConfigPath(), help="Config file location")

        self.addArgumentsToParser(parser)

        args = vars(parser.parse_args())

        config = {}

        with open(args['config'], 'r') as configFile:
            config = json.load(configFile)

        logConfig = config['Logging']
        logConfig['version'] = 1
        logging.config.dictConfig(logConfig)

        self.logger = logging.getLogger("Main")

        try:
            self.logger.info("New instance started with command line {0}".format(sys.argv))
            config = config['Settings']

            self.logger.info("Args is {0}".format(args))
            self.logger.info("Config is {0}".format(config))

            override = self.getConfigOverrideSection(config)

            for (name, value) in six.iteritems(args):
                if value is not None:
                    override[name] = value

            self.logger.info("Effective config is {0}".format(config))

            self.logger.info("Creating runnable")
            runnable = self.createUtil(config)

            try:
                self.logger.info("Executing runnable")
                runnable.run()
            except Exception as ex:
                self.logger.error("Exception caught: {0}\n{1}".format(ex, traceback.format_exc()))

            self.logger.info("Instance ended")

        except Exception as ex:
            self.logger.error("Exception caught: {0}\n{1}".format(ex, traceback.format_exc()))