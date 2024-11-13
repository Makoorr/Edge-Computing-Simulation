from utils.process import Generation_pub_messages_oneTopic
from utils.simulator import Simulator
from paho.mqtt import client as mqtt_client

BROKER="localhost"
topic="tp4/topic"

print("Start message publication....") 

client = mqtt_client.Client(client_id="Pub", callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)  
client.connect(BROKER)

seed = 12345
mean = 20
standard_deviation = 5
simulator = Simulator(seed, mean, standard_deviation)

data_set = [simulator.calculate_next_value() for _ in range(100000)]

print("start periodic publish")

# l : lambda arrivals per seconds
l=50
NbreMessages = len(data_set)
Generation_pub_messages_oneTopic(client, l, NbreMessages, data_set, topic)