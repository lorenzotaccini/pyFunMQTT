import queue
import sys
import threading
from types import SimpleNamespace

import paho.mqtt.client as mqtt

import Utils.OnFiles.yaml_loader as y
import Utils.UserFunctions.toolbox as t

QOS = 1
CALLBACK_VERSION = mqtt.CallbackAPIVersion.VERSION2


class MQTTClient(mqtt.Client):

    def __init__(self, yl: dict, toolbox: t.MethodToolBox):
        super().__init__(CALLBACK_VERSION)
        self.config_params = SimpleNamespace(**yl)  # Simplenamespace to improve usability within the class
        self.msg_queue = queue.Queue()
        self.toolbox = toolbox

        self.client = mqtt.Client(CALLBACK_VERSION)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_connect_fail = self.on_connect_fail

        self.publish_thread = threading.Thread(target=self.publish_messages)

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
        self.client.subscribe(self.config_params.inTopic)

    def on_connect_fail(self, client, userdata):
        print("First connection with the selected MQTT broker has failed, quitting.")
        sys.exit(-2)

    # Funzione di esempio per elaborare il messaggio
    def process_message(self, payload):
        return self.toolbox.process(self.config_params.function, payload)

    def publish_messages(self) -> None:
        while True:
            message = self.msg_queue.get()
            if message is None:  # TODO sostituire None con valore più appropriato
                self.msg_queue.task_done()
                print("quitting has been requested on publishing thread")
                return
            self.client.publish(self.config_params.outTopic, message, QOS)
            print(f"Published message on topic {self.config_params.outTopic}: {message}")
            self.msg_queue.task_done()

    def start(self) -> None:
        try:
            self.client.connect(host=self.config_params.broker, port=self.config_params.port)
            self.publish_thread.start()
            self.client.loop_start()
        except ConnectionRefusedError as cre:
            print(cre)
            sys.exit(-1)

    # disconnect the subscriber task, waits for the queue of messages that are being processed to be empty,
    # stops the publishing thread setting stop_event, waits for the thread to terminate
    def stop(self) -> None:
        print("stopping all workers...")
        self.client.disconnect()
        self.client.loop_stop()
        self.msg_queue.put(None)  # requests the interruption of publish thread
        self.msg_queue.join()
        self.publish_thread.join()
        print('all workers have stopped. Quitting...')
        sys.exit(1)


if __name__ == "__main__":
    client = MQTTClient(y.YamlLoader(), t.MethodToolBox())
    # signal.signal(signal.SIGTERM, client.stop)
    client.start()
    if input():
        client.stop()
