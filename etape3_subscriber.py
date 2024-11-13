from utils.client import ClientFactory
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

CLOUD_TOPIC = "tp4/cloud"
BROKER="localhost"
PORT=1883

chunck_data = []

client = ClientFactory(CLOUD_TOPIC)

def on_message(client, userdata, message):
    data = float(message.payload.decode())
    
    chunck_data.append(data)
    print(f"Received data: {data}")

client.on_message = on_message
client.connect(BROKER,PORT)
client.subscribe(CLOUD_TOPIC)
client.loop_start()

plt.style.use("seaborn")
fig, ax = plt.subplots()
ax.set_title("Graphique des données moyennes publiées vers le cloud")
ax.set_xlabel("Temps")
ax.set_ylabel("Valeur moyenne")

def update(frame):
    ax.clear()
    ax.plot(chunck_data, label="Moyenne des données", color="b")
    ax.set_title("Graphique des données moyennes publiées vers le cloud")
    ax.set_xlabel("Temps")
    ax.set_ylabel("Valeur moyenne")
    ax.legend()

ani = FuncAnimation(fig, update, interval=1000)
plt.show()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Arrêt du programme")
finally:
    client.loop_stop()
    client.disconnect()