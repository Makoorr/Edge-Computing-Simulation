from utils.client import ClientFactory
from utils.movingaverage import moving_average
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

CLOUD_TOPIC = "tp4/cloud"
BROKER="localhost"
PORT=1883

data = []
original_data = []
reduced_data = []
WINDOW_SIZE = 3

client = ClientFactory(CLOUD_TOPIC)

def on_message(client, userdata, message):
    global original_data
    original_data.append(float(message.payload.decode()))
    data.append(float(message.payload.decode()))

    if len(data) < WINDOW_SIZE:
        return
    
    reduced_data.append(moving_average(data, WINDOW_SIZE))
    
    data.pop(0)
    print(f"Received reduced_data: {reduced_data}")

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
    ax.plot(original_data, label="Moyenne des données originals", color="g")
    ax.plot(reduced_data, label="Moyenne des données", color="b")
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