import os
import sys
import threading
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# not using watchdog library as of now, it was resulting in the watchdog thread being unable to detect file changes
class ConfigFileWatchdog:
    def __init__(self, spawner):
        self.__spawner = spawner
        self.filename = self.__spawner.configfile_name
        self.last_modified_time = self.__get_last_modified_time()
        self.actual_conf = self.__spawner.yaml_data
        self.stop_flag = threading.Event()

    def __get_last_modified_time(self):
        try:
            if os.path.exists(self.filename):
                return os.path.getmtime(self.filename)
            else:
                raise FileNotFoundError()
        except FileNotFoundError:
            logger.critical(f"{self.filename} does not exist.")
            sys.exit(-1)

    def __check_apply_modification(self):
        current_modified_time = self.__get_last_modified_time()
        if current_modified_time != self.last_modified_time:
            new_conf = self.__spawner.load_current_config()
            if new_conf != self.actual_conf:
                # Get the current time
                self.actual_conf = new_conf

                logger.warning('Changes detected in configuration file. RELOADING SESSION')
                self.__spawner.reload(self.actual_conf)

        self.last_modified_time = current_modified_time

    def watch(self):
        logger.info('----- watchdog is now detecting changes on file ' + self.filename + '-----')
        while True:
            if self.stop_flag.is_set():
                logger.info('stopping watchdog...')
                return True
            self.stop_flag.wait(int(self.__spawner.watchdog_interval))
            self.__check_apply_modification()
