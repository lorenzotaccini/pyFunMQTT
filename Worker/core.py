# class that groups all the little pieces and utilities and make them work togheter generating a definitive worker
# object
import threading
import time

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
        self.watchdog = Wd(self)  # instantiate watchdog on config file (not started yet)
        self.watchdog_thread = threading.Thread(target=self.watchdog.watch)

    def spawn_worker(self):
        self.watchdog_thread.start()
        self.mqttc.start()

    # reloads only necessary objects and restarts the new MQTT client. Typically called when changes are detected
    # in the config file by the watchdog
    def reload(self):
        self.mqttc.stop(False)
        self.yaml_data = Yl(self.configfile_name).load()
        self.mqttc = MQTTClient(self.yaml_data, self.toolbox)
        self.mqttc.start()
        print("session reloaded with modified configuration file.")


if __name__ == "__main__":
    worker = MQTTWorker()
    worker.spawn_worker()
    #worker2 = MQTTWorker()
    #worker2.spawn_worker()
    for thread in threading.enumerate():
        print(thread.name)
    while True:
        time.sleep(1)
