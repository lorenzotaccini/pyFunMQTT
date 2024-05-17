import os
import time
from datetime import datetime


# not using watchdog library as of now, it was resulting in the watchdog thread being unable to detect file changes
class ConfigFileWatchdog:
    def __init__(self, spawner):
        self.spawner = spawner
        self.filename = self.spawner.configfile_name
        self.last_modified_time = self.get_last_modified_time()
        self.old_data = spawner.get_config()
        self.stop_flag = False

    def get_last_modified_time(self):
        if os.path.exists(self.filename):
            return os.path.getmtime(self.filename)
        else:
            raise FileNotFoundError(f"{self.filename} does not exist.")

    def check_modification(self):
        current_modified_time = self.get_last_modified_time()
        if current_modified_time != self.last_modified_time:
            affected_clients = []
            # Get the current time
            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            new_data = self.spawner.get_config()
            print(f'-------- at time {formatted_time} --------')
            for i, o_i, n_i in enumerate(zip(self.old_data, new_data)):
                if not o_i == n_i:
                    print(f'detected changes in config file {self.filename}, document {i}')
                    affected_clients.append(i)

            self.old_data = new_data

            flag = input('do you want to reload the affected clients with the new configuration? [y/n] -> ')
            if flag == 'y' or flag == 'Y':
                self.stop_flag = True

            self.last_modified_time = current_modified_time

    def watch(self, interval=1):
        while True:
            while not self.stop_flag:
                if self.spawner.watchdog_stop_event.is_set():
                    return True
                time.sleep(interval)
                self.check_modification()
            self.spawner.reload_single()
            self.stop_flag = False
