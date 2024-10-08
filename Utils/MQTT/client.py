import queue
import sys
import threading
import logging
import secrets
import string

import paho.mqtt.client as mqtt

import Utils.UserFunctions.toolbox as t

QOS = 1
OUTPUT_TOPIC_PREFIX = 'out/'
CALLBACK_VERSION = mqtt.CallbackAPIVersion.VERSION2

logger = logging.getLogger(__name__)


class MQTTClient(mqtt.Client):

    def __init__(self, yl: dict, toolbox: t.MethodToolBox):
        super().__init__(CALLBACK_VERSION)
        self.__config_params = yl
        self.__msg_queue = queue.Queue()
        self.__stop_key = self.generate_stop_key()

        self.toolbox = toolbox
        self.client = mqtt.Client(CALLBACK_VERSION)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_connect_fail = self.on_connect_fail

        self.publish_thread = threading.Thread(target=self.publish_messages)

    # Incoming messages are put in a queue to be processed and re-set from publish_message function
    def on_message(self, mqttc, obj, message):
        payload = message.payload.decode("utf-8")
        logger.info(f"Received message on topic {message.topic}: {payload}")

        self.__msg_queue.put(payload)

    def on_connect(self, mqttc, obj, flags, reason_code, properties):
        logger.info(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe(self.__config_params['inTopic'])

    def on_connect_fail(self, client, userdata):
        logger.critical("Connection with the selected MQTT broker has failed, quitting.")
        self.stop()


    def process_message(self, payload):
        # TODO as of now, messages are strings and not serialized data files such as json yaml exc...
        return self.toolbox.process(self.__config_params,
                                    payload)

    def publish_messages(self) -> None:
        while True:
            message = self.__msg_queue.get()
            if message is self.__stop_key:
                self.__msg_queue.task_done()
                logger.info("quitting has been requested on publishing thread")
                return

            message = self.process_message(message)

            '''
            If processed data to publish is a dict (for example, splitting original data and publishing on different topics),
            key represents the topic on which the message will be published, value is the payload.
            This will also ignore the list of output topics given in config file.
            OTHER DATA IS NOT ALLOWED TO BE DICT, IT HAS TO BE IN SOME SORT OF DATA FORMAT LIKE JSON, CSV....
            '''
            if isinstance(message, dict):
                for key, value in message.items():
                    self.client.publish(OUTPUT_TOPIC_PREFIX+key, value, qos=QOS, retain=self.__config_params['retain'])
            else:
                for out_topic in self.__config_params['outTopic']:
                    self.client.publish(OUTPUT_TOPIC_PREFIX+out_topic, message, qos=QOS, retain=self.__config_params['retain'])

            logger.info(f"Published message on topic/s {self.__config_params['outTopic']}: {message}")
            self.__msg_queue.task_done()

    def get_configuration(self) -> dict:
        return self.__config_params

    @staticmethod
    def generate_stop_key() -> str:
        charset = string.ascii_letters + string.digits
        return ''.join(secrets.choice(charset) for _ in range(32))

    def start(self) -> None:
        try:
            logger.info(f"Starting MQTT client with configuration: {self.get_configuration()}")
            self.client.connect(host=self.__config_params['broker'], port=self.__config_params['port'])
            self.publish_thread.start()
            self.client.loop_start()
        except ConnectionRefusedError as cre:
            logger.critical(cre)
            sys.exit(-1)

    # disconnect the subscriber task, waits for the queue of messages that are being processed to be empty,
    # stops the publishing thread setting stop_event, waits for the thread to terminate
    def stop(self, quit_flag: bool = False) -> None:
        logger.info("stopping all client workers...")
        self.client.disconnect()
        self.client.loop_stop()
        self.__msg_queue.put(self.__stop_key)  # requests the interruption of publish thread
        self.__msg_queue.join()
        self.publish_thread.join()
        logger.info('mqtt service stopped')
        if quit_flag:
            logger.info('Quitting system...')
            sys.exit(1)
