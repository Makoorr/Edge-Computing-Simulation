from paho.mqtt import client as mqtt_client
from termcolor import colored

def ClientFactory(topic):
    def on_connect(client: mqtt_client.Client, userdata, connect_flags, reason_code: mqtt_client.MQTTErrorCode, properties):
        if reason_code == mqtt_client.MQTTErrorCode.MQTT_ERR_SUCCESS:
            print(colored("Connected to MQTT Broker!","green"))
            client.subscribe(topic)
        else:
            print(colored(f"Failed to connect, return code {reason_code}","red"))

    def on_log(client, userdata, level, buf):
        if level == mqtt_client.MQTT_LOG_INFO:
            print(colored(f"[INFO] - {buf}","light_blue"))
        elif level == mqtt_client.MQTT_LOG_NOTICE:
            print(colored(f"[NOTICE] - {buf}","light_yellow"))
        elif level == mqtt_client.MQTT_LOG_WARNING:
            print(colored(f"[WARNING] - {buf}","light_magenta"))
        elif level == mqtt_client.MQTT_LOG_ERR:
            print(colored(f"[ERR] - {buf}","red"))
        elif level == mqtt_client.MQTT_LOG_DEBUG:
            print(f"[DEBUG] - {buf}")

    def on_message(client, userdata, msg: mqtt_client.MQTTMessage):
        print(colored(f"[MESSAGE] - {msg.topic.upper()} - {str(msg.payload)}","blue"))

    def on_disconnect (client, userdata, mid, reason_code, properties):
        print(colored("client disconnected","red"))

    client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    client.on_log = on_log
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # client.tls_set(ca_certs=ca)
    # client.tls_insecure_set(True)

    return client