import paho.mqtt.client as mqtt
import json
import queue
import threading
import Utils.toolbox as t

# Configurazione dei broker e dei topic
broker_address = "localhost"
broker_port = 1883
input_topic = "input/topic"
output_topic = "output/topic"

# Coda per i messaggi da pubblicare
message_queue = queue.Queue()


# Funzione per gestire i messaggi in arrivo
def on_message(client, toolbox, message):
    payload = message.payload.decode("utf-8")
    print(f"Received message on topic {message.topic}: {payload}")

    # Applica una funzione ai messaggi in arrivo
    processed_message = process_message(toolbox, payload)

    # Aggiungi il messaggio elaborato alla coda
    message_queue.put(processed_message)


# Funzione di esempio per elaborare il messaggio
def process_message(toolbox, payload):
    return toolbox.run('upper', payload)



# Funzione per pubblicare i messaggi dalla coda
def publish_messages(client):
    while True:
        message = message_queue.get()
        client.publish(output_topic, message)
        print(f"Published message on topic {output_topic}: {message}")
        message_queue.task_done()


# Crea un nuovo client MQTT
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=t.MethodToolBox(),protocol=mqtt.MQTTv5)

# Imposta la funzione di callback per i messaggi in arrivo
mqtt_client.on_message = on_message

# Connettiti al broker MQTT
mqtt_client.connect(broker_address, broker_port)

# Iscriviti al topic di input
mqtt_client.subscribe(input_topic)

# Avvia un thread separato per pubblicare i messaggi dalla coda
publish_thread = threading.Thread(target=publish_messages, args=(mqtt_client,))
publish_thread.start()

# Avvia il loop per gestire i messaggi in arrivo
mqtt_client.loop_forever()
