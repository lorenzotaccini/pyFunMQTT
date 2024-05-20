import os
import sys
import threading
import time
from datetime import datetime


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
            print(f"{self.filename} does not exist.")
            sys.exit(-1)

    def __check_apply_modification(self):
        current_modified_time = self.__get_last_modified_time()
        if current_modified_time != self.last_modified_time:
            new_conf = self.__spawner.load_current_config()
            if new_conf != self.actual_conf:
                # Get the current time
                self.actual_conf = new_conf
                current_time = datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")

                flag = input('Changes detected in configuration file.\n'
                             'Do you want to reload all clients with the new configuration? [y/n] -> ')
                if flag == 'y' or flag == 'Y':
                    self.__spawner.reload(self.actual_conf)

        self.last_modified_time = current_modified_time

    def watch(self):
        print('----- watchdog is now detecting changes on file ' + self.filename + '-----')
        while True:
            if self.stop_flag.is_set():
                print('stopping watchdog...')
                return True
            self.stop_flag.wait(int(self.__spawner.watchdog_interval))
            self.__check_apply_modification()



'''
    def watch(self, interval=1):
        print('----- watchdog is now watching on file ' + self.filename + '-----')
        while True:
            while not self.stop_flag:
                print('alive')
                if self.spawner.watchdog_stop_event.is_set():
                    print('stopping watchdog...')
                    return True
                time.sleep(interval)
                self.__check_modification()
            print('now reloading')
            self.spawner.reload()
            self.stop_flag = False
'''

