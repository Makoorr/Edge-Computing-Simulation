from utils.client import ClientFactory
from utils.simulator import Simulator

TOPIC="tp4/topic"
host="localhost"
PORT=1883

seed = 12345
mean = 20
standard_deviation = 5
simulator = Simulator(seed, mean, standard_deviation)

data_set = [simulator.calculate_next_value() for _ in range(100000)]

client = ClientFactory(topic=TOPIC)
client.connect(host,PORT)

for data in data_set:
    client.publish(TOPIC,data)