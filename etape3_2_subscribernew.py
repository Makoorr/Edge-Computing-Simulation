from utils.client import ClientFactory
from utils.movingaverage import moving_average
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

CLOUD_TOPIC = "tp4/topic"
BROKER = "localhost"
PORT = 1883

data = []
original_data = []
reduced_data = []
original_times = []
reduced_times = []
WINDOW_SIZE = 10

client = ClientFactory(CLOUD_TOPIC)

def on_message(client, userdata, message):
    global original_data, reduced_data
    payload = float(message.payload.decode())
    current_time = datetime.now()

    original_data.append(payload)
    original_times.append(current_time)
    
    data.append(payload)

    if len(data) >= WINDOW_SIZE:
        avg = moving_average(data, WINDOW_SIZE)
        reduced_data.append(avg)
        reduced_times.append(current_time)
        
        data.pop(0)
    
    print(f"Received original data: {payload}, moving average: {reduced_data}")

client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe(CLOUD_TOPIC)
client.loop_start()

plt.style.use("seaborn")
fig, ax = plt.subplots()
ax.set_title("Graphique des données moyennes publiées vers le cloud")
ax.set_xlabel("Temps")
ax.set_ylabel("Valeur moyenne")

def update(frame):
    ax.clear()

    if original_times:
        ax.plot(original_times, original_data, label="Données originales", color="g")

    if reduced_times:
        ax.plot(reduced_times, reduced_data, label="Moyenne mobile", color="b")

    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    
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