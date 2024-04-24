#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation

# This example shows how you can use the MQTT client in a class.

import paho.mqtt.client as mqtt


class MyMQTTClass(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, reason_code, properties):
        print("rc: "+str(reason_code))

    def on_connect_fail(self, mqttc, obj):
        print("Connect failed")

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid, reason_codes, properties):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, reason_code_list, properties):
        print("Subscribed: "+str(mid)+" "+str(reason_code_list))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def run(self):
        self.connect("mqtt.eclipseprojects.io", 1883, 60)
        self.subscribe("$SYS/#", 0)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


# If you want to use a specific client id, use
# mqttc = MyMQTTClass("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = MyMQTTClass(mqtt.CallbackAPIVersion.VERSION2)
rc = mqttc.run()

print("rc: "+str(rc))