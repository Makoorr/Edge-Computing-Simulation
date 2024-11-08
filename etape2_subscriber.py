from utils.client import ClientFactory
from paho.mqtt import client as mqtt_client
import time
import threading

EDGE_TOPIC="tp4/topic"
CLOUD_TOPIC = "tp4/cloud"
BROKER="localhost"
PORT=1883

chunck_data = []
SAMPLING_PERIOD = 1

client = ClientFactory(EDGE_TOPIC)

def on_message(client, userdata, message):
    data = float(message.payload.decode())
    
    chunck_data.append(data)
    print(f"Received data: {data}")

def publish_average():
    while True:
        time.sleep(SAMPLING_PERIOD)

        if chunck_data:
            average = sum(chunck_data) / len(chunck_data)
            
            client.publish(CLOUD_TOPIC, average)
            print(f"Published average: {average}")
            
            chunck_data.clear()

client.on_message = on_message

client.connect(BROKER,PORT)
client.subscribe(EDGE_TOPIC)
client.loop_start()

threading.Thread(target=publish_average, daemon=True).start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Arrêt du programme")
finally:
    client.loop_stop()
    client.disconnect()