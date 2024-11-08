from utils.client import ClientFactory

class Etape3Subscriber:
    def __init__(self, data_list):
        self.data_list = data_list
        self.CLOUD_TOPIC = "tp4/cloud"
        self.BROKER = "localhost"
        self.PORT = 1883
        self.client = ClientFactory(self.CLOUD_TOPIC)
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        data = float(message.payload.decode())
        self.data_list.append(data)
        print(f"Etape 3 - Received data: {data}")

    def start(self):
        print('started etape3')
        self.client.connect(self.BROKER, self.PORT)
        self.client.subscribe(self.CLOUD_TOPIC)
        self.client.loop_forever()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
