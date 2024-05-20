import sys

import paho.mqtt.client as mqtt


def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")


if __name__=='__main__':

    unacked_publish = set()
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_publish = on_publish

    mqttc.user_data_set(unacked_publish)
    mqttc.connect("localhost")
    mqttc.loop_start()

    lorem = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore "
        "magna aliqua. Sit amet porttitor eget dolor morbi non. Commodo viverra maecenas accumsan lacus vel facilisis "
        "volutpat est. Duis at consectetur lorem donec massa sapien faucibus et. Amet dictum sit amet justo donec "
        "enim diam vulputate ut. Euismod in pellentesque massa placerat duis ultricies. Rutrum tellus pellentesque eu "
        "tincidunt tortor aliquam nulla facilisi cras. In hac habitasse platea dictumst quisque. Scelerisque felis "
        "imperdiet proin fermentum leo vel orci porta non. Elementum curabitur vitae nunc sed velit dignissim. Eget "
        "lorem dolor sed viverra ipsum nunc. Mauris in aliquam sem fringilla ut morbi tincidunt augue interdum. "
        "Tempor orci dapibus ultrices in. Morbi tincidunt ornare massa eget egestas purus viverra. Cum sociis natoque "
        "penatibus et magnis dis parturient montes. Donec et odio pellentesque diam volutpat commodo sed. Turpis "
        "tincidunt id aliquet risus feugiat in ante metus dictum.")

    for i in range(5000):
        # Our application produce some messages
        print(i)
        msg_info = mqttc.publish("i/1", "{}. {}".format(i, lorem), qos=1)
        unacked_publish.add(msg_info.mid)  # mid is MESSAGE ID

        # Due to race-condition described above, the following way to wait for all publish is safer
        msg_info.wait_for_publish()

    mqttc.disconnect()
    mqttc.loop_stop()
    sys.exit(10)


