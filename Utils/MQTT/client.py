import paho.mqtt.client as mqtt
import queue
import threading
import Utils.UserFunctions.toolbox as t
import Utils.OnFiles.yaml_loader as y


class MQTTClient:
    def __init__(self, yl: y.YamlLoader, t: t.MethodToolBox):
        self.loaded_data = yl.load()


if __name__ == "__main__":
    client = MQTTClient(y.YamlLoader(), t.MethodToolBox())
