import paho.mqtt.client as mqtt
from PIL import Image
import io


# Funzione per salvare l'immagine dal payload ricevuto
def save_image_from_payload(payload: bytes, output_path: str):
    """
    Riceve un payload rappresentante un'immagine PNG e salva l'immagine in locale.

    :param payload: Il payload in formato byte che rappresenta l'immagine PNG.
    :param output_path: Il percorso dove salvare l'immagine.
    """
    try:
        image_stream = io.BytesIO(payload)
        image = Image.open(image_stream)
        image.save(output_path)
        print(f"Immagine salvata correttamente in: {output_path}")
    except Exception as e:
        print(f"Errore durante il salvataggio dell'immagine: {e}")


# Callback quando viene ricevuto un messaggio
def on_message(client, userdata, msg):
    print(f"Messaggio ricevuto su {msg.topic} con {len(msg.payload)} byte")

    # Salva l'immagine dal payload
    output_image_path = "received_image.png"
    save_image_from_payload(msg.payload, output_image_path)


# Funzione principale per connettersi al broker MQTT e iscriversi al topic
def main():
    broker = "localhost"  # Indirizzo del broker MQTT
    port = 1883  # Porta MQTT standard
    topic = "image/png"  # Topic su cui sottoscriversi

    # Crea un client MQTT
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Imposta la callback per la ricezione dei messaggi
    client.on_message = on_message

    # Connetti al broker
    try:
        client.connect(broker, port, 60)
    except Exception as e:
        print(f"Errore durante la connessione al broker MQTT: {e}")
        return

    # Sottoscrivi al topic
    client.subscribe(topic)
    print(f"Iscritto al topic: {topic}")

    # Mantieni il client in ascolto per i messaggi
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Chiusura del client MQTT.")


if __name__ == "__main__":
    main()
