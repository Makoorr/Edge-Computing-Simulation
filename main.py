import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
from class_etape2_subscriber import Etape2Subscriber
from class_etape3_subscriber import Etape3Subscriber
from class_etape3_2_subscriber import Etape3_2Subscriber

EDGE_TOPIC = "tp4/topic"
CLOUD_TOPIC = "tp4/cloud"
BROKER = "localhost"
PORT = 1883

data_etape2 = []
data_etape3 = []
data_etape3_2 = []

subscriber_etape2 = Etape2Subscriber(EDGE_TOPIC, CLOUD_TOPIC, BROKER, PORT, data_etape2)
subscriber_etape3 = Etape3Subscriber(data_etape3)
subscriber_etape3_2 = Etape3_2Subscriber(data_etape3_2)

plt.style.use("seaborn")
fig, ax = plt.subplots()
ax.set_title("Comparaison des données moyennes publiées")
ax.set_xlabel("Temps")
ax.set_ylabel("Valeur moyenne")

def update(frame):
    ax.clear()
    ax.plot(data_etape3, label="Etape 3 - Données moyennes", color="b")
    ax.plot(data_etape3_2, label="Etape 3.2 - Données moyennes avec MA", color="r")
    ax.set_title("Comparaison des données moyennes publiées")
    ax.set_xlabel("Temps")
    ax.set_ylabel("Valeur moyenne")
    ax.legend()

thread_etape2 = threading.Thread(target=subscriber_etape2.start)
thread_etape3 = threading.Thread(target=subscriber_etape3.start)
thread_etape3_2 = threading.Thread(target=subscriber_etape3_2.start)

thread_etape2.start()
thread_etape3.start()
thread_etape3_2.start()

ani = FuncAnimation(fig, update, interval=1000)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Arrêt du programme")
finally:
    subscriber_etape2.stop()
    subscriber_etape3.stop()
    subscriber_etape3_2.stop()
