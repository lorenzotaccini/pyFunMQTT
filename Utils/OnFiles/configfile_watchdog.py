import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import Utils.cli as cli
from Utils.MQTT.client import MQTTClient


class ConfigFileWatchdog(FileSystemEventHandler):
    def __init__(self, worker):
        super().__init__()
        self.worker = worker
        self.configfile_name = worker.configfile_name

    def on_modified(self, event):
        if event.src_path.endswith(self.configfile_name):
            if input(f"at {time.localtime()} -> Detected changes in actual configuration file: '{self.configfile_name}'"
                     f"\nReload the session applying the new configuration? [y/n]: ") == ('Y' or 'y'):
                self.worker.reload()

    def watch(self):
        observer = Observer()
        observer.schedule(self, path='.', recursive=False)
        observer.start()
        try:
            while True:
                print("a")
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
