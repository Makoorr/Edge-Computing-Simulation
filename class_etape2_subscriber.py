from utils.client import ClientFactory
import time
import threading

class Etape2Subscriber:
    def __init__(self, edge_topic, cloud_topic, broker, port, data_list, sampling_period=1):
        self.edge_topic = edge_topic
        self.cloud_topic = cloud_topic
        self.broker = broker
        self.port = port
        self.data_list = data_list
        self.sampling_period = sampling_period
        self.chunck_data = []
        
        self.client = ClientFactory(edge_topic)
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        data = float(message.payload.decode())
        self.chunck_data.append(data)
        print(f"Etape 2 - Received data: {data}")

    def publish_average(self):
        while True:
            time.sleep(self.sampling_period)
            if self.chunck_data:
                average = sum(self.chunck_data) / len(self.chunck_data)
                self.data_list.append(average)
                self.client.publish(self.cloud_topic, average)
                print(f"Etape 2 - Published average: {average}")
                self.chunck_data.clear()

    def start(self):
        print('started etape2')
        self.client.connect(self.broker, self.port)
        self.client.subscribe(self.edge_topic)
        self.client.loop_start()
        
        self.publish_thread = threading.Thread(target=self.publish_average, daemon=True)
        self.publish_thread.start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
