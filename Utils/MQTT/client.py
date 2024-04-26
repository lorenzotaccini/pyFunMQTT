import signal
import sys
import time

import paho.mqtt.client as mqtt
import queue
import threading
from types import SimpleNamespace
import Utils.UserFunctions.toolbox as t
import Utils.OnFiles.yaml_loader as y


class MQTTClient(mqtt.Client):

    def __init__(self, yl: y.YamlLoader, toolbox: t.MethodToolBox):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2)
        self.config_params = SimpleNamespace(**yl.load())  # Simplenamespace to improve usability within the class
        self.msg_queue = queue.Queue()
        self.toolbox = toolbox

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        self.stop_event = threading.Event()
        self.publish_thread = threading.Thread(target=self.publish_messages)

        # TODO completare, pensare al funzionamento bloccante della classe

    # Funzione per gestire i messaggi in arrivo
    def on_message(self, mqttc, obj, message):
        payload = message.payload.decode("utf-8")
        print(f"Received message on topic {message.topic}: {payload}")

        processed_message = self.process_message(payload)

        self.msg_queue.put(processed_message)

    def on_connect(self, mqttc, obj, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe(self.config_params.topic)

    # Funzione di esempio per elaborare il messaggio
    def process_message(self, payload):
        return self.toolbox.process(self.config_params.function, payload)

    def publish_messages(self) -> None:
        while True:
            if self.stop_event.is_set():
                break
            message = self.msg_queue.get()
            self.client.publish(self.config_params.outTopic, message)
            print(f"Published message on topic {self.config_params.outTopic}: {message}")
            self.msg_queue.task_done()

    def start(self):

        self.publish_thread.start()

        try:
            self.client.connect(host=self.config_params.broker, port=self.config_params.port)
            self.client.loop_start()
        except OSError:
            print("First connection with the selected MQTT broker has failed, quitting.")
            self.stop()
            return

    # disconnect the subscriber task, waits for the queue of messages that are being processed to be empty,
    # stops the publishing thread setting stop_event, waits for the thread to terminate
    def stop(self, sig, frame):
        print("stopping all workers...")
        self.client.disconnect()
        self.client.loop_stop()
        self.msg_queue.join()
        self.stop_event.set()
        self.publish_thread.join()
        print('all workers have stopped. Quitting...')


if __name__ == "__main__":
    client = MQTTClient(y.YamlLoader(), t.MethodToolBox())
    signal.signal(signal.SIGINT, client.stop)
    client.start()
