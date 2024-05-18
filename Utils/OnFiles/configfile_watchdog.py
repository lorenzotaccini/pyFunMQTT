import os
import time
from datetime import datetime


# not using watchdog library as of now, it was resulting in the watchdog thread being unable to detect file changes
class ConfigFileWatchdog:
    def __init__(self, spawner):
        self.spawner = spawner
        self.filename = self.spawner.configfile_name
        self.last_modified_time = self.__get_last_modified_time()
        self.actual_data = spawner.get_config(dynamic=False)
        self.stop_flag = False

    def __get_last_modified_time(self):
        if os.path.exists(self.filename):
            return os.path.getmtime(self.filename)
        else:
            raise FileNotFoundError(f"{self.filename} does not exist.")

    def __check_modification(self):
        current_modified_time = self.__get_last_modified_time()
        if current_modified_time != self.last_modified_time:
            # Get the current time
            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            new_data = self.spawner.get_config()
            print(f'-------- at time {formatted_time} --------')
            for i, (o_i, n_i) in enumerate(zip(self.actual_data, new_data)):
                print('loop')
                if not o_i == n_i:
                    print(f'detected changes in config file {self.filename}, document {i}')

            self.actual_data = new_data

            flag = input('do you want to reload the clients with the new configuration? [y/n] -> ')
            if flag == 'y' or flag == 'Y':
                print('aaaaaa')
                self.stop_flag = True

            self.last_modified_time = current_modified_time

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
