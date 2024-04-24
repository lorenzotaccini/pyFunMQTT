import paho.mqtt.client as mqtt
import queue
import threading
from types import SimpleNamespace
import Utils.UserFunctions.toolbox as t
import Utils.OnFiles.yaml_loader as y


class MQTTClient:

    def __init__(self, yl: y.YamlLoader, toolbox: t.MethodToolBox):
        self.config_params = SimpleNamespace(**yl.load())  # Simplenamespace to improve usability within the class
        self.msg_queue = queue.Queue()
        self.toolbox = toolbox

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=t)
        self.client.on_message = self.on_message

        # TODO completare classe, pensare al funzionamento bloccante della classe
        self.broker_address = "localhost"
        self.broker_port = 1883
        self.input_topic = "input/topic"
        self.output_topic = "output/topic"

    # Funzione per gestire i messaggi in arrivo
    def on_message(self, message):
        payload = message.payload.decode("utf-8")
        print(f"Received message on topic {message.topic}: {payload}")

        # Applica una funzione ai messaggi in arrivo
        processed_message = self.process_message(payload)

        # Aggiungi il messaggio elaborato alla coda
        self.msg_queue.put(processed_message)

    # Funzione di esempio per elaborare il messaggio
    def process_message(self, payload):
        return self.toolbox.process(self.config_params.function, payload)

    def publish_messages(self):
        while True:
            message = self.msg_queue.get()
            self.client.publish(self.config_params.outTopic, message)
            print(f"Published message on topic {self.config_params.outTopic}: {message}")
            self.msg_queue.task_done()

    def start(self):
        try:

            self.client.connect(self.config_params.broker, self.config_params.port)
            self.client.loop_forever()
        except OSError:
            print("First connection with the selected MQTT broker has failed, quitting.")
            return False


if __name__ == "__main__":
    client = MQTTClient(y.YamlLoader(), t.MethodToolBox())
