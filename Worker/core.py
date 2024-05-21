import logging
import sys
import threading
import logging

from Utils.MQTT.client import MQTTClient
from Utils.OnFiles.configfile_watchdog import ConfigFileWatchdog as Wd
from Utils.OnFiles.yaml_loader_full import YamlLoader as Yl
import Utils.UserFunctions.toolbox as t


logger = logging.getLogger(__name__)


class Spawner:
    def __init__(self, run_args):
        self.run_args = run_args  # arguments from program call in command line
        self.configfile_name = self.run_args.args.configfile
        self.yaml_data = self.load_current_config()  # arguments for selected config YAML file
        self.watchdog_interval = self.run_args.args.w
        self.watchdog, self.watchdog_thread = self.__start_watchdog()
        self.worker_list = []  # list containing all clients actually running

    def load_current_config(self) -> [dict]:
        return [doc for doc in Yl(self.configfile_name).load()]

    # spawn as many clients as required from configuration file
    def spawn_all(self):
        for conf in self.yaml_data:
            self.__spawn_single(conf)

        logger.debug(f'clients list: {self.worker_list}')

    # spawn a single client. configuration data structure is required in the arguments
    def __spawn_single(self, conf: dict):
        new_mqclient = MQTTClient(conf, t.MethodToolBox())
        self.worker_list.append(new_mqclient)
        new_mqclient.start()

    def reload(self, config: [dict]):
        for c in self.worker_list:
            c.stop()
        self.worker_list = []
        self.yaml_data = config
        self.spawn_all()

    def shutdown(self):
        logger.info('Shutting down...')
        self.__stop_watchdog()  # send shutdown signal to watchdog
        for c in self.worker_list:
            c.stop()
        logger.info('all clients have been shutdown, now quitting...')
        sys.exit(1)

    def __start_watchdog(self) -> tuple[Wd, threading.Thread]:
        w = Wd(self)  # instantiate watchdog on config file (not started yet)
        w_t = threading.Thread(target=w.watch)
        w_t.start()
        return w, w_t

    def __stop_watchdog(self):
        self.watchdog.stop_flag.set()
        self.watchdog_thread.join()
