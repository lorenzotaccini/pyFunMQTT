# class that groups all the little pieces and utilities and make them work togheter generating a definitive worker
# object
import sys
import threading
import time

from Utils.MQTT.client import MQTTClient
from Utils.OnFiles.configfile_watchdog import ConfigFileWatchdog as Wd
from Utils.OnFiles.yaml_loader_full import YamlLoader as Yl
import Utils.UserFunctions.toolbox as t

import Utils.cli as cli


class Spawner:
    def __init__(self):
        self.run_args = cli.CLI()  # arguments from program call in command line
        self.configfile_name = self.run_args.args.configfile
        self.yaml_data = []  # arguments for selected config YAML file
        self.watchdog = Wd(self)  # instantiate watchdog on config file (not started yet)
        self.watchdog_thread = threading.Thread(target=self.watchdog.watch)
        self.watchdog_thread.start()
        self.watchdog_stop_event = threading.Event()
        self.worker_list = []  # list containing all clients actually running

    def get_config(self, dynamic: bool = True):
        if dynamic:
            self.yaml_data = [doc for doc in Yl(self.configfile_name).load()]
        return self.yaml_data

    # spawn as many clients as required from configuration file
    def spawn_all(self):
        for conf in self.get_config():
            self.__spawn_single(conf)
        print(f'clients list: {self.worker_list}')

    # spawn a single client. configuration data structure is required in the arguments
    def __spawn_single(self, conf: dict):
        new_mqclient = MQTTClient(conf, t.MethodToolBox())
        self.worker_list.append(new_mqclient)
        new_mqclient.start()

    def reload(self):
        for c in self.worker_list:
            c.stop()
        self.worker_list = []
        self.spawn_all()

    def shutdown(self):
        print('Shutting down...')
        self.watchdog_stop_event.set()  # send shutdown signal to watchdog
        self.watchdog_thread.join()
        for c in self.worker_list:
            c.stop()
        print('all clients have been shutdown, now quitting...')
        sys.exit(1)


if __name__ == "__main__":
    s = Spawner()
    s.spawn_all()
    for thread in threading.enumerate():
        print(thread.name)
    while True:
        time.sleep(1)