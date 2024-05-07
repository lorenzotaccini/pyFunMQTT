# class that groups all the little pieces and utilities and make them work togheter generating a definitive worker object

from Utils.MQTT.client import MQTTClient as mqc
from Utils.OnFiles.configfile_watchdog import ConfigFileWatchdog as wd
import Utils.UserFunctions.toolbox as t

import Utils.cli as cli


class MQTTWorker:
    def __init__(self):
        self.run_args = cli.CLI()
        self.toolbox= t.MethodToolBox()
        self.mqttc = mqc(self.run_args, self.toolbox)
