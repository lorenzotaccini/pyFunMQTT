# class that groups all the little pieces and utilities and make them work togheter generating a definitive worker object

from Utils.MQTT.client import MQTTClient
from Utils.OnFiles.configfile_watchdog import ConfigFileWatchdog as Wd
from Utils.OnFiles.yaml_loader import YamlLoader as Yl
import Utils.UserFunctions.toolbox as t

import Utils.cli as cli


class MQTTWorker:
    def __init__(self):
        self.run_args = cli.CLI()  # arguments from program call in command line
        self.configfile_name = self.run_args.args.configfile
        self.toolbox = t.MethodToolBox()  # generate toolbox of functions
        self.yaml_data = Yl(self.configfile_name).load()  # arguments for selected config YAML file
        self.mqttc = MQTTClient(self.yaml_data, self.toolbox)  # instantiate mqtt custom client (not started yet)

    def spawn_worker(self):
        watchdog = Wd(self.configfile_name,)  # instantiate watchdog on config file (not started yet)
