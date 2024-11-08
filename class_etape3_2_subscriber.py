from utils.client import ClientFactory
from utils.movingaverage import moving_average

class Etape3_2Subscriber:
    def __init__(self, data_list):
        self.data_list = data_list
        self.CLOUD_TOPIC = "tp4/cloud"
        self.BROKER = "localhost"
        self.PORT = 1883
        self.SAMPLING_PERIOD = 10
        self.client = ClientFactory(self.CLOUD_TOPIC)
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        data = moving_average(float(message.payload.decode()), self.SAMPLING_PERIOD)
        self.data_list.append(data)
        print(f"Etape 3.2 - Received data: {data}")

    def start(self):
        print('started etape 3.2')
        self.client.connect(self.BROKER, self.PORT)
        self.client.subscribe(self.CLOUD_TOPIC)
        self.client.loop_forever()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
