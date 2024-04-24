import paho.mqtt.client as mqtt
import queue
import threading
import Utils.UserFunctions.toolbox as t

# Configurazione dei broker e dei topic
broker_address = "localhost"
broker_port = 1883
input_topic = "input/topic"
output_topic = "output/topic"

# Coda per i messaggi da pubblicare
message_queue = queue.Queue()


# Funzione per gestire i messaggi in arrivo
def on_message(mqtt_client, toolbox, message):
    payload = message.payload.decode("utf-8")
    print(f"Received message on topic {message.topic}: {payload}")

    # Applica una funzione ai messaggi in arrivo
    processed_message = process_message(toolbox, payload)

    # Aggiungi il messaggio elaborato alla coda
    message_queue.put(processed_message)


# Funzione di esempio per elaborare il messaggio
def process_message(toolbox, payload):
    return toolbox.process('upper', payload)


def publish_messages(mqtt_client):
    while True:
        message = message_queue.get()
        mqtt_client.publish(output_topic, message)
        print(f"Published message on topic {output_topic}: {message}")
        message_queue.task_done()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=t.MethodToolBox())

client.on_message = on_message

client.connect(broker_address, broker_port)

client.subscribe(input_topic)

publish_thread = threading.Thread(target=publish_messages, args=(client,))
publish_thread.start()


client.loop_forever()
