import functools

import paho.mqtt.client as mqtt
import Utils.input_normalizer as norm
import Utils.toolbox as toolbox


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("on topic: " + msg.topic + " message: " + str(msg.payload))
    msg.payload = userdata.normalize(msg.payload)
    print(msg.payload)


    # TEST: APPLY NORMALIZER, APPLY FUNCTION, REPUBLISH


if __name__ == '__main__':
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=norm.YAMLNormalizer(), protocol=mqtt.MQTTv5)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect("localhost", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqttc.loop_forever()
